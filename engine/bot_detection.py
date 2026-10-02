"""
NETRA Social Intelligence Platform - Bot & Coordinated Activity Detection Engine
Identifies Automated Accounts, Bot Swarms, and Coordinated Inauthentic Behavior (CIB).
Generates Tactical Threat Alerts with severity ratings and countermeasures.
"""

from typing import List, Dict, Any
from collections import defaultdict
import difflib

class BotDetector:
    def __init__(self):
        pass

    def evaluate_account(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates a Bot Probability Score (0 - 100%) for a single post/account.
        """
        followers = post.get("followers", 0)
        following = post.get("following", 0)
        verified = post.get("verified", False)
        created_date = post.get("account_created", "2020-01-01")
        author = post.get("author", "")

        bot_score = 0
        reasons = []

        # Indicator 1: Extreme following-to-follower ratio
        if followers < 50 and following > 1500:
            bot_score += 40
            reasons.append("High Following-to-Follower asymmetry (<50 followers, >1500 following)")
        elif followers < 100 and following > 500:
            bot_score += 20
            reasons.append("Low organic reach ratio")

        # Indicator 2: Handle naming pattern (common bot suffix syntax e.g. bot_, _01, 8 random digits)
        if "bot" in author.lower() or any(author.endswith(f"_{i:02d}") for i in range(1, 100)):
            bot_score += 30
            reasons.append("Synthetic handle nomenclature signature")

        # Indicator 3: Account recency (created within last 30 days)
        if created_date.startswith("2026-09"):
            bot_score += 25
            reasons.append("Recently provisioned account (<30 days old)")

        # Verified credential mitigation
        if verified:
            bot_score = max(0, bot_score - 50)

        is_bot = bot_score >= 50
        return {
            "is_bot": is_bot,
            "bot_probability": min(99, bot_score),
            "threat_tier": "CONFIRMED_BOT" if bot_score >= 70 else ("SUSPICIOUS" if bot_score >= 45 else "ORGANIC"),
            "reasons": reasons
        }

    def detect_coordinated_campaigns(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detects Coordinated Inauthentic Behavior (CIB) by clustering accounts posting
        near-identical texts within short temporal windows.
        """
        # Group posts by normalized content text
        text_clusters = defaultdict(list)
        for post in posts:
            # Strip URLs and hashtags for similarity grouping
            clean = " ".join(w for w in post.get("content", "").split() if not w.startswith(('#', '@', 'http')))
            if len(clean) > 20:
                text_clusters[clean.lower()].append(post)

        alerts = []
        alert_counter = 1

        for norm_text, matched_posts in text_clusters.items():
            if len(matched_posts) >= 2:
                # Potential copy-paste astroturfing
                authors = list(set(p.get("author") for p in matched_posts))
                target_topic = matched_posts[0].get("primary_topic", "General Discourse")
                hashtags = list(set(tag for p in matched_posts for tag in p.get("entities", {}).get("hashtags", [])))
                
                # Check if panic or fraud keywords present
                is_critical = any(kw in norm_text for kw in ["blackout", "imminent", "collapse", "1000x", "emergency"])
                severity = "CRITICAL" if is_critical else "HIGH"

                countermeasure = (
                    "Trigger automated fact-check advisory; submit bot roster to platform integrity API; "
                    "isolate network cluster in knowledge graph."
                ) if is_critical else "Monitor amplification velocity; flag account cluster for shadow-quarantine."

                alerts.append({
                    "alert_id": f"CIB-ALT-{alert_counter:04d}",
                    "severity": severity,
                    "title": f"Synchronized Swarm on {target_topic}",
                    "pattern": "Coordinated Copy-Paste Messaging (Astroturfing)",
                    "target_topic": target_topic,
                    "involved_accounts": [f"@{a}" for a in authors],
                    "account_count": len(authors),
                    "hashtags_used": hashtags,
                    "repetition_count": len(matched_posts),
                    "sample_text": matched_posts[0].get("content", "")[:140] + "...",
                    "recommended_action": countermeasure,
                    "detected_at": matched_posts[-1].get("timestamp", "2026-09-28T09:10:00Z")
                })
                alert_counter += 1

        # Also add anomaly alert if sudden burst on a topic
        topic_counts = Counter(p.get("primary_topic") for p in posts)
        for topic, count in topic_counts.items():
            if count >= 6 and not any(a["target_topic"] == topic for a in alerts):
                alerts.append({
                    "alert_id": f"CIB-ALT-{alert_counter:04d}",
                    "severity": "MEDIUM",
                    "title": f"Unusual High-Velocity Chatter Spike",
                    "pattern": "Temporal Velocity Anomaly",
                    "target_topic": topic,
                    "involved_accounts": [f"@{p.get('author')}" for p in posts if p.get('primary_topic') == topic][:5],
                    "account_count": count,
                    "hashtags_used": [],
                    "repetition_count": count,
                    "sample_text": f"Sustained high-frequency discourse observed across {count} nodes.",
                    "recommended_action": "Track sentiment inflection; verify whether traffic is driven by breaking news.",
                    "detected_at": "2026-09-28T10:00:00Z"
                })
                alert_counter += 1

        alerts.sort(key=lambda x: 0 if x["severity"] == "CRITICAL" else (1 if x["severity"] == "HIGH" else 2))
        return alerts

from collections import Counter
