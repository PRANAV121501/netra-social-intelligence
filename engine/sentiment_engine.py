"""
NETRA Social Intelligence Platform - Sentiment & Emotional Intelligence Engine
Provides multi-dimensional polarity classification, emotional vector extraction
(Anger, Fear, Anxiety, Joy, Excitement, Trust, Urgency, Sarcasm), stance detection
(Supportive / Against / Neutral), and topic-based sentiment aggregation.
"""

import re
from typing import Dict, Any, List

# Lexicon weighted patterns for social/cyber intelligence
POSITIVE_LEXICON = {
    "neutralized": 0.8, "secured": 0.9, "safe": 0.7, "protect": 0.8, "verified": 0.9,
    "success": 0.8, "resolved": 0.85, "equalizer": 0.75, "booming": 0.8, "upgrade": 0.7,
    "deterrence": 0.6, "clarification": 0.6, "capacity": 0.5, "protection": 0.8, "innovative": 0.7,
    "celebrate": 0.75, "achievement": 0.8, "milestone": 0.7, "proud": 0.7, "victory": 0.85,
    "support": 0.65, "help": 0.6, "solidarity": 0.7, "hope": 0.65, "progress": 0.7
}

NEGATIVE_LEXICON = {
    "breach": -0.85, "attack": -0.8, "blackout": -0.95, "imminent": -0.7, "collapse": -0.9,
    "panic": -0.85, "scam": -0.9, "fraud": -0.9, "manipulation": -0.8, "fake": -0.75,
    "strangle": -0.7, "destroy": -0.8, "probe": -0.5, "threat": -0.75, "emergency": -0.8,
    "forfeiture": -0.7, "severity": -0.6, "corrupt": -0.85, "lie": -0.75, "expose": -0.6,
    "ban": -0.65, "fail": -0.7, "crisis": -0.85, "disaster": -0.9, "alarming": -0.75
}

EMOTION_PATTERNS = {
    "fear":      ["blackout", "collapse", "imminent", "panic", "emergency", "severity", "strain", "danger", "threat", "catastrophe"],
    "anxiety":   ["worried", "concern", "uncertain", "unstable", "nervous", "uneasy", "stress", "tense", "apprehensive", "dread", "anxious", "fear spreading"],
    "anger":     ["hiding", "strangle", "scam", "shilling", "manipulation", "capture", "monopolies", "outrage", "furious", "corrupt", "betrayed", "unacceptable"],
    "trust":     ["cert-in", "verified", "who", "isro", "pib", "protect", "advisory", "official", "safeguard", "confirmed", "credible", "authorized"],
    "joy":       ["booming", "success", "innovative", "deterrence", "equalizer", "upgrade", "proud", "celebrate", "milestone", "victory", "amazing"],
    "excitement":["breaking", "launch", "announce", "just in", "wow", "incredible", "groundbreaking", "historic", "first ever", "massive", "game changer", "trending"],
    "urgency":   ["alert", "now", "warning", "immediate", "breaking", "caution", "rush", "urgent", "asap", "critical", "sos", "act now"],
    "sarcasm":   ["oh sure", "totally fine", "great job", "wow much", "yeah right", "obviously", "of course they", "because that always", "real shocker", "color me surprised", "nothing to see"]
}

# Sarcasm detection patterns (contextual phrases + punctuation signals)
SARCASM_SIGNALS = [
    r"oh\s+sure",
    r"totally\s+fine",
    r"great\s+job.*(?:again|as\s+usual|right)",
    r"yeah\s+right",
    r"real\s+shocker",
    r"color\s+me\s+surprised",
    r"because\s+that\s+always\s+works",
    r"nothing\s+to\s+see\s+here",
    r"wow\s+so\s+brave",
    r"of\s+course\s+they\s+did",
    r"totally\s+normal",
    r"so\s+unexpected",
    r"absolutely\s+shocked",
    r"what\s+a\s+surprise"
]

