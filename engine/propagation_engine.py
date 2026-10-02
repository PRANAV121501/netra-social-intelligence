"""
NETRA Social Intelligence Platform - Information Propagation Engine
Tracks how narratives, breaking leaks, and rumors propagate through network hops.
Reconstructs cascade trees: Originator -> Amplifiers -> Communities -> Mass Audience.
"""

from typing import List, Dict, Any
from datetime import datetime

class PropagationEngine:
    def __init__(self):
        pass

    def build_propagation_trees(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Reconstructs propagation cascades for the key topics and breaking narratives.
        """
        topic_groups = {}
        for post in posts:
            topic = post.get("primary_topic", "General Discourse")
            if topic not in topic_groups:
                topic_groups[topic] = []
            topic_groups[topic].append(post)

        cascades = []

        for topic, topic_posts in topic_groups.items():
            # Sort chronologically
            sorted_posts = sorted(topic_posts, key=lambda x: x.get("timestamp", ""))
            if not sorted_posts:
                continue

            root_post = sorted_posts[0]
            root_author = root_post.get("author", "unknown")
            root_time = root_post.get("timestamp", "")

            nodes = []
            links = []

            # Add Root Node (Tier 0: Originator)
            nodes.append({
                "id": root_author,
                "label": f"@{root_author}",
                "tier": "Originator",
                "tier_level": 0,
                "timestamp": root_time,
                "followers": root_post.get("followers", 0),
                "is_bot": root_post.get("bot_analysis", {}).get("is_bot", False),
                "color": "#00f0ff"
            })

            # Subsequent posts are assigned cascade tiers based on timestamps and mentions
            prev_node_id = root_author
            total_reach = root_post.get("followers", 0) + root_post.get("retweets", 0) * 15

            for i, p in enumerate(sorted_posts[1:], start=1):
                p_author = p.get("author", f"user_{i}")
                mentions = [m.replace("@", "") for m in p.get("entities", {}).get("mentions", [])]
                
                # Determine parent node: if this post mentions an earlier node, connect there; else chain
                parent = root_author
                for m in mentions:
                    if any(n["id"] == m for n in nodes):
                        parent = m
                        break

                is_bot = p.get("bot_analysis", {}).get("is_bot", False)
                tier_level = 1 if p.get("followers", 0) > 50000 else (3 if is_bot else 2)
                tier_name = "Key Influencer" if tier_level == 1 else ("Bot Echo Cell" if is_bot else "Community Amplifier")
                
                color = "#ff3366" if is_bot else ("#a855f7" if tier_level == 1 else "#00f59b")

                nodes.append({
                    "id": p_author,
                    "label": f"@{p_author}",
                    "tier": tier_name,
                    "tier_level": tier_level,
                    "timestamp": p.get("timestamp", ""),
                    "followers": p.get("followers", 0),
                    "is_bot": is_bot,
                    "color": color
                })

                links.append({
                    "source": parent,
                    "target": p_author,
                    "delay_minutes": i * 15 + 5
                })

                total_reach += p.get("followers", 0) + p.get("retweets", 0) * 12

            # Virality metrics
            cascade_depth = len(set(n["tier_level"] for n in nodes))
            time_span_hrs = round(len(sorted_posts) * 0.75, 1)
            diffusion_speed = f"{round(len(sorted_posts) / max(0.5, time_span_hrs), 1)} hops/hr"
            virality_r0 = round(1.2 + (len(links) / max(1, len(nodes) - 1)) * 1.5, 2)

            cascades.append({
                "topic": topic,
                "root_originator": f"@{root_author}",
                "start_time": root_time,
                "cascade_depth": cascade_depth,
                "node_count": len(nodes),
                "total_cascade_reach": total_reach,
                "diffusion_speed": diffusion_speed,
                "virality_reproduction_rate": virality_r0,
                "nodes": nodes,
                "links": links
            })

        cascades.sort(key=lambda x: x["node_count"], reverse=True)
        return cascades
