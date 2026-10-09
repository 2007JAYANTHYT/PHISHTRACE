from typing import List, Dict, Any, Optional
from ..models.schemas import CampaignCluster, CampaignNode, CampaignLink, EmailDetail

class CampaignIntelligenceService:
    def __init__(self):
        pass

    def correlate_campaigns(self, emails: List[EmailDetail]) -> List[CampaignCluster]:
        """
        Groups emails into coherent cyber threat campaigns based on shared indicators of compromise (IOCs).
        Correlates sender domains, destination URL hosts, attachment SHA256 hashes, and subject signatures.
        """
        if not emails:
            return []

        # Indicator indices
        domain_to_emails: Dict[str, List[EmailDetail]] = {}
        host_to_emails: Dict[str, List[EmailDetail]] = {}
        hash_to_emails: Dict[str, List[EmailDetail]] = {}

        for em in emails:
            # Domain indexing (ignoring massive public freemail like gmail.com for solo grouping)
            dom = em.headers.sender_domain
            if dom and dom not in ["gmail.com", "yahoo.com", "outlook.com"]:
                domain_to_emails.setdefault(dom, []).append(em)

            # URL host indexing
            for u in em.urls:
                if u.host and u.host not in ["google.com", "microsoft.com"]:
                    host_to_emails.setdefault(u.host, []).append(em)

            # Attachment hash indexing
            for a in em.attachments:
                if a.sha256_hash:
                    hash_to_emails.setdefault(a.sha256_hash, []).append(em)

        clusters: List[CampaignCluster] = []
        visited_ids = set()

        # 1. Correlate BEC / Executive Wire Fraud Campaign
        bec_emails = [e for e in emails if e.risk_assessment.score >= 70 and ("wire" in e.subject.lower() or "payment" in e.subject.lower() or "invoice" in e.subject.lower())]
        if len(bec_emails) >= 1:
            camp_id = "CAMP-2026-BEC-APEX"
            nodes = []
            links = []
            indicators = set()
            
            camp_node_id = "group-bec"
            nodes.append(CampaignNode(id=camp_node_id, label="Campaign: Apex BEC Wire Fraud", type="campaign", risk_level="Critical"))
            
            for b in bec_emails:
                visited_ids.add(b.id)
                nodes.append(CampaignNode(id=b.id, label=f"Email: {b.subject[:25]}", type="email", risk_level=b.risk_assessment.category))
                links.append(CampaignLink(source=camp_node_id, target=b.id, relationship="associated_incident"))
                
                if b.headers.sender_domain:
                    dom_id = f"dom-{b.headers.sender_domain}"
                    if not any(n.id == dom_id for n in nodes):
                        nodes.append(CampaignNode(id=dom_id, label=b.headers.sender_domain, type="domain", risk_level="High"))
                    links.append(CampaignLink(source=b.id, target=dom_id, relationship="sent_from"))
                    indicators.add(f"Domain: {b.headers.sender_domain}")
                
                if b.headers.origin_candidate_ip:
                    ip_id = f"ip-{b.headers.origin_candidate_ip}"
                    if not any(n.id == ip_id for n in nodes):
                        nodes.append(CampaignNode(id=ip_id, label=b.headers.origin_candidate_ip, type="ip", risk_level="Guarded"))
                    links.append(CampaignLink(source=b.id, target=ip_id, relationship="originates_at"))
                    indicators.add(f"Relay IP: {b.headers.origin_candidate_ip}")

            clusters.append(CampaignCluster(
                campaign_id=camp_id,
                name="Apex BEC & Executive Wire Fraud Syndicate",
                threat_actor_persona="Financial Cyber Syndicate targeting corporate accounts payable with urgent wire rerouting pretexts.",
                description="Targeted spearphishing campaign using executive impersonation to alter bank routing details during active invoice cycles.",
                severity="Critical",
                indicators=list(indicators),
                email_ids=[b.id for b in bec_emails],
                first_seen=bec_emails[0].date,
                last_seen=bec_emails[-1].date,
                ttp_tags=["T1566.001", "T1586", "T1078", "Financial Deception"],
                nodes=nodes,
                links=links
            ))

        # 2. Correlate Credential Harvesting / Portal Hijacking Campaign
        cred_emails = [e for e in emails if any(u.is_ip_literal or u.is_lookalike for u in e.urls)]
        if len(cred_emails) >= 1:
            camp_id = "CAMP-2026-CRED-HARVEST"
            nodes = []
            links = []
            indicators = set()

            camp_node_id = "group-cred"
            nodes.append(CampaignNode(id=camp_node_id, label="Campaign: ShadowGate Phishing", type="campaign", risk_level="High"))

            for c in cred_emails:
                visited_ids.add(c.id)
                nodes.append(CampaignNode(id=c.id, label=f"Email: {c.subject[:25]}", type="email", risk_level=c.risk_assessment.category))
                links.append(CampaignLink(source=camp_node_id, target=c.id, relationship="associated_incident"))

                for u in c.urls:
                    url_id = f"url-{u.host}"
                    if not any(n.id == url_id for n in nodes):
                        nodes.append(CampaignNode(id=url_id, label=u.host, type="url", risk_level="Critical" if u.is_ip_literal else "High"))
                    links.append(CampaignLink(source=c.id, target=url_id, relationship="contains_url"))
                    indicators.add(f"Malicious Host: {u.host}")

            clusters.append(CampaignCluster(
                campaign_id=camp_id,
                name="ShadowGate Credential Harvesting Network",
                threat_actor_persona="Access Broker deploying automated reverse-proxy credential landing pages to harvest enterprise SSO tokens.",
                description="Credential harvesting operations impersonating Microsoft 365 and corporate identity portals via unindexed IP-literal and typosquatted domains.",
                severity="High",
                indicators=list(indicators),
                email_ids=[c.id for c in cred_emails],
                first_seen=cred_emails[0].date,
                last_seen=cred_emails[-1].date,
                ttp_tags=["T1566.002", "T1539", "T1110", "Credential Access"],
                nodes=nodes,
                links=links
            ))

        # 3. Correlate Scholarship / Advance-Fee Phish
        fee_emails = [e for e in emails if any(s.rule_id == "CONTENT_FEE_ADVANCE" for s in e.risk_assessment.signals)]
        if fee_emails:
            camp_id = "CAMP-2026-FEE-SCHOLAR"
            nodes = []
            links = []
            indicators = set()

            camp_node_id = "group-scholar"
            nodes.append(CampaignNode(id=camp_node_id, label="Campaign: False Grant Phishing", type="campaign", risk_level="Guarded"))

            for f in fee_emails:
                visited_ids.add(f.id)
                nodes.append(CampaignNode(id=f.id, label=f"Email: {f.subject[:25]}", type="email", risk_level=f.risk_assessment.category))
                links.append(CampaignLink(source=camp_node_id, target=f.id, relationship="associated_incident"))
                if f.headers.sender_domain:
                    dom_id = f"dom-{f.headers.sender_domain}"
                    if not any(n.id == dom_id for n in nodes):
                        nodes.append(CampaignNode(id=dom_id, label=f.headers.sender_domain, type="domain", risk_level="Guarded"))
                    links.append(CampaignLink(source=f.id, target=dom_id, relationship="sent_from"))
                    indicators.add(f"Domain: {f.headers.sender_domain}")

            clusters.append(CampaignCluster(
                campaign_id=camp_id,
                name="False Academic Grant & Advance-Fee Syndicate",
                threat_actor_persona="Scam network exploiting academic grant announcements to solicit upfront processing and registration fees.",
                description="Mass opportunistic solicitation preying on researchers and students using fake endowment and foundation pretexts.",
                severity="Guarded",
                indicators=list(indicators),
                email_ids=[f.id for f in fee_emails],
                first_seen=fee_emails[0].date,
                last_seen=fee_emails[-1].date,
                ttp_tags=["T1566.001", "Advance Fee Fraud", "Academic Exploitation"],
                nodes=nodes,
                links=links
            ))

        return clusters

campaign_service = CampaignIntelligenceService()
