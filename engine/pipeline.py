"""
NETRA Social Intelligence Platform - Master Intelligence Pipeline
Coordinates the complete end-to-end intelligence workflow:
Social Media Dataset -> Entity Extraction -> Sentiment Analysis -> Topic Detection
-> Community Detection -> Influence Analysis -> Information Propagation Analysis
-> Graph Intelligence -> Bot/CIB Detection -> Predictive Analytics -> Tactical Briefings.
"""

from typing import List, Dict, Any
import json
import os

from engine.entity_extractor import EntityExtractor
from engine.sentiment_engine import SentimentEngine
from engine.topic_engine import TopicEngine
from engine.narrative_engine import NarrativeEngine
from engine.graph_engine import GraphEngine
from engine.propagation_engine import PropagationEngine
from engine.bot_detection import BotDetector
from engine.predictive_engine import PredictiveEngine
from engine.ai_assistant import AIAssistant

class IntelligencePipeline:
    def __init__(self):
        self.entity_extractor = EntityExtractor()
        self.sentiment_engine = SentimentEngine()
        self.topic_engine = TopicEngine()
        self.narrative_engine = NarrativeEngine()
        self.graph_engine = GraphEngine()
        self.propagation_engine = PropagationEngine()
        self.bot_detector = BotDetector()
        self.predictive_engine = PredictiveEngine()
        self.ai_assistant = AIAssistant()

    def run(self, raw_posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes the 10-stage intelligence transformation on input posts.
        """
        processed_posts = []

        # Stage 1 & 2: Entity Extraction, Bot Scoring, Sentiment Scoring per post
        for post in raw_posts:
            p = dict(post)
            # Bot scoring
            bot_info = self.bot_detector.evaluate_account(p)
            p["bot_analysis"] = bot_info

            # Entity extraction
            entities = self.entity_extractor.extract(p.get("content", ""), p.get("location"))
            p["entities"] = entities
            p["primary_topic"] = entities["primary_topic"]

            # Sentiment & Emotion classification
            sentiment_info = self.sentiment_engine.analyze_post(p.get("content", ""))
            p["sentiment"] = sentiment_info

            processed_posts.append(p)

        # Stage 3: Sentiment Aggregation by Topic
        topic_sentiment = self.sentiment_engine.aggregate_by_topic(processed_posts)

        # Stage 4: Topic & Trend Detection
        trends = self.topic_engine.detect_trends(processed_posts)

        # Stage 5: Sub-Narrative Detection & Stance Mapping
        narratives = self.narrative_engine.detect_narratives(processed_posts)

        # Stage 6: Graph Intelligence, Centrality & Louvain Community Detection
        graph_data = self.graph_engine.build_graph(processed_posts)

        # Stage 7: Information Propagation Cascades
        cascades = self.propagation_engine.build_propagation_trees(processed_posts)

        # Stage 8: Bot Swarm & Coordinated Inauthentic Behavior (CIB) Detection
        alerts = self.bot_detector.detect_coordinated_campaigns(processed_posts)

        # Stage 9: Predictive Intelligence (24-72h Trajectory & Early Warnings)
        predictions = self.predictive_engine.generate_predictions(
            trends=trends, 
            communities=graph_data["communities"], 
            narratives=narratives
        )

        # Global KPIs & Entity Rollups
        all_hashtags = []
        all_mentions = []
        all_orgs = []
        all_locs = []
        for p in processed_posts:
            all_hashtags.extend(p["entities"]["hashtags"])
            all_mentions.extend(p["entities"]["mentions"])
            all_orgs.extend(p["entities"]["organizations"])
            all_locs.extend(p["entities"]["locations"])

        from collections import Counter
        top_hashtags = [{"name": tag, "count": count} for tag, count in Counter(all_hashtags).most_common(12)]
        top_orgs = [{"name": org, "count": count} for org, count in Counter(all_orgs).most_common(10)]
        top_locations = [{"name": loc, "count": count} for loc, count in Counter(all_locs).most_common(10)]

        # Geolocation points for Leaflet map
        from engine.entity_extractor import KNOWN_LOCATIONS
        geo_points = []
        loc_counter = Counter(all_locs)
        for loc_name, count in loc_counter.items():
            if loc_name in KNOWN_LOCATIONS:
                coord = KNOWN_LOCATIONS[loc_name]
                geo_points.append({
                    "city": loc_name,
                    "country": coord["country"],
                    "lat": coord["lat"],
                    "lon": coord["lon"],
                    "volume": count * 35 + 10,
                    "threat_level": "ELEVATED" if count > 2 else "NORMAL"
                })

        # Assemble Master Intelligence Response
        results = {
            "summary_kpis": {
                "total_posts": len(processed_posts),
                "total_entities_extracted": len(all_hashtags) + len(all_mentions) + len(all_orgs) + len(all_locs),
                "active_communities": len(graph_data["communities"]),
                "critical_threat_alerts": sum(1 for a in alerts if a["severity"] == "CRITICAL"),
                "bot_accounts_quarantined": sum(1 for p in processed_posts if p["bot_analysis"]["is_bot"]),
                "knowledge_graph_nodes": graph_data["node_count"],
                "knowledge_graph_edges": graph_data["edge_count"],
                "viral_reproduction_index": cascades[0]["virality_reproduction_rate"] if cascades else 1.5
            },
            "posts": processed_posts,
            "trends": trends,
            "topic_sentiment": topic_sentiment,
            "narratives": narratives,
            "influencers": graph_data["influencers"],
            "communities": graph_data["communities"],
            "knowledge_graph": {
                "nodes": graph_data["vis_nodes"],
                "edges": graph_data["vis_edges"]
            },
            "cascades": cascades,
            "alerts": alerts,
            "predictions": predictions,
            "entities": {
                "top_hashtags": top_hashtags,
                "top_organizations": top_orgs,
                "top_locations": top_locations
            },
            "geo_points": geo_points
        }

        # Cache internal graph for path finder queries
        self._last_graph = graph_data["graph"]
        self._last_results = results

        return results

    def answer_query(self, prompt: str) -> Dict[str, Any]:
        """
        Executes an AI intelligence inquiry against the pipeline state.
        """
        if not hasattr(self, "_last_results") or self._last_results is None:
            return {"error": "Pipeline has not run yet"}
        return self.ai_assistant.query(prompt, self._last_results)

    def find_path(self, source: str, target: str) -> List[str]:
        """
        Finds shortest graph intelligence connection path.
        """
        if not hasattr(self, "_last_graph") or self._last_graph is None:
            return []
        return self.graph_engine.find_shortest_path(self._last_graph, source, target)
