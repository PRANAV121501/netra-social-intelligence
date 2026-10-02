"""
NETRA Social Intelligence Platform - Entity Extraction Engine
Extracts Usernames, Hashtags, Organizations, Locations, Topics, Mentions, and URLs.
Combines spaCy Named Entity Recognition (NER) with regex & curated tactical catalogs.
"""

import re
from typing import Dict, List, Any

KNOWN_ORGS = {
    "CERT-In": "Cyber Emergency Response Team (India)",
    "NCIIPC": "National Critical Information Infrastructure Protection Centre",
    "ISRO": "Indian Space Research Organisation",
    "DRDO": "Defence Research and Development Organisation",
    "SEBI": "Securities and Exchange Board of India",
    "RBI": "Reserve Bank of India",
    "OpenAI": "AI Frontier Lab",
    "Google": "Global Tech Entity",
    "Microsoft": "Global Tech Entity",
    "PIB": "Press Information Bureau"
}

KNOWN_LOCATIONS = {
    "New Delhi": {"lat": 28.6139, "lon": 77.2090, "country": "India"},
    "Delhi": {"lat": 28.7041, "lon": 77.1025, "country": "India"},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "country": "India"},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946, "country": "India"},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "country": "India"},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "country": "India"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "country": "India"}
}

TOPIC_KEYWORDS = {
    "IndiaAI": ["indiaai", "digitalindia", "ai strategy", "artificial intelligence", "frontier models", "tutor", "autonomous"],
    "CyberSecurity": ["cybersecurity", "infosec", "vulnerability", "breach", "scada", "telemetry", "cert-in", "ddos", "panic", "outage"],
    "StockRally": ["stockrally", "nifty", "sensex", "dalalstreet", "finance", "markets", "bullish", "fii", "investments"],
    "NationalSecurity": ["nationalsecurity", "defense", "border", "surveillance", "makeinindia", "drdo", "electronic warfare"],
    "ClimateAction": ["climateaction", "greenenergy", "renewable", "solar", "sustainability", "coastal", "environmental"],
    "Policy & Governance": ["policy", "governance", "regulation", "initiatives", "government", "parliament"],
    "Tech Startups": ["startups", "ecosystem", "innovation", "seed", "venture", "founders"]
}

_NLP = None

def get_spacy_nlp():
    global _NLP
    if _NLP is None:
        try:
            import spacy
            _NLP = spacy.load("en_core_web_sm")
        except Exception:
            _NLP = False
    return _NLP if _NLP else None


class EntityExtractor:
    def __init__(self):
        self.url_regex = re.compile(r'https?://\S+|www\.\S+')
        self.hashtag_regex = re.compile(r'#(\w+)')
        self.mention_regex = re.compile(r'@(\w+)')
        self.nlp = get_spacy_nlp()

    def extract(self, text: str, declared_location: str = None) -> Dict[str, Any]:
        urls = self.url_regex.findall(text)
        hashtags = self.hashtag_regex.findall(text)
        mentions = self.mention_regex.findall(text)

        orgs = set()
        locations = set()

        for org in KNOWN_ORGS:
            if re.search(r'\b' + re.escape(org) + r'\b', text, re.IGNORECASE):
                orgs.add(org)

        for loc in KNOWN_LOCATIONS:
            if re.search(r'\b' + re.escape(loc) + r'\b', text, re.IGNORECASE):
                locations.add(loc)

        if declared_location:
            for loc in KNOWN_LOCATIONS:
                if loc.lower() in declared_location.lower():
                    locations.add(loc)

        if self.nlp:
            clean_text = self.url_regex.sub('', text)
            doc = self.nlp(clean_text)
            for ent in doc.ents:
                if ent.label_ == "ORG" and len(ent.text) > 2:
                    if ent.text not in orgs and not ent.text.startswith(('#', '@')):
                        orgs.add(ent.text)
                elif ent.label_ in ("GPE", "LOC") and len(ent.text) > 2:
                    if ent.text not in locations and not ent.text.startswith(('#', '@')):
                        locations.add(ent.text)

        assigned_topics = []
        text_lower = text.lower()
        for topic_name, keywords in TOPIC_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                assigned_topics.append({"topic": topic_name, "relevance": score})

        assigned_topics.sort(key=lambda x: x["relevance"], reverse=True)
        primary_topic = assigned_topics[0]["topic"] if assigned_topics else "IndiaAI"

        return {
            "hashtags": [f"#{tag}" for tag in hashtags],
            "mentions": [f"@{m}" for m in mentions],
            "organizations": list(orgs),
            "locations": list(locations),
            "urls": urls,
            "topics": [t["topic"] for t in assigned_topics],
            "primary_topic": primary_topic
        }
