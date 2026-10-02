"""
NETRA Social Intelligence Platform - High-Volume Dataset Generator
Generates realistic multi-domain social media streams for SIH demonstration
(Cybersecurity & Disinformation, AI & Tech Policy, Financial Market Manipulation,
Geopolitical Defense, and Public Health Bio-surveillance).
"""

import json
import random
from datetime import datetime, timedelta

TOPICS = [
    {
        "name": "Critical Infrastructure & Cyber Defense",
        "hashtags": ["#GridBreach", "#CyberSecurity", "#SCADA", "#CERTIn", "#NationalSecurity"],
        "locations": ["New Delhi", "Mumbai", "Bengaluru", "Pune"],
        "orgs": ["CERT-In", "NCIIPC", "DRDO"],
        "templates": [
            ("CyberSentinel_IN", "CRITICAL ADVISORY: Targeted spear-phishing probes detected against SCADA distribution links in {loc}. IOCs correlated with state actor threat group. #GridBreach #CyberSecurity", True),
            ("PowerGrid_Ops", "Automated safety firewalls isolated substation circuits in {loc}. Telemetry integrity 100% verified. Zero power disruption. #GridBreach #SCADA", True),
            ("bot_echo_{id}", "TOTAL BLACKOUT IMMINENT!! Power grid collapsing across {loc}! Withdraw your cash and buy fuel now before shutdown! #GridBreach #Panic", False),
            ("PIB_FactCheck", "FACT CHECK: Reports of nationwide power outages in {loc} are completely fabricated by coordinated bot networks. Power grid operating nominally. #FakeNewsBusted #GridBreach", True),
            ("TechJournalist_{id}", "Forensic packet analysis shows how panic disinfo swarms deployed copy-pasted alarmist narratives 15 minutes after the initial {loc} alert. #CognitiveWarfare", False)
        ]
    },
    {
        "name": "Artificial Intelligence & Future of Work",
        "hashtags": ["#ArtificialIntelligence", "#FutureOfWork", "#AIRegulation", "#EdTech", "#OpenSource"],
        "locations": ["Bengaluru", "San Francisco", "London", "Geneva"],
        "orgs": ["OpenAI", "Google", "UNESCO", "European Commission"],
        "templates": [
            ("Aravind_AI", "Next-gen code intelligence models in {loc} are cutting developer cycle times by 70%. Urgent need for engineering curriculum revamps. #ArtificialIntelligence #FutureOfWork", True),
            ("EdTechLead_{id}", "Deploying multilingual generative AI tutors across rural secondary schools. Learning engagement up 3.4x. #EdTech #Innovation", False),
            ("PolicyFellow_{id}", "European Commission and UNESCO ratifying binding treaty standards for sovereign frontier models in {loc}. Algorithmic transparency mandatory. #AIRegulation", True),
            ("OpenSourceDev_{id}", "Centralized tech monopolies are lobbying for restrictive AI licensing under the guise of safety. Open weights are critical for digital autonomy! #OpenSource", False)
        ]
    },
    {
        "name": "Financial Integrity & Market Surveillance",
        "hashtags": ["#MarketManipulation", "#FinSec", "#Crypto", "#SEBI", "#ScamAlert"],
        "locations": ["Mumbai", "Singapore", "London"],
        "orgs": ["SEBI", "RBI"],
        "templates": [
            ("SEBI_OfficialWatcher", "NOTICE: Coordinated astroturfing campaigns detected pumping synthetic penny tokens. Surveillance systems monitoring promotional handle syndicates in {loc}. #SEBI #MarketIntegrity", True),
            ("pump_bot_{id}", "🚀🚀 $CYNX TOKEN IS GOING TO THE MOON! BUY NOW ON DEX BEFORE 500X LISTING TONIGHT!! DON'T MISS OUT! #Crypto #MoonGains", False),
            ("FinSecAnalyst_{id}", "Telemetry identifies synchronized bot swarm deploying duplicate shill posts for $CYNX originating from VPN proxies. Retail alert. #FinSec", False)
        ]
    }
]

def generate_stream(count=120):
    posts = []
    base_time = datetime.utcnow() - timedelta(hours=8)

    for i in range(1, count + 1):
        topic_info = random.choice(TOPICS)
        template = random.choice(topic_info["templates"])
        author_tmpl, content_tmpl, is_verified = template

        author = author_tmpl.format(id=f"{random.randint(10, 99)}")
        loc = random.choice(topic_info["locations"])
        content = content_tmpl.format(loc=loc, id=f"{random.randint(10, 99)}")
        
        post_time = base_time + timedelta(minutes=int(i * (480 / count)))
        is_bot = author.startswith(("bot_", "pump_bot"))
        followers = random.randint(10, 75) if is_bot else (random.randint(45000, 320000) if is_verified else random.randint(1500, 28000))
        following = random.randint(1800, 3500) if is_bot else random.randint(100, 900)

        posts.append({
            "id": f"post_gen_{i:04d}",
            "author": author,
            "author_name": author if is_bot else f"{author} (Verified Intel)",
            "content": content,
            "timestamp": post_time.isoformat() + "Z",
            "likes": random.randint(2, 45) if is_bot else random.randint(120, 5600),
            "retweets": random.randint(120, 680) if is_bot else random.randint(40, 2400),
            "replies": random.randint(5, 40) if is_bot else random.randint(15, 450),
            "followers": followers,
            "following": following,
            "account_created": "2026-09-22" if is_bot else "2018-05-14",
            "location": loc,
            "verified": is_verified,
            "urls": []
        })

    return posts

if __name__ == "__main__":
    stream = generate_stream(150)
    with open("data/expanded_social_stream.json", "w", encoding="utf-8") as f:
        json.dump(stream, f, indent=2)
    print(f"Successfully generated {len(stream)} high-volume simulated social media intelligence posts!")
