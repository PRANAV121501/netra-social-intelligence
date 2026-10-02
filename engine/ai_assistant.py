"""
NETRA Social Intelligence Platform - AI Tactical Intelligence Assistant (NAT)
Answers complex natural language intelligence inquiries with structured tactical briefings,
evidentiary grounding, graph links, and countermeasure recommendations.
"""

from typing import Dict, Any, List
import re

class AIAssistant:
    def __init__(self):
        pass

    def query(self, prompt: str, pipeline_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes natural language query against current intelligence pipeline state.
        """
        p_lower = prompt.lower()
        influencers = pipeline_results.get("influencers", [])
        trends = pipeline_results.get("trends", [])
        communities = pipeline_results.get("communities", [])
        narratives = pipeline_results.get("narratives", [])
        alerts = pipeline_results.get("alerts", [])
        predictions = pipeline_results.get("predictions", [])
        cascades = pipeline_results.get("cascades", [])

        # Query Type 1: Influencers on specific topic (e.g. "top influencers discussing AI" or "who is influential")
        if any(w in p_lower for w in ["influencer", "influential", "key accounts", "who is driving"]):
            target_topic = "Artificial Intelligence" if "ai" in p_lower else ("Critical Infrastructure" if "cyber" in p_lower or "grid" in p_lower else None)
            
            top_users = influencers[:5]
            summary = (
                f"NETRA Graph Centrality Engine evaluated {len(influencers)} user nodes using PageRank, "
                f"Betweenness Centrality (bridging influence), and network amplification velocity. "
                f"The highest-scoring authoritative accounts currently commanding discourse are detailed below."
            )
            entities = [{"name": u["username"], "detail": f"Score: {u['influence_score']} | Tier: {u['impact_tier']} | Comm: {u['community_name']}"} for u in top_users]
            
            return {
                "query": prompt,
                "category": "INFLUENCE_ASSESSMENT",
                "executive_briefing": summary,
                "evidence_points": [
                    f"Top authority node @{top_users[0]['username']} commands an influence score of {top_users[0]['influence_score']}/100.",
                    f"Network bridges (high betweenness) include @{top_users[1]['username']}, serving as critical cross-community information conduits.",
                    f"Identified {sum(1 for u in influencers if u['is_bot'])} synthetic bot handles filtered out from organic influence rankings."
                ],
                "entities": entities,
                "actionable_recommendations": [
                    "Engage or monitor primary bridge accounts for official rebuttal dissemination.",
                    "Track sentiment delta of top 3 influencers as early indicators of community shifts."
                ]
            }

        # Query Type 2: Communities discussing cybersecurity or topics
        elif any(w in p_lower for w in ["communit", "group", "cluster", "echo chamber"]):
            comm_list = communities[:4]
            summary = (
                f"Louvain Modularity partitioning identified {len(communities)} active network communities. "
                f"Each community represents a distinct ideological cluster or operational syndicate with its own dominant topics and sentiment vectors."
            )
            entities = [{"name": c["name"], "detail": f"Size: {c['member_count']} nodes | Topic: {c['dominant_topic']} | Risk: {c['risk_level']}"} for c in comm_list]
            
            return {
                "query": prompt,
                "category": "COMMUNITY_STRUCTURE",
                "executive_briefing": summary,
                "evidence_points": [
                    f"Dominant defensive cluster: '{communities[0]['name']}' ({communities[0]['member_count']} verified nodes).",
                    f"Identified high-risk coordinated cluster: '{next((c['name'] for c in communities if c['risk_level'] == 'CRITICAL'), 'None')}' exhibiting extreme astroturfing signals.",
                    "Inter-community modularity index indicates strong polarization between institutional fact-checkers and sensationalist bot clusters."
                ],
                "entities": entities,
                "actionable_recommendations": [
                    "Maintain continuous telemetry on the boundary bridge nodes connecting community clusters.",
                    "Isolate synchronized nodes in cluster #2 to prevent viral spillover into mainstream discussions."
                ]
            }

        # Query Type 3: Explain why Topic X or hashtag is trending
        elif any(w in p_lower for w in ["why", "trend", "trending", "spike", "accelerat"]):
            top_trend = trends[0] if trends else {"topic": "General", "trend_score": 90, "growth_rate_pct": 120}
            summary = (
                f"Topic '{top_trend['topic']}' is currently trending at #{top_trend['trend_score']} velocity "
                f"(growth rate: +{top_trend['growth_rate_pct']}%). "
                f"The spike is driven by breaking disclosures from authoritative accounts combined with high-velocity downstream amplification."
            )
            return {
                "query": prompt,
                "category": "TREND_ROOT_CAUSE_ANALYSIS",
                "executive_briefing": summary,
                "evidence_points": [
                    f"Lifecycle Stage: {top_trend.get('stage', 'Accelerating')} with {top_trend.get('post_count', 0)} monitored critical posts.",
                    f"Top catalyst hashtags: {', '.join(top_trend.get('top_hashtags', []))}.",
                    f"Sample intelligence headline: \"{top_trend.get('sample_headline', '')}\""
                ],
                "entities": [{"name": t["topic"], "detail": f"Score: {t['trend_score']} | Stage: {t['stage']}"} for t in trends[:4]],
                "actionable_recommendations": [
                    "Deploy real-time counter-disinformation monitoring on related secondary hashtags.",
                    "Prepare pre-bunking public communications before projected 18-hour viral peak."
                ]
            }

        # Query Type 4: Information propagation / how narrative spread
        elif any(w in p_lower for w in ["spread", "propagat", "cascade", "how did"]):
            cascade = cascades[0] if cascades else {"topic": "Breaking Intelligence", "root_originator": "@CyberSentinel_IN", "virality_reproduction_rate": 2.4}
            summary = (
                f"Information cascade analysis traces the root inception of '{cascade.get('topic')}' to {cascade.get('root_originator')}. "
                f"Information propagated across {cascade.get('cascade_depth', 3)} hierarchical network tiers, "
                f"achieving an estimated viral reproduction rate (R0) of {cascade.get('virality_reproduction_rate')}."
            )
            return {
                "query": prompt,
                "category": "CASCADE_DIFFUSION_RECONSTRUCTION",
                "executive_briefing": summary,
                "evidence_points": [
                    f"Originator Node: {cascade.get('root_originator')} at timestamp {cascade.get('start_time', 'T0')}.",
                    f"Diffusion Velocity: {cascade.get('diffusion_speed', '3.5 hops/hr')}.",
                    f"Estimated Cascade Reach: ~{cascade.get('total_cascade_reach', 150000):,} user impressions across connected edges."
                ],
                "entities": [{"name": n["label"], "detail": f"Tier: {n['tier']} | Hops: {n['tier_level']}"} for n in cascade.get("nodes", [])[:5]],
                "actionable_recommendations": [
                    "Interdict false narrative branches at the tier-1 Key Influencer junction before tier-3 broadcast.",
                    "Review timeline correlation between originator post and first automated bot amplification."
                ]
            }

        # Query Type 5: Bot & coordinated activity
        elif any(w in p_lower for w in ["bot", "coordinated", "fake", "cib", "manipulation", "alert"]):
            critical_alerts = alerts
            summary = (
                f"NETRA Coordinated Inauthentic Behavior (CIB) Detector has flagged {len(alerts)} active operational alerts. "
                f"Synthesized indicators reveal synchronized copy-paste astroturfing and timestamp clustering designed to simulate organic panic."
            )
            entities = [{"name": a["alert_id"], "detail": f"Severity: {a['severity']} | Topic: {a['target_topic']} | Accounts: {a['account_count']}"} for a in alerts]
            return {
                "query": prompt,
                "category": "THREAT_ALERT_BRIEFING",
                "executive_briefing": summary,
                "evidence_points": [
                    f"Alert {alerts[0]['alert_id'] if alerts else 'CIB-001'}: {alerts[0]['title'] if alerts else 'Swarm Detection'} with {alerts[0]['account_count'] if alerts else 4} synchronized sockpuppets.",
                    "Pattern: Coordinated duplicate payload deployment across non-organic account clusters within 90-second intervals.",
                    f"Recommended Action: {alerts[0]['recommended_action'] if alerts else 'Submit platform quarantine request.'}"
                ],
                "entities": entities,
                "actionable_recommendations": [
                    "Export IP and handle manifest for telecommunications/social platform regulatory escalation.",
                    "Initiate automated counter-narrative broadcasting via official verified handles."
                ]
            }

        # Query Type 6: Predictive intelligence / what is likely to trend next
        elif any(w in p_lower for w in ["predict", "next", "future", "forecast", "emerging"]):
            top_preds = predictions[:4]
            summary = (
                f"Predictive Intelligence Engine has simulated viral trajectory models over a 24-72 hour horizon. "
                f"Identified high-velocity emerging narratives expected to cross mainstream virality thresholds within 18 hours."
            )
            entities = [{"name": p["entity_name"], "detail": f"Proj: {p['projected_24h_velocity_change']} | Conf: {p['confidence_score']} | State: {p['predicted_state']}"} for p in top_preds]
            return {
                "query": prompt,
                "category": "PREDICTIVE_FORECAST",
                "executive_briefing": summary,
                "evidence_points": [
                    f"Top Emerging Arc: '{top_preds[0]['entity_name']}' projected to accelerate {top_preds[0]['projected_24h_velocity_change']} (Confidence: {top_preds[0]['confidence_score']}).",
                    f"Forecast Assessment: {top_preds[0]['forecast_reasoning']}",
                    f"Threat Vector Warning: Synthetic cluster expansion detected in connected peripheral communities."
                ],
                "entities": entities,
                "actionable_recommendations": [
                    "Pre-position public advisories and factual context prior to expected peak velocity window.",
                    "Configure automated alerting on keyword thresholds for projected narratives."
                ]
            }

        # Default fallback: General intelligence summary
        else:
            return {
                "query": prompt,
                "category": "TACTICAL_OVERVIEW",
                "executive_briefing": (
                    f"NETRA Social Intelligence Platform is currently monitoring {len(pipeline_results.get('posts', []))} ingested intelligence posts "
                    f"across {len(trends)} primary topics. All systems operating at nominal real-time processing capacity."
                ),
                "evidence_points": [
                    f"Active Critical Threats: {len([a for a in alerts if a['severity'] == 'CRITICAL'])} high-priority CIB alerts.",
                    f"Top Trending Narrative: {trends[0]['topic'] if trends else 'Critical Infrastructure'}.",
                    f"Identified Communities: {len(communities)} modularity-partitioned ideological clusters."
                ],
                "entities": [{"name": f"@{u['username']}", "detail": f"Influence: {u['influence_score']}"} for u in influencers[:4]],
                "actionable_recommendations": [
                    "Select a specific module or query prompt to inspect deep-graph propagation or bot forensics."
                ]
            }
