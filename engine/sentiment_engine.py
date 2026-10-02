"""
NETRA Social Intelligence Platform - Sentiment & Emotional Intelligence Engine
Provides multi-dimensional polarity classification, emotional vector extraction
(Anger, Fear, Joy, Trust, Urgency), and topic-based sentiment aggregation.
"""

import re
from typing import Dict, Any, List

# Lexicon weighted patterns for social/cyber intelligence
POSITIVE_LEXICON = {
    "neutralized": 0.8, "secured": 0.9, "safe": 0.7, "protect": 0.8, "verified": 0.9,
    "success": 0.8, "resolved": 0.85, "equalizer": 0.75, "booming": 0.8, "upgrade": 0.7,
    "deterrence": 0.6, "clarification": 0.6, "capacity": 0.5, "protection": 0.8, "innovative": 0.7
}

NEGATIVE_LEXICON = {
    "breach": -0.85, "attack": -0.8, "blackout": -0.95, "imminent": -0.7, "collapse": -0.9,
    "panic": -0.85, "scam": -0.9, "fraud": -0.9, "manipulation": -0.8, "fake": -0.75,
    "strangle": -0.7, "destroy": -0.8, "probe": -0.5, "threat": -0.75, "emergency": -0.8,
    "forfeiture": -0.7, "severity": -0.6
}

EMOTION_PATTERNS = {
    "fear": ["blackout", "collapse", "imminent", "panic", "emergency", "severity", "strain"],
    "anger": ["hiding", "strangle", "scam", "shilling", "manipulation", "capture", "monopolies"],
    "trust": ["cert-in", "verified", "who", "isro", "pib", "protect", "advisory", "official", "safeguard"],
    "joy": ["booming", "success", "innovative", "deterrence", "equalizer", "upgrade"],
    "urgency": ["alert", "now", "warning", "immediate", "breaking", "caution", "rush"]
}

class SentimentEngine:
    def __init__(self):
        pass

    def analyze_post(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment, polarity, and emotional intensity of a post.
        """
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)

        pos_score = sum(POSITIVE_LEXICON.get(w, 0) for w in words)
        neg_score = sum(abs(NEGATIVE_LEXICON.get(w, 0)) for w in words)

        # Exclamation emphasis
        exclamation_factor = 1.0 + min(0.5, text.count('!') * 0.1)

        raw_score = (pos_score - neg_score) * exclamation_factor
        total_signals = pos_score + neg_score + 0.001

        # Normalized compound score between -1.0 and +1.0
        normalized_compound = max(-1.0, min(1.0, raw_score / (total_signals + 1.5)))

        if normalized_compound > 0.15:
            classification = "Positive"
        elif normalized_compound < -0.15:
            classification = "Negative"
        else:
            classification = "Neutral"

        # Emotional vector detection
        emotions = {}
        for emotion, terms in EMOTION_PATTERNS.items():
            match_count = sum(1 for term in terms if term in text_lower)
            emotions[emotion] = min(1.0, round(match_count * 0.35, 2))

        # Stance classification (Tactical Intelligence distinction)
        if any(w in text_lower for w in ["imminent", "collapse", "total blackout", "going 1000x"]):
            stance = "Sensational / Alarmist"
        elif any(w in text_lower for w in ["confirming", "advisory", "telemetry", "clarification", "neutralized"]):
            stance = "Authoritative / Factual"
        elif any(w in text_lower for w in ["analyzing", "notice how", "productivity", "disagree"]):
            stance = "Analytical / Discussion"
        else:
            stance = "General Public"

        return {
            "score": round(normalized_compound, 3),
            "classification": classification,
            "emotions": emotions,
            "stance": stance
        }

    def aggregate_by_topic(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate sentiment breakdown across identified topics.
        """
        topic_summary = {}
        for post in posts:
            topic = post.get("primary_topic", "General Discourse")
            sentiment = post.get("sentiment", {}).get("classification", "Neutral")
            score = post.get("sentiment", {}).get("score", 0.0)

            if topic not in topic_summary:
                topic_summary[topic] = {
                    "total": 0, "positive": 0, "negative": 0, "neutral": 0,
                    "avg_score": 0.0, "scores": []
                }

            topic_summary[topic]["total"] += 1
            topic_summary[topic][sentiment.lower()] += 1
            topic_summary[topic]["scores"].append(score)

        for topic, data in topic_summary.items():
            if data["scores"]:
                data["avg_score"] = round(sum(data["scores"]) / len(data["scores"]), 3)
            del data["scores"]

        return topic_summary
