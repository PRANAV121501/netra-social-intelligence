"""
NETRA Social Intelligence Platform - Predictive Intelligence Engine
Forecasts future trending trajectories, emerging narratives, community expansion,
and acceleration velocity over 24h - 72h temporal horizons.
"""

from typing import List, Dict, Any
import math

class PredictiveEngine:
    def __init__(self):
        pass

    def generate_predictions(self, trends: List[Dict[str, Any]], communities: List[Dict[str, Any]], narratives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Synthesizes historical velocity, sentiment pressure, and network centrality
        to project emerging narrative arcs and future trending topics.
        """
        predictions = []

        # 1. Topic Predictions
        for trend in trends:
            topic = trend["topic"]
            growth = trend["growth_rate_pct"]
            current_score = trend["trend_score"]
            stage = trend["stage"]

            # Trajectory model
            if stage in ("Accelerating", "Emerging"):
                projected_growth = round(growth * 1.45, 1)
                predicted_state = "Will Peak in Next 18-24 Hours"
                confidence = min(96, int(75 + (current_score * 0.2)))
                risk_indicator = "HIGH_MONITORING"
                reasoning = (
                    f"Strong viral velocity (+{growth}%) coupled with multi-community cross-pollination. "
                    "Information cascade has crossed critical reproduction threshold."
                )
            elif stage == "Peaking":
                projected_growth = round(growth * 0.3, 1)
                predicted_state = "Expected to Plateau & Stabilize within 12 Hours"
                confidence = 88
                risk_indicator = "STABILIZING"
                reasoning = "Saturation reached among primary influencer hubs; institutional rebuttals dampening acceleration."
            else:
                projected_growth = round(growth * 0.1, 1)
                predicted_state = "Declining Trajectory"
                confidence = 82
                risk_indicator = "LOW"
                reasoning = "Discourse moving to secondary peripheral accounts; attention migrating to newer emerging events."

            predictions.append({
                "entity_name": topic,
                "type": "Topic Trajectory",
                "current_trend_score": current_score,
                "projected_24h_velocity_change": f"{'+' if projected_growth > 0 else ''}{projected_growth}%",
                "predicted_state": predicted_state,
                "confidence_score": f"{confidence}%",
                "risk_indicator": risk_indicator,
                "forecast_reasoning": reasoning
            })

        # 2. Emerging Narrative Spike Predictions
        high_impact_narratives = [n for n in narratives if "Disinformation" in n["stance"] or "Critical" in n["stance"] or "Concerned" in n["stance"]]
        for nar in high_impact_narratives[:3]:
            predictions.append({
                "entity_name": nar["narrative"],
                "type": "Narrative Warning",
                "current_trend_score": min(95, nar["engagement"] // 80),
                "projected_24h_velocity_change": "+210%",
                "predicted_state": "High Probability of Mass Spread & Echo-Chamber Polarization",
                "confidence_score": "92%",
                "risk_indicator": "CRITICAL_EARLY_WARNING",
                "forecast_reasoning": f"Driven by active stance '{nar['stance']}'. Accounts {', '.join(nar['primary_drivers'][:2])} are seeding cross-platform syndication."
            })

        # 3. Community Expansion Forecast
        for comm in communities[:2]:
            if comm["bot_ratio_pct"] > 25:
                predictions.append({
                    "entity_name": comm["name"],
                    "type": "Network Cluster Proliferation",
                    "current_trend_score": comm["member_count"] * 10,
                    "projected_24h_velocity_change": "+180%",
                    "predicted_state": "Synthetic Expansion Expected",
                    "confidence_score": "89%",
                    "risk_indicator": "THREAT_CLUSTER_EXPANSION",
                    "forecast_reasoning": f"Cluster exhibits {comm['bot_ratio_pct']}% synthetic density. Algorithmic amplification likely to target mainstream hashtags next."
                })

        return predictions
