import email
from email import policy
import hashlib
import re
import html
from typing import Tuple, Dict, Any, List, Optional
from pathlib import Path

MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024 # 15 MB max

def compute_sha256(data: bytes) -> str:
    """Compute deterministic SHA-256 hex digest of raw bytes."""
    return hashlib.sha256(data).hexdigest()

def sanitize_filename(name: str) -> str:
    """Strip directory traversal sequences and invalid filesystem characters."""
    if not name:
        return "unnamed_attachment"
    clean = Path(name).name
    clean = re.sub(r'[^a-zA-Z0-9_\-\.\(\)\s]', '_', clean)
    return clean.strip() or "unnamed_attachment"

def sanitize_html(html_content: str) -> str:
    """
    Sanitize HTML email body to prevent script execution, external injection,
    and dangerous embedded elements in the SOC preview.
    """
    if not html_content:
        return ""
    # Strip script tags and their contents
    cleaned = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html_content, flags=re.IGNORECASE)
    # Strip iframes, objects, embeds, applets
    cleaned = re.sub(r'<(iframe|object|embed|applet)\b[^>]*>.*?<\/\1>', '', cleaned, flags=re.IGNORECASE)
    # Strip self-closing or lone iframe/embeds
    cleaned = re.sub(r'<(iframe|object|embed|applet)\b[^>]*\/?>', '', cleaned, flags=re.IGNORECASE)
    # Strip event handlers (onload, onerror, onclick, etc.)
    cleaned = re.sub(r'\s+on[a-zA-Z]+\s*=\s*["\'][^"\']*["\']', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+on[a-zA-Z]+\s*=\s*[^\s>]+', '', cleaned, flags=re.IGNORECASE)
    # Neutralize dangerous javascript: hrefs
    cleaned = re.sub(r'href\s*=\s*["\']javascript:[^"\']*["\']', 'href="#"', cleaned, flags=re.IGNORECASE)
    return cleaned

def extract_urls_from_text(text: str) -> List[str]:
    """Find URLs inside plain text and HTML anchors."""
    url_pattern = r'https?://[^\s<>"\')]+'
    found = re.findall(url_pattern, text)
    # Remove trailing punctuation often captured at sentence end
    cleaned_urls = []
    for u in found:
        u = re.sub(r'[\.,;\)]$', '', u)
        if u not in cleaned_urls:
            cleaned_urls.append(u)
    return cleaned_urls

class ParsedEmailData:
    def __init__(self):
        self.message_id: str = ""
        self.subject: str = "(No Subject)"
        self.sender_from: str = ""
        self.sender_display_name: str = ""
        self.sender_domain: str = ""
        self.reply_to: str = ""
        self.return_path: str = ""
        self.recipient_to: str = ""
        self.date: str = ""
        self.received_headers: List[str] = []
        self.auth_results_raw: str = ""
        self.received_spf_raw: str = ""
        self.dkim_signature_raw: str = ""
        self.arc_results_raw: str = ""
        self.body_text: str = ""
        self.body_html: str = ""
        self.sanitized_body_preview: str = ""
        self.urls: List[str] = []
        self.attachments: List[Dict[str, Any]] = []
        self.original_digest: str = ""
        self.raw_bytes_size: int = 0

def parse_email_bytes(raw_bytes: bytes) -> ParsedEmailData:
    """
    Robust RFC-compliant email parsing using standard library.
    Enforces size limits, safe MIME decoding, and cryptographic evidence hashing.
    """
    if len(raw_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError(f"Email file size ({len(raw_bytes)} bytes) exceeds the maximum 15MB security threshold.")
    
    data = ParsedEmailData()
    data.original_digest = compute_sha256(raw_bytes)
    data.raw_bytes_size = len(raw_bytes)

    try:
        msg = email.message_from_bytes(raw_bytes, policy=policy.default)
    except Exception as e:
        raise ValueError(f"Failed to parse email MIME structure: {str(e)}")

    # Extract core RFC headers
    data.message_id = str(msg.get("Message-ID", "")).strip() or f"<generated-{data.original_digest[:16]}@phishtrace.local>"
    data.subject = str(msg.get("Subject", "(No Subject)")).strip()
    data.sender_from = str(msg.get("From", "")).strip()
    data.reply_to = str(msg.get("Reply-To", "")).strip()
    data.return_path = str(msg.get("Return-Path", "")).strip()
    data.recipient_to = str(msg.get("To", "")).strip()
    data.date = str(msg.get("Date", "")).strip()

    # Parse display name and domain from From
    from_header = data.sender_from
    if "<" in from_header and ">" in from_header:
        display_part = from_header.split("<")[0].strip().strip('"\'')
        data.sender_display_name = display_part
        email_part = from_header.split("<")[1].split(">")[0].strip()
        if "@" in email_part:
            data.sender_domain = email_part.split("@")[-1].lower()
    elif "@" in from_header:
        data.sender_domain = from_header.split("@")[-1].lower().strip()
        data.sender_display_name = from_header.split("@")[0].strip()

    # Extract authentication headers
    data.auth_results_raw = str(msg.get("Authentication-Results", "")).strip()
    data.received_spf_raw = str(msg.get("Received-SPF", "")).strip()
    data.dkim_signature_raw = str(msg.get("DKIM-Signature", "")).strip()
    data.arc_results_raw = str(msg.get("ARC-Authentication-Results", "")).strip()

    # Extract Received headers in original order (top is most recent hop, bottom is earliest)
    received_list = msg.get_all("Received") or []
    data.received_headers = [str(h).strip() for h in received_list]

    # Walk MIME payload safely
    body_text_parts = []
    body_html_parts = []

    for part in msg.walk():
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition", ""))

        # Check for attachment
        is_attachment = ("attachment" in content_disposition.lower()) or (part.get_filename() is not None)

        if is_attachment:
            raw_filename = part.get_filename() or "attachment.dat"
            safe_name = sanitize_filename(raw_filename)
            try:
                payload = part.get_payload(decode=True) or b""
            except Exception:
                payload = b""
            
            att_hash = compute_sha256(payload)
            att_size = len(payload)
            
            # Risk check on extensions
            ext = Path(safe_name).suffix.lower()
            dangerous_exts = {".exe", ".scr", ".vbs", ".bat", ".cmd", ".ps1", ".js", ".hta", ".iso", ".img", ".xlsm", ".docm"}
            is_exec = ext in dangerous_exts
            is_double = len(safe_name.split(".")) > 2 and any(safe_name.lower().endswith(de) for de in dangerous_exts)
            
            risk_flags = []
            if is_exec:
                risk_flags.append(f"High-risk executable or script attachment extension ({ext})")
            if is_double:
                risk_flags.append("Evasive double-extension detected (e.g. .pdf.exe)")
            if att_size > 5 * 1024 * 1024:
                risk_flags.append("Large attachment size (>5MB)")

            data.attachments.append({
                "filename": safe_name,
                "content_type": content_type,
                "size_bytes": att_size,
                "sha256_hash": att_hash,
                "is_executable": is_exec,
                "is_double_extension": is_double,
                "risk_reasons": risk_flags
            })
        else:
            # Body content
            try:
                if content_type == "text/plain":
                    text_content = part.get_payload(decode=True)
                    if text_content:
                        charset = part.get_content_charset() or "utf-8"
                        body_text_parts.append(text_content.decode(charset, errors="replace"))
                elif content_type == "text/html":
                    html_content = part.get_payload(decode=True)
                    if html_content:
                        charset = part.get_content_charset() or "utf-8"
                        body_html_parts.append(html_content.decode(charset, errors="replace"))
            except Exception:
                pass

    data.body_text = "\n\n".join(body_text_parts)
    data.body_html = "\n\n".join(body_html_parts)

    # Sanitize preview
    if data.body_html:
        data.sanitized_body_preview = sanitize_html(data.body_html)
    else:
        # Convert plain text to safe HTML preview
        escaped = html.escape(data.body_text)
        data.sanitized_body_preview = f"<pre style='font-family:monospace;white-space:pre-wrap;'>{escaped}</pre>"

    # Extract all unique URLs
    urls_found = extract_urls_from_text(data.body_text) + extract_urls_from_text(data.body_html)
    data.urls = list(dict.fromkeys(urls_found))

    return data
