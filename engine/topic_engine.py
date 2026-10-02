"""
NETRA Social Intelligence Platform - Trend Detection Engine
Calculates trend scores, velocity, acceleration, growth rates, and lifecycle stages
(Emerging, Accelerating, Peaking, Stabilizing, Decaying).
"""

from typing import List, Dict, Any
from collections import Counter
from datetime import datetime

class TopicEngine:
    def __init__(self):
        pass

    def detect_trends(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculates trend metrics per topic based on volume, engagement, and temporal velocity.
        """
        topic_groups = {}
        for post in posts:
            topic = post.get("primary_topic", "General Discourse")
            if topic not in topic_groups:
                topic_groups[topic] = []
            topic_groups[topic].append(post)

        trends = []
        for topic, topic_posts in topic_groups.items():
            post_count = len(topic_posts)
            total_likes = sum(p.get("likes", 0) for p in topic_posts)
            total_shares = sum(p.get("retweets", 0) for p in topic_posts)
            total_engagement = total_likes + total_shares * 2

            # Temporal sorting
            sorted_posts = sorted(topic_posts, key=lambda x: x.get("timestamp", ""))
            
            # Sub-divide into earlier half vs recent half to detect velocity acceleration
            mid_point = max(1, len(sorted_posts) // 2)
            earlier = sorted_posts[:mid_point]
            recent = sorted_posts[mid_point:]

            recent_eng = sum(p.get("likes", 0) + p.get("retweets", 0) * 2 for p in recent)
            earlier_eng = sum(p.get("likes", 0) + p.get("retweets", 0) * 2 for p in earlier) or 1

            growth_rate = round(((recent_eng - earlier_eng) / earlier_eng) * 100, 1)

            # Trend score composite: volume + engagement factor + growth rate bonus
            base_score = post_count * 12 + (total_engagement / 500)
            trend_score = min(100.0, round(base_score * (1 + max(0, growth_rate) / 100), 1))

            # Lifecycle Stage determination
            if growth_rate > 150:
                stage = "Accelerating"
                status_color = "#00f0ff"
            elif growth_rate > 50:
                stage = "Emerging"
                status_color = "#00f59b"
            elif growth_rate > -10:
                stage = "Peaking"
                status_color = "#ffb703"
            else:
                stage = "Decaying"
                status_color = "#8d93a3"

            # Top hashtags associated
            hashtags = []
            for p in topic_posts:
                hashtags.extend(p.get("entities", {}).get("hashtags", []))
            top_hashtags = [tag for tag, _ in Counter(hashtags).most_common(4)]

            trends.append({
                "topic": topic,
                "trend_score": trend_score,
                "post_count": post_count,
                "total_engagement": total_engagement,
                "growth_rate_pct": growth_rate,
                "stage": stage,
                "status_color": status_color,
                "top_hashtags": top_hashtags,
                "sample_headline": sorted_posts[-1].get("content", "")[:120] + "..."
            })

        trends.sort(key=lambda x: x["trend_score"], reverse=True)
        return trends
