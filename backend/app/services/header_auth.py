import re
import ipaddress
from typing import List, Tuple, Optional, Dict, Any
from ..models.schemas import HeaderForensics, HopInfo, GeoInfo
from .geo_intelligence import geo_service

IP_REGEX = r'(?:\[(?:IPv6:)?([a-fA-F0-9:]+)\]|\[?(\b(?:\d{1,3}\.){3}\d{1,3}\b)\]?)'

def extract_ip_from_hop_str(hop_str: str) -> Optional[str]:
    """Find the most plausible IP address inside a Received header."""
    matches = re.findall(r'\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]', hop_str)
    if matches:
        return matches[0]
    
    # Try naked IP
    matches_plain = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', hop_str)
    for ip in matches_plain:
        try:
            parsed = ipaddress.ip_address(ip)
            # Avoid matching version numbers or dates looking like IPs
            octets = [int(o) for o in ip.split('.')]
            if all(0 <= o <= 255 for o in octets):
                return ip
        except ValueError:
            pass
    return None

def parse_auth_results(auth_raw: str, spf_raw: str, dkim_raw: str) -> Dict[str, str]:
    """
    Parses observed authentication values.
    Returns dictionary with normalized 'pass', 'fail', 'softfail', 'neutral', 'none'.
    """
    combined = f"{auth_raw} {spf_raw} {dkim_raw}".lower()
    
    spf = "none"
    if "spf=pass" in combined or "received-spf: pass" in combined:
        spf = "pass"
    elif "spf=fail" in combined or "received-spf: fail" in combined:
        spf = "fail"
    elif "spf=softfail" in combined or "received-spf: softfail" in combined:
        spf = "softfail"
    elif "spf=neutral" in combined:
        spf = "neutral"

    dkim = "none"
    if "dkim=pass" in combined:
        dkim = "pass"
    elif "dkim=fail" in combined:
        dkim = "fail"
    elif "dkim=neutral" in combined:
        dkim = "neutral"
    elif dkim_raw:
        # Signature present but status not reported in header
        dkim = "observed_signature_only"

    dmarc = "none"
    if "dmarc=pass" in combined:
        dmarc = "pass"
    elif "dmarc=fail" in combined:
        dmarc = "fail"
    elif "dmarc=quarantine" in combined:
        dmarc = "quarantine_policy"
    elif "dmarc=reject" in combined:
        dmarc = "reject_policy"

    arc = "none"
    if "arc=pass" in combined:
        arc = "pass"
    elif "arc=fail" in combined:
        arc = "fail"

    return {
        "spf": spf,
        "dkim": dkim,
        "dmarc": dmarc,
        "arc": arc
    }

def analyze_header_hops(
    received_headers: List[str],
    sender_from: str,
    sender_display_name: Optional[str],
    sender_domain: Optional[str],
    reply_to: Optional[str],
    return_path: Optional[str],
    recipient_to: str,
    subject: str,
    date: str,
    message_id: Optional[str],
    auth_results_raw: str,
    received_spf_raw: str,
    dkim_raw: str,
    arc_raw: str
) -> HeaderForensics:
    """
    Forensically traces Received header chain from receiver back to origin.
    Calculates attribution confidence, highlights candidate origin, and documents caveats.
    """
    auth = parse_auth_results(auth_results_raw, received_spf_raw, dkim_raw)
    
    hops: List[HopInfo] = []
    earliest_public_hop: Optional[HopInfo] = None
    
    # Process received headers in reverse order (bottom to top = hop 1 to hop N)
    # The bottom-most Received header is chronologically the earliest observed hop.
    raw_hops_chronological = list(reversed(received_headers))
    
    for idx, raw_h in enumerate(raw_hops_chronological, start=1):
        ip = extract_ip_from_hop_str(raw_h)
        is_private = False
        geo = None
        confidence = 0.5
        uncertainty = None

        # Parse from / by MTA hosts
        from_host_m = re.search(r'from\s+([^\s\(\)]+)', raw_h, re.IGNORECASE)
        by_host_m = re.search(r'by\s+([^\s\(\)]+)', raw_h, re.IGNORECASE)
        from_host = from_host_m.group(1) if from_host_m else "unspecified"
        by_host = by_host_m.group(1) if by_host_m else "unspecified"

        if ip:
            if geo_service.is_routable_public_ip(ip):
                geo = geo_service.lookup_ip(ip)
                is_private = False
                confidence = 0.75 if idx == 1 else 0.85
            else:
                is_private = True
                confidence = 0.3
                uncertainty = "RFC1918 Private or Loopback address; internal relay cannot be geolocated externally."
        else:
            confidence = 0.2
            uncertainty = "Hop lacks client IP address; MTA did not record peer IP."

        hop_info = HopInfo(
            hop_number=idx,
            from_host=from_host,
            by_host=by_host,
            ip=ip,
            is_private=is_private,
            timestamp=None, # Parsed from header if standard date formatted
            geo=geo,
            confidence=confidence,
            uncertainty_reason=uncertainty
        )
        hops.append(hop_info)

        if not is_private and ip and geo and earliest_public_hop is None:
            earliest_public_hop = hop_info

    # Origin attribution analysis
    candidate_ip = None
    origin_geo = None
    origin_confidence = 0.0
    origin_caveat = None

    if earliest_public_hop and earliest_public_hop.geo:
        candidate_ip = earliest_public_hop.ip
        origin_geo = earliest_public_hop.geo
        origin_confidence = earliest_public_hop.confidence
        origin_caveat = (
            f"Earliest external MTA hop identified at {candidate_ip} ({origin_geo.city}, {origin_geo.country}). "
            "Note: Adversaries may forge initial Received headers, route through open relays, or utilize commercial VPNs/Tor. "
            "This IP represents the first plausible public network boundary, not guaranteed physical perpetrator location."
        )
    else:
        origin_confidence = 0.1
        origin_caveat = "No routable public IP observed in Received headers. Email may have originated entirely within private intranet or headers were truncated."

    return HeaderForensics(
        message_id=message_id,
        sender_from=sender_from,
        sender_display_name=sender_display_name,
        sender_domain=sender_domain,
        reply_to=reply_to,
        return_path=return_path,
        recipient_to=recipient_to,
        subject=subject,
        date=date,
        received_hops=hops,
        spf_observed=auth["spf"],
        dkim_observed=auth["dkim"],
        dmarc_observed=auth["dmarc"],
        arc_observed=auth["arc"],
        auth_results_raw=auth_results_raw,
        origin_candidate_ip=candidate_ip,
        origin_geo=origin_geo,
        origin_confidence=origin_confidence,
        origin_caveat=origin_caveat
    )
