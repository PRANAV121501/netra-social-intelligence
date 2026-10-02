"""
NETRA — Fact-Check & Misinformation Debunking Radar
Cross-references detected narrative claims against verified national registries
(PIB Fact Check, CERT-In Advisories, RBI Financial Fraud Alerts, National Disaster Management).
"""

from typing import List, Dict, Any
import re

VERIFIED_REGISTRY = [
    {
        "claim_pattern": r"(grid|power|blackout|substation|northern)",
        "topic": "NationalSecurity",
        "verdict": "FLAGGED // COGNITIVE WARFARE",
        "credibility_score": 14,
        "manipulation_index": 88,
        "official_status": "DEBUNKED",
        "fact": "Northern Power Grid operates normally. Isolated telemetry anomaly was contained by CERT-In without service disruption.",
        "registry_source": "CERT-In Advisory CI-2026-0928 & Ministry of Power",
        "debunk_url": "https://pib.gov.in/factcheck/power-grid-update"
    },
    {
        "claim_pattern": r"(ai.*banned|banning ai|ai ban|prohibit ai)",
        "topic": "IndiaAI",
        "verdict": "FALSE CLAIM // ASTROTURFING",
        "credibility_score": 22,
        "manipulation_index": 76,
        "official_status": "FABRICATED",
        "fact": "IndiaAI mission has allocated Rs 10,372 Cr for domestic GPU compute and sovereign foundation models. No ban proposed.",
        "registry_source": "MeitY IndiaAI Mission Release 2026",
        "debunk_url": "https://pib.gov.in/factcheck/india-ai-policy"
    },
    {
        "claim_pattern": r"(stock|market crash|sebi.*freeze|trading halt)",
        "topic": "StockRally",
        "verdict": "SUSPICIOUS // MARKET MANIPULATION",
        "credibility_score": 31,
        "manipulation_index": 82,
        "official_status": "MANIPULATED",
        "fact": "Stock exchanges NSE & BSE operated under normal surveillance circuits. Rumors triggered by bot-driven pump/dump channels.",
        "registry_source": "SEBI Surveillance Alert & NSE Notification",
        "debunk_url": "https://sebi.gov.in/surveillance/alerts-2026"
    },
    {
        "claim_pattern": r"(climate.*hoax|carbon tax.*fraud|renewable.*shutdown)",
        "topic": "ClimateAction",
        "verdict": "UNVERIFIED NARRATIVE",
        "credibility_score": 39,
        "manipulation_index": 64,
        "official_status": "MISLEADING",
        "fact": "India continues expanding solar/wind capacity under National Solar Mission with 180GW target on track.",
        "registry_source": "MNRE Official Bulletin 2026",
        "debunk_url": "https://mnre.gov.in/facts-renewable-targets"
    },
    {
        "claim_pattern": r"(cyber.*ransomware.*aiims|hospital.*leak|aadhaar.*hacked)",
        "topic": "CyberSecurity",
        "verdict": "PARTIALLY TRUE // EXAGGERATED",
        "credibility_score": 52,
        "manipulation_index": 58,
        "official_status": "EXAGGERATED",
        "fact": "Probing attempts detected on peripheral subnets; main databases and biometric vaults remain untouched behind zero-trust architecture.",
        "registry_source": "National Critical Information Infrastructure Protection Centre (NCIIPC)",
        "debunk_url": "https://nciipc.gov.in/bulletin/cyber-defense-oct"
    }
]

class FactCheckRadar:
    """Verifies posts and narratives against truth registries and computes deception metrics."""

    def __init__(self):
        self.registry = VERIFIED_REGISTRY

    def analyze_claims(self, posts: List[Dict[str, Any]], narratives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        seen_patterns = set()

        # Check posts
        for post in posts:
            content = post.get("content", "").lower()
            for entry in self.registry:
                if re.search(entry["claim_pattern"], content):
                    key = entry["topic"] + entry["official_status"]
                    if key not in seen_patterns:
                        seen_patterns.add(key)
                        results.append({
                            "claim_sample": post.get("content", "")[:120] + "...",
                            "author": post.get("author", "Unknown"),
                            "topic": entry["topic"],
                            "verdict": entry["verdict"],
                            "credibility_score": entry["credibility_score"],
                            "manipulation_index": entry["manipulation_index"],
                            "official_status": entry["official_status"],
                            "fact": entry["fact"],
                            "registry_source": entry["registry_source"],
                            "debunk_url": entry["debunk_url"],
                            "timestamp": post.get("timestamp", "2026-09-28T10:00:00Z"),
                            "amplification": post.get("retweets", 0) + post.get("likes", 0)
                        })

        # Ensure at least curated default findings exist if stream is small
        if not results:
            for entry in self.registry[:3]:
                results.append({
                    "claim_sample": f"Viral claim circulating in {entry['topic']} discussions alleging critical system abnormalities.",
                    "author": "Synthesized_Monitor",
                    "topic": entry["topic"],
                    "verdict": entry["verdict"],
                    "credibility_score": entry["credibility_score"],
                    "manipulation_index": entry["manipulation_index"],
                    "official_status": entry["official_status"],
                    "fact": entry["fact"],
                    "registry_source": entry["registry_source"],
                    "debunk_url": entry["debunk_url"],
                    "timestamp": "2026-09-28T12:00:00Z",
                    "amplification": 1420
                })

        return sorted(results, key=lambda x: x["manipulation_index"], reverse=True)
