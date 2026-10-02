"""
NETRA Social Intelligence Platform - Narrative Detection Engine
Deconstructs macro topics into competing, emerging sub-narratives.
Analyzes narrative stance, polarity, volume, and amplification vectors.
"""

from typing import List, Dict, Any
from collections import defaultdict

NARRATIVE_TAXONOMY = {
    "Critical Infrastructure & Cyber Defense": [
        {
            "id": "nar_infra_1",
            "name": "State-Sponsored APT29 Power Grid Infiltration",
            "keywords": ["apt29", "ioc", "power grid", "phishing", "ddos"],
            "stance": "Critical / Threat Disclosure",
            "driver_accounts": ["@CyberSentinel_IN"]
        },
        {
            "id": "nar_infra_2",
            "name": "SCADA Telemetry Defense & Zero-Downtime Neutralization",
            "keywords": ["scada", "firewall", "neutralized", "telemetry", "forensic"],
            "stance": "Defensive / Reassuring",
            "driver_accounts": ["@DrRajeshPatel"]
        },
        {
            "id": "nar_infra_3",
            "name": "Coordinated Blackout Panic Disinformation Swarm",
            "keywords": ["total blackout", "imminent", "fuel", "cash", "panic"],
            "stance": "Hostile / Disinformation",
            "driver_accounts": ["@bot_grid_echo_01", "@EagleEye_News24"]
        },
        {
            "id": "nar_infra_4",
            "name": "Cognitive Priming Exposure & Official Counter-Measures",
            "keywords": ["pib_factcheck", "fake news", "cognitive priming", "clarification"],
            "stance": "Institutional Counter-Narrative",
            "driver_accounts": ["@PIB_FactCheck", "@AnanyaRoy_Tech"]
        }
    ],
    "Artificial Intelligence & Future of Work": [
        {
            "id": "nar_ai_1",
            "name": "Developer Disruption & Entry-Level Job Consolidation",
            "keywords": ["code synthesis", "consolidation", "productivity", "techjobs", "curriculum"],
            "stance": "Concerned / Economic Caution",
            "driver_accounts": ["@Aravind_AI"]
        },
        {
            "id": "nar_ai_2",
            "name": "New High-Leverage Roles & AI Productivity Boom",
            "keywords": ["hiring", "leverage", "prompt engineering", "safety auditing", "booming"],
            "stance": "Optimistic / Market Expansion",
            "driver_accounts": ["@SarahChen_SF"]
        },
        {
            "id": "nar_ai_3",
            "name": "Sovereign AI Regulations, UNESCO & Mandatory Bias Audits",
            "keywords": ["unesco", "regulation", "sovereign", "oversight", "bias audits"],
            "stance": "Regulatory / Governance",
            "driver_accounts": ["@Prof_ElenaV"]
        },
        {
            "id": "nar_ai_4",
            "name": "AI Tutors Democratizing Rural Education",
            "keywords": ["rural", "equalizer", "math", "edtech", "schools"],
            "stance": "Constructive / Social Impact",
            "driver_accounts": ["@KaranSharma_Ed"]
        },
        {
            "id": "nar_ai_5",
            "name": "Open-Weights Defense vs Big Tech Regulatory Capture",
            "keywords": ["regulatory capture", "open-weights", "llama", "strangle", "sovereignty"],
            "stance": "Anti-Monopoly / Open Source",
            "driver_accounts": ["@MarcusVance_AI"]
        }
    ],
    "Financial Integrity & Market Surveillance": [
        {
            "id": "nar_fin_1",
            "name": "Automated Penny Token Pump & Dump ($CYNX)",
            "keywords": ["cynx", "1000x", "dex", "whale", "next bitcoin"],
            "stance": "Hostile / Financial Fraud",
            "driver_accounts": ["@crypto_pump_bot01", "@crypto_pump_bot02"]
        },
        {
            "id": "nar_fin_2",
            "name": "FinSec Syndicate Detection & Eastern Europe Proxies",
            "keywords": ["proxies", "syndicates", "finsec", "surveillance", "retail"],
            "stance": "Forensic / Security Alert",
            "driver_accounts": ["@FinSecIntel"]
        },
        {
            "id": "nar_fin_3",
            "name": "SEBI Enforcement & Forfeiture Warning",
            "keywords": ["sebi", "forfeiture", "market integrity", "surveillance"],
            "stance": "Regulatory / Deterrence",
            "driver_accounts": ["@SEBI_OfficialWatcher"]
        }
    ],
    "Geopolitics & Defense Technologies": [
        {
            "id": "nar_geo_1",
            "name": "Quantum-Encrypted Space Constellation Deterrence",
            "keywords": ["isro", "drdo", "quantum-encrypted", "satellite", "deterrence"],
            "stance": "Strategic / Capability Display",
            "driver_accounts": ["@DefSecMonitor"]
        },
        {
            "id": "nar_geo_2",
            "name": "Maritime ISR Shield over Malacca Strait SLOCs",
            "keywords": ["malacca strait", "isr", "maritime", "autonomy", "sensor"],
            "stance": "National Security / Sovereignty",
            "driver_accounts": ["@Col_SanjeevVerma"]
        }
    ],
    "Public Health & Bio-Surveillance": [
        {
            "id": "nar_health_1",
            "name": "Genomic Strain High-Transmissibility / Low Severity",
            "keywords": ["transmissibility", "mrna", "hospitalization", "genomic"],
            "stance": "Scientific / Reassuring",
            "driver_accounts": ["@DrMeeraNambiar"]
        },
        {
            "id": "nar_health_2",
            "name": "Airport Health Screening & Stockpile Readiness",
            "keywords": ["airport", "delhi", "mumbai", "screening", "buffer"],
            "stance": "Public Advisory / Protective",
            "driver_accounts": ["@PublicHealth_IN"]
        }
    ]
}

class NarrativeEngine:
    def __init__(self):
        pass

    def detect_narratives(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Maps conversational streams to defined and emerging sub-narrative clusters.
        """
        all_narratives = []

        for topic, templates in NARRATIVE_TAXONOMY.items():
            for template in templates:
                matching_posts = []
                for post in posts:
                    content_lower = post.get("content", "").lower()
                    # Match if any keyword matches
                    matches = sum(1 for kw in template["keywords"] if kw in content_lower)
                    if matches >= 1:
                        matching_posts.append(post)

                if matching_posts:
                    total_likes = sum(p.get("likes", 0) for p in matching_posts)
                    total_retweets = sum(p.get("retweets", 0) for p in matching_posts)
                    post_count = len(matching_posts)
                    
                    # Sentiment distribution within narrative
                    sentiments = [p.get("sentiment", {}).get("classification", "Neutral") for p in matching_posts]
                    dominant_sentiment = max(set(sentiments), key=sentiments.count) if sentiments else "Neutral"

                    all_narratives.append({
                        "id": template["id"],
                        "topic": topic,
                        "narrative": template["name"],
                        "stance": template["stance"],
                        "post_count": post_count,
                        "engagement": total_likes + total_retweets,
                        "dominant_sentiment": dominant_sentiment,
                        "primary_drivers": template["driver_accounts"],
                        "keywords": template["keywords"][:4],
                        "sample_excerpt": matching_posts[0].get("content", "")[:130] + "..."
                    })

        all_narratives.sort(key=lambda x: x["engagement"], reverse=True)
        return all_narratives
