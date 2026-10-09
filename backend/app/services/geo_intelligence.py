import json
import ipaddress
import urllib.request
import urllib.error
from typing import Optional, Dict, Any
from pathlib import Path
from ..config import settings
from ..models.schemas import GeoInfo

# Built-in offline curated intelligence cache for demo / zero-network environments
CURATED_OFFLINE_GEO = {
    # Microsoft / Office 365 MTAs
    "40.107.92.54": {"country": "United States", "country_code": "US", "city": "Redmond", "region": "Washington", "latitude": 47.674, "longitude": -122.1215, "org": "Microsoft Corporation", "asn": "AS8075"},
    "40.92.74.88": {"country": "United States", "country_code": "US", "city": "Des Moines", "region": "Iowa", "latitude": 41.6005, "longitude": -93.6091, "org": "Microsoft Corporation", "asn": "AS8075"},
    # Google Workspace MTAs
    "209.85.220.41": {"country": "United States", "country_code": "US", "city": "Mountain View", "region": "California", "latitude": 37.4056, "longitude": -122.0775, "org": "Google LLC", "asn": "AS15169"},
    "209.85.216.170": {"country": "United States", "country_code": "US", "city": "Council Bluffs", "region": "Iowa", "latitude": 41.2619, "longitude": -95.8608, "org": "Google LLC", "asn": "AS15169"},
    # Suspicious Foreign / Bulletproof Hosting MTAs
    "185.220.101.5": {"country": "Germany", "country_code": "DE", "city": "Frankfurt", "region": "Hesse", "latitude": 50.1109, "longitude": 8.6821, "org": "Zwiebelfreunde Tor Exit", "asn": "AS200651"},
    "194.26.29.112": {"country": "Russia", "country_code": "RU", "city": "Moscow", "region": "Moscow", "latitude": 55.7558, "longitude": 37.6173, "org": "Bulletproof Hosting Services", "asn": "AS49392"},
    "198.54.117.200": {"country": "United States", "country_code": "US", "city": "Phoenix", "region": "Arizona", "latitude": 33.4484, "longitude": -112.074, "org": "Namecheap Inc", "asn": "AS22612"},
    "103.253.144.10": {"country": "India", "country_code": "IN", "city": "Bengaluru", "region": "Karnataka", "latitude": 12.9716, "longitude": 77.5946, "org": "Hostinger Cloud", "asn": "AS46015"},
    "45.154.255.89": {"country": "Netherlands", "country_code": "NL", "city": "Amsterdam", "region": "North Holland", "latitude": 52.3676, "longitude": 4.9041, "org": "Chang Way Technologies", "asn": "AS57523"},
    "91.240.118.42": {"country": "Seychelles", "country_code": "SC", "city": "Victoria", "region": "Mahe", "latitude": -4.6191, "longitude": 55.4513, "org": "Anonymized Offshore VPS", "asn": "AS60117"}
}

class GeoIntelligenceService:
    def __init__(self):
        self.cache_file = settings.IP_GEO_CACHE_FILE
        self._cache: Dict[str, Dict[str, Any]] = self._load_cache()

    def _load_cache(self) -> Dict[str, Dict[str, Any]]:
        cache = dict(CURATED_OFFLINE_GEO)
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cache.update(data)
            except Exception:
                pass
        return cache

    def _save_cache(self):
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, indent=2)
        except Exception:
            pass

    def is_routable_public_ip(self, ip_str: str) -> bool:
        """Strictly validates if an IP address is valid and globally routable."""
        if not ip_str:
            return False
        try:
            ip = ipaddress.ip_address(ip_str.strip())
            return not (ip.is_private or ip.is_loopback or ip.is_link_local or 
                        ip.is_reserved or ip.is_multicast or ip.is_unspecified)
        except ValueError:
            return False

    def lookup_ip(self, ip_str: str) -> GeoInfo:
        """
        Geolocate an IP address safely.
        Private/local IPs are NEVER sent to any public service.
        """
        ip_clean = (ip_str or "").strip()
        if not ip_clean:
            return GeoInfo(ip="unknown", is_private=True, org="Invalid IP")

        try:
            parsed = ipaddress.ip_address(ip_clean)
            if parsed.is_private or parsed.is_loopback or parsed.is_link_local or parsed.is_reserved:
                return GeoInfo(
                    ip=ip_clean,
                    country="Local / Private",
                    city="RFC1918 Intranet",
                    region="Private Subnet",
                    is_private=True,
                    org="Internal Enterprise Gateway",
                    source="Private Address Space"
                )
        except ValueError:
            return GeoInfo(ip=ip_clean, is_private=True, org="Unparseable IP")

        # Check memory / offline curated cache first
        if ip_clean in self._cache:
            entry = self._cache[ip_clean]
            return GeoInfo(
                ip=ip_clean,
                country=entry.get("country", "Unknown"),
                country_code=entry.get("country_code", ""),
                city=entry.get("city", "Unknown"),
                region=entry.get("region", "Unknown"),
                latitude=entry.get("latitude"),
                longitude=entry.get("longitude"),
                org=entry.get("org", "Unknown"),
                asn=entry.get("asn", "Unknown"),
                is_private=False,
                source="Cached SOC Intelligence"
            )

        # Fallback to public free IP-API with strict 2-second timeout
        try:
            url = f"http://ip-api.com/json/{ip_clean}?fields=status,message,country,countryCode,regionName,city,lat,lon,isp,org,as"
            req = urllib.request.Request(url, headers={"User-Agent": "PhishTrace-Forensics/1.0"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("status") == "success":
                    geo = GeoInfo(
                        ip=ip_clean,
                        country=data.get("country"),
                        country_code=data.get("countryCode"),
                        city=data.get("city"),
                        region=data.get("regionName"),
                        latitude=data.get("lat"),
                        longitude=data.get("lon"),
                        org=data.get("org") or data.get("isp"),
                        asn=data.get("as"),
                        is_private=False,
                        source="Live IP-API Lookup"
                    )
                    self._cache[ip_clean] = geo.dict()
                    self._save_cache()
                    return geo
        except Exception:
            pass

        # If live lookup fails or times out, return unknown
        return GeoInfo(
            ip=ip_clean,
            country="Unknown Location",
            city="Lookup Unavailable",
            region="Unknown",
            is_private=False,
            org="Public Gateway",
            source="Unresolved Public IP"
        )

geo_service = GeoIntelligenceService()
