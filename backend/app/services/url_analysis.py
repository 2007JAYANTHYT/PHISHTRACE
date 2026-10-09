import re
from urllib.parse import urlparse
from typing import List, Dict, Any
from ..models.schemas import UrlIndicator

SUSPICIOUS_TLDS = {".top", ".xyz", ".work", ".click", ".buzz", ".country", ".gq", ".ml", ".cf", ".tk", ".su", ".fit", ".rest"}
TYPOSQUAT_KEYWORDS = ["microsoft", "paypal", "google", "apple", "amazon", "chase", "bankofamerica", "wellsfargo", "netflix", "dropbox", "docusign", "office365", "outlook"]

def is_ip_literal(host: str) -> bool:
    """Check if host is a raw IP address rather than a domain name."""
    clean_host = host.split(":")[0].strip("[]")
    parts = clean_host.split(".")
    if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
        return True
    return False

def analyze_url(url: str, anchor_text: str = "") -> UrlIndicator:
    """Forensically inspects a single URL for phishing and deception indicators."""
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
    except Exception:
        host = ""

    risk_score = 0
    risk_reasons: List[str] = []
    
    # Check IP-literal
    is_ip = is_ip_literal(host)
    if is_ip:
        risk_score += 45
        risk_reasons.append("Raw IP-literal URL host bypasses DNS reputation filters")

    # Check Punycode / IDN homograph attack
    is_puny = host.startswith("xn--") or ".xn--" in host
    if is_puny:
        risk_score += 40
        risk_reasons.append("Punycode (IDN) domain detected: potential homograph spoofing")

    # Check Suspicious TLDs
    has_suspicious_tld = any(host.endswith(tld) for tld in SUSPICIOUS_TLDS)
    if has_suspicious_tld:
        risk_score += 25
        risk_reasons.append(f"High-abuse top-level domain ({host.split('.')[-1]})")

    # Lookalike brand typosquatting check
    is_lookalike = False
    clean_alphanumeric = re.sub(r'[^a-z0-9]', '', host)
    for brand in TYPOSQUAT_KEYWORDS:
        if brand in host and not (host.endswith(f".{brand}.com") or host == f"{brand}.com"):
            is_lookalike = True
            risk_score += 35
            risk_reasons.append(f"Deceptive brand keyword '{brand}' found in suspicious non-official domain '{host}'")
            break

    # Anchor mismatch check
    anchor_mismatch = False
    if anchor_text:
        anchor_clean = anchor_text.strip().lower()
        if (anchor_clean.startswith("http://") or anchor_clean.startswith("https://") or "www." in anchor_clean):
            try:
                anchor_host = urlparse(anchor_clean if anchor_clean.startswith("http") else f"https://{anchor_clean}").hostname or ""
                if anchor_host and anchor_host != host:
                    anchor_mismatch = True
                    risk_score += 40
                    risk_reasons.append(f"Deceptive anchor text display ('{anchor_clean}') diverts to completely different destination host ('{host}')")
            except Exception:
                pass

    # Excessive subdomains (deep nesting evasion)
    subdomain_parts = host.split(".")
    if len(subdomain_parts) > 4 and not is_ip:
        risk_score += 15
        risk_reasons.append(f"Excessively nested subdomains ({len(subdomain_parts)} parts)")

    return UrlIndicator(
        url=url,
        host=host,
        is_ip_literal=is_ip,
        is_lookalike=is_lookalike,
        suspicious_tld=has_suspicious_tld,
        anchor_mismatch=anchor_mismatch,
        risk_score=min(100, risk_score),
        risk_reasons=risk_reasons
    )

def analyze_all_urls(urls: List[str], body_html: str = "") -> List[UrlIndicator]:
    """Analyzes a collection of URLs with anchor correlation."""
    indicators: List[UrlIndicator] = []
    
    # Extract anchor text mappings if html exists
    anchor_map = {}
    if body_html:
        matches = re.findall(r'<a\s+(?:[^>]*?\s+)?href=["\']([^"\']+)["\'][^>]*>(.*?)<\/a>', body_html, re.IGNORECASE | re.DOTALL)
        for href, text in matches:
            plain_text = re.sub(r'<[^>]+>', '', text).strip()
            anchor_map[href.strip()] = plain_text

    for u in urls:
        anchor = anchor_map.get(u, "")
        indicators.append(analyze_url(u, anchor))

    return indicators