class SentimentEngine:
    def __init__(self):
        self._sarcasm_patterns = [re.compile(p, re.IGNORECASE) for p in SARCASM_SIGNALS]

    def _detect_sarcasm(self, text: str) -> float:
        """Returns sarcasm confidence score 0.0–1.0"""
        score = 0.0
        for pattern in self._sarcasm_patterns:
            if pattern.search(text):
                score += 0.4
        # Punctuation signals: multiple !!! or ??? or "..."
        if re.search(r'[!?]{2,}', text):
            score += 0.15
        if re.search(r'\.{3,}', text):
            score += 0.1
        # Emoji irony combos
        if re.search(r'🙄|🤡|😂.*(?:sure|right|fine)', text, re.IGNORECASE):
            score += 0.2
        return min(1.0, round(score, 2))

    def analyze_post(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment, polarity, and emotional intensity of a post.
        Returns: score, classification, emotions (8 vectors), stance, sarcasm_score, support_stance
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

        # Emotional vector detection (8 dimensions)
        emotions = {}
        for emotion, terms in EMOTION_PATTERNS.items():
            match_count = sum(1 for term in terms if term in text_lower)
            emotions[emotion] = min(1.0, round(match_count * 0.35, 2))

        # Sarcasm detection
        sarcasm_score = self._detect_sarcasm(text)
        emotions["sarcasm"] = sarcasm_score
        # If high sarcasm, flip classification
        if sarcasm_score > 0.4 and classification == "Positive":
            classification = "Negative"
            normalized_compound = -abs(normalized_compound)

        # Stance classification (Tactical Intelligence)
        if any(w in text_lower for w in ["imminent", "collapse", "total blackout", "going 1000x"]):
            stance = "Sensational / Alarmist"
        elif any(w in text_lower for w in ["confirming", "advisory", "telemetry", "clarification", "neutralized"]):
            stance = "Authoritative / Factual"
        elif any(w in text_lower for w in ["analyzing", "notice how", "productivity", "disagree"]):
            stance = "Analytical / Discussion"
        else:
            stance = "General Public"

        # Supportive / Against classification
        supportive_signals = ["support", "agree", "solidarity", "stand with", "back", "endorse", "approve", "for", "yes", "correct"]
        against_signals = ["oppose", "against", "reject", "condemn", "ban", "stop", "wrong", "no", "fake", "lie", "corrupt"]

        support_count = sum(1 for w in supportive_signals if w in text_lower)
        against_count = sum(1 for w in against_signals if w in text_lower)

        if support_count > against_count:
            support_stance = "Supportive"
        elif against_count > support_count:
            support_stance = "Against"
        else:
            support_stance = "Neutral"

        return {
            "score": round(normalized_compound, 3),
            "classification": classification,
            "emotions": emotions,
            "stance": stance,
            "support_stance": support_stance,
            "sarcasm_score": sarcasm_score
        }

    def aggregate_by_topic(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate sentiment breakdown across identified topics."""
        topic_summary = {}
        for post in posts:
            topic = post.get("primary_topic", "General Discourse")
            sentiment = post.get("sentiment", {}).get("classification", "Neutral")
            score = post.get("sentiment", {}).get("score", 0.0)
            timestamp = post.get("timestamp", "")

            if topic not in topic_summary:
                topic_summary[topic] = {
                    "total": 0, "positive": 0, "negative": 0, "neutral": 0,
                    "avg_score": 0.0, "scores": [],
                    "supportive": 0, "against": 0,
                    "timeline": []
                }

            topic_summary[topic]["total"] += 1
            topic_summary[topic][sentiment.lower()] += 1
            topic_summary[topic]["scores"].append(score)

            # Support stance tally
            support_stance = post.get("sentiment", {}).get("support_stance", "Neutral")
            if support_stance == "Supportive":
                topic_summary[topic]["supportive"] += 1
            elif support_stance == "Against":
                topic_summary[topic]["against"] += 1

            # Timeline entry
            if timestamp:
                topic_summary[topic]["timeline"].append({
                    "t": timestamp[:10],  # date only
                    "score": score
                })

        for topic, data in topic_summary.items():
            if data["scores"]:
                data["avg_score"] = round(sum(data["scores"]) / len(data["scores"]), 3)
            del data["scores"]
            # Sort timeline
            data["timeline"].sort(key=lambda x: x["t"])

        return topic_summary

    def build_sentiment_timeline(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Build a chronological sentiment timeline across all posts.
        Returns list of {date, avg_score, positive_pct, negative_pct, dominant_emotion}
        """
        from collections import defaultdict
        daily = defaultdict(lambda: {"scores": [], "emotions": {}})

        for post in posts:
            ts = post.get("timestamp", "")[:10]
            if not ts:
                continue
            score = post.get("sentiment", {}).get("score", 0.0)
            daily[ts]["scores"].append(score)
            emotions = post.get("sentiment", {}).get("emotions", {})
            for emotion, val in emotions.items():
                daily[ts]["emotions"][emotion] = daily[ts]["emotions"].get(emotion, 0) + val

        timeline = []
        for date in sorted(daily.keys()):
            d = daily[date]
            scores = d["scores"]
            avg = round(sum(scores) / len(scores), 3) if scores else 0
            pos = sum(1 for s in scores if s > 0.15)
            neg = sum(1 for s in scores if s < -0.15)
            total = max(len(scores), 1)

            # Dominant emotion
            emo = d["emotions"]
            dominant = max(emo, key=emo.get) if emo else "neutral"

            timeline.append({
                "date": date,
                "avg_score": avg,
                "positive_pct": round(pos / total * 100, 1),
                "negative_pct": round(neg / total * 100, 1),
                "neutral_pct": round((total - pos - neg) / total * 100, 1),
                "dominant_emotion": dominant,
                "post_count": total
            })

        return timeline
