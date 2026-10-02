"""
Test suite for NETRA Social Intelligence Platform Master Pipeline.
"""

import json
from engine.pipeline import IntelligencePipeline

def main():
    with open("data/sample_social_stream.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    pipeline = IntelligencePipeline()
    results = pipeline.run(posts)

    print("Pipeline run SUCCESS!")
    print(f"Total posts: {results['summary_kpis']['total_posts']}")
    print(f"Total entities: {results['summary_kpis']['total_entities_extracted']}")
    print(f"Active communities: {results['summary_kpis']['active_communities']}")
    print(f"Critical alerts: {results['summary_kpis']['critical_threat_alerts']}")
    print(f"Graph nodes: {results['summary_kpis']['knowledge_graph_nodes']}, edges: {results['summary_kpis']['knowledge_graph_edges']}")
    
    print("\nTop Trends:")
    for t in results["trends"][:3]:
        print(f" - {t['topic']}: Score {t['trend_score']} | Stage: {t['stage']}")

    print("\nTop Influencers:")
    for u in results["influencers"][:3]:
        print(f" - @{u['username']}: Score {u['influence_score']} | Tier: {u['impact_tier']}")

    print("\nNarrative count:", len(results["narratives"]))
    print("Alerts count:", len(results["alerts"]))
    print("Predictions count:", len(results["predictions"]))

    # Test AI Assistant query
    ai_resp = pipeline.answer_query("Show top influencers discussing AI")
    print("\nAI Assistant Query Result Category:", ai_resp.get("category"))
    print("AI Assistant Executive Briefing:", ai_resp.get("executive_briefing")[:120], "...")

    # Test Path finding
    source = "CyberSentinel_IN"
    target = "PIB_FactCheck"
    path = pipeline.find_path(source, target)
    print(f"\nPath from {source} to {target}:", " -> ".join(path))

if __name__ == "__main__":
    main()
