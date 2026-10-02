"""
NETRA Social Intelligence Platform - Graph Intelligence Engine
Constructs multi-relational Knowledge Graphs (Users, Topics, Hashtags, Organizations, Locations, Communities).
Executes PageRank, Betweenness Centrality, Degree Centrality, Louvain Community Detection, and Shortest-Path tracing.
"""

from typing import List, Dict, Any, Tuple
import networkx as nx
from collections import Counter, defaultdict

COMMUNITY_METADATA = {
    0: {"name": "Cyber Defense & National Security Core", "color": "#00f0ff", "archetype": "Government / Defensive"},
    1: {"name": "AI Researchers & Tech Policy Syndicate", "color": "#a855f7", "archetype": "Academia / Industry"},
    2: {"name": "Synchronized Bot & Disinformation Swarm", "color": "#ff3366", "archetype": "Coordinated Inauthentic"},
    3: {"name": "Public Health & Sovereign Scientific Advisory", "color": "#00f59b", "archetype": "Advisory / Institutional"},
    4: {"name": "Market Regulators & FinSec Watchdogs", "color": "#ffb703", "archetype": "Financial Regulatory"},
    5: {"name": "Open-Source & Civil Liberties Advocates", "color": "#38bdf8", "archetype": "Civil Society"}
}

def compute_pagerank(G: nx.DiGraph, alpha: float = 0.85, max_iter: int = 100, tol: float = 1e-6) -> Dict[str, float]:
    """
    Robust pure-Python / numpy power-iteration PageRank with zero scipy dependency.
    """
    nodes = list(G.nodes())
    N = len(nodes)
    if N == 0:
        return {}
    scores = {n: 1.0 / N for n in nodes}
    for _ in range(max_iter):
        next_scores = {n: (1.0 - alpha) / N for n in nodes}
        dangling_sum = sum(scores[n] for n in nodes if G.out_degree(n) == 0)
        dangling_contrib = alpha * dangling_sum / N
        for n in nodes:
            next_scores[n] += dangling_contrib
            out_deg = G.out_degree(n)
            if out_deg > 0:
                out_share = alpha * scores[n] / out_deg
                for nbr in G.successors(n):
                    next_scores[nbr] += out_share
        err = sum(abs(next_scores[n] - scores[n]) for n in nodes)
        scores = next_scores
        if err < tol:
            break
    return scores

class GraphEngine:
    def __init__(self):
        pass

    def build_graph(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds a comprehensive heterogeneous Knowledge Graph from processed posts.
        """
        G = nx.DiGraph()
        user_interaction_graph = nx.Graph()

        # Step 1: Collect entities and interactions
        for post in posts:
            author = post["author"]
            author_label = post.get("author_name", author)
            topic = post.get("primary_topic", "General Discourse")
            location = post.get("entities", {}).get("locations", [])
            orgs = post.get("entities", {}).get("organizations", [])
            hashtags = post.get("entities", {}).get("hashtags", [])
            mentions = post.get("entities", {}).get("mentions", [])
            is_bot = post.get("bot_analysis", {}).get("is_bot", False)

            # Add Author Node
            if not G.has_node(author):
                G.add_node(author, 
                           type="user", 
                           label=f"@{author}", 
                           title=f"{author_label} ({author})",
                           followers=post.get("followers", 0),
                           verified=post.get("verified", False),
                           is_bot=is_bot)
            user_interaction_graph.add_node(author)

            # Add Topic Node
            if not G.has_node(topic):
                G.add_node(topic, type="topic", label=topic, title=f"Topic: {topic}")
            G.add_edge(author, topic, relation="DISCUSSES", weight=1.0)

            # Add Location Nodes
            for loc in location:
                if not G.has_node(loc):
                    G.add_node(loc, type="location", label=loc, title=f"Location: {loc}")
                G.add_edge(author, loc, relation="LOCATED_IN", weight=1.0)

            # Add Organization Nodes
            for org in orgs:
                if not G.has_node(org):
                    G.add_node(org, type="organization", label=org, title=f"Organization: {org}")
                G.add_edge(author, org, relation="AFFILIATED_OR_TARGETS", weight=1.0)

            # Add Hashtag Nodes
            for tag in hashtags:
                if not G.has_node(tag):
                    G.add_node(tag, type="hashtag", label=tag, title=f"Hashtag: {tag}")
                G.add_edge(author, tag, relation="USES_TAG", weight=1.0)

            # Add Mention Edges
            for m in mentions:
                clean_m = m.replace("@", "")
                if not G.has_node(clean_m):
                    G.add_node(clean_m, type="user", label=f"@{clean_m}", title=f"User: {clean_m}", followers=1000)
                user_interaction_graph.add_node(clean_m)
                G.add_edge(author, clean_m, relation="MENTIONS", weight=2.0)
                user_interaction_graph.add_edge(author, clean_m, weight=2.0)

        # Connect synchronized bot accounts directly in interaction graph
        bot_users = [p["author"] for p in posts if p.get("bot_analysis", {}).get("is_bot", False)]
        for i in range(len(bot_users)):
            for j in range(i + 1, len(bot_users)):
                u1, u2 = bot_users[i], bot_users[j]
                user_interaction_graph.add_edge(u1, u2, weight=3.0)
                G.add_edge(u1, u2, relation="COORDINATED_WITH", weight=3.0)

        # Step 2: Louvain Community Detection on User Interaction Subgraph
        user_communities = {}
        try:
            communities = list(nx.community.louvain_communities(user_interaction_graph, seed=42))
            for comm_id, comm_nodes in enumerate(communities):
                for node in comm_nodes:
                    user_communities[node] = comm_id
        except Exception:
            # Fallback connected components
            for comm_id, comp in enumerate(nx.connected_components(user_interaction_graph)):
                for node in comp:
                    user_communities[node] = comm_id % 6

        # Step 3: Centrality Metrics (PageRank, Betweenness, In-Degree)
        pagerank = compute_pagerank(G)
        undirected_G = G.to_undirected()
        betweenness = nx.betweenness_centrality(undirected_G, weight="weight")

        # Step 4: Extract Influence Leaderboard for Users
        influencers = []
        user_nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "user"]

        for u in user_nodes:
            pr = pagerank.get(u, 0.0)
            bw = betweenness.get(u, 0.0)
            in_deg = G.in_degree(u) if G.has_node(u) else 0
            node_data = G.nodes[u]
            followers = node_data.get("followers", 0)
            is_bot = node_data.get("is_bot", False)

            # Composite Influence Score (0 - 100)
            bot_penalty = 0.2 if is_bot else 1.0
            raw_influence = (pr * 500 + bw * 300 + min(20, in_deg * 3) + min(25, followers / 10000)) * bot_penalty
            influence_score = min(100.0, max(5.0, round(raw_influence, 1)))

            comm_id = user_communities.get(u, 0)
            comm_meta = COMMUNITY_METADATA.get(comm_id, {"name": f"Community #{comm_id}", "color": "#8d93a3"})

            influencers.append({
                "username": u,
                "display_name": node_data.get("label", f"@{u}"),
                "influence_score": influence_score,
                "pagerank": round(pr, 4),
                "betweenness": round(bw, 4),
                "in_degree": in_deg,
                "followers": followers,
                "community_id": comm_id,
                "community_name": comm_meta["name"],
                "is_bot": is_bot,
                "impact_tier": "Alpha Influencer" if influence_score > 75 else ("Key Amplifier" if influence_score > 45 else "Periphery Node")
            })

        influencers.sort(key=lambda x: x["influence_score"], reverse=True)

        # Step 5: Format Communities summary
        community_summary = []
        comm_user_map = defaultdict(list)
        for u, cid in user_communities.items():
            comm_user_map[cid].append(u)

        for cid, members in comm_user_map.items():
            meta = COMMUNITY_METADATA.get(cid, {"name": f"Syndicate Cluster {cid}", "color": "#00f0ff", "archetype": "Discourse Group"})
            
            comm_topics = []
            for m in members:
                for target in G.successors(m):
                    if G.nodes[target].get("type") == "topic":
                        comm_topics.append(target)
            dom_topic = Counter(comm_topics).most_common(1)[0][0] if comm_topics else "General Discourse"

            bot_count = sum(1 for m in members if G.nodes[m].get("is_bot", False))
            bot_ratio = round((bot_count / max(1, len(members))) * 100, 1)

            community_summary.append({
                "community_id": cid,
                "name": meta["name"],
                "color": meta["color"],
                "archetype": meta["archetype"],
                "member_count": len(members),
                "members": members[:8],
                "dominant_topic": dom_topic,
                "bot_ratio_pct": bot_ratio,
                "risk_level": "CRITICAL" if bot_ratio > 40 else ("ELEVATED" if bot_ratio > 15 else "NORMAL")
            })

        community_summary.sort(key=lambda x: x["member_count"], reverse=True)

        # Step 6: Prepare JSON nodes and edges for Vis.js UI
        vis_nodes = []
        vis_edges = []

        type_colors = {
            "user": "#5486bb",
            "topic": "#ffb703",
            "hashtag": "#00f59b",
            "organization": "#ec4899",
            "location": "#f97316"
        }

        for n, data in G.nodes(data=True):
            ntype = data.get("type", "entity")
            color = type_colors.get(ntype, "#8d93a3")
            
            # User color override by community or bot status
            if ntype == "user":
                if data.get("is_bot"):
                    color = "#ff3366"  # Red for bot
                else:
                    cid = user_communities.get(n, 0)
                    color = COMMUNITY_METADATA.get(cid, {}).get("color", "#5486bb")

            size = 18
            if ntype == "topic":
                size = 28
            elif ntype == "user":
                size = 14 + min(18, int(pagerank.get(n, 0) * 300))
            elif ntype == "organization":
                size = 22

            vis_nodes.append({
                "id": n,
                "label": data.get("label", n),
                "group": ntype,
                "color": color,
                "size": size,
                "title": f"<b>{data.get('label', n)}</b><br>Type: {ntype.upper()}<br>PR: {round(pagerank.get(n, 0), 4)}",
                "community_id": user_communities.get(n, -1)
            })

        for u, v, data in G.edges(data=True):
            rel = data.get("relation", "CONNECTS")
            edge_color = "#2a3140"
            if rel == "COORDINATED_WITH":
                edge_color = "#ff3366"
            elif rel == "MENTIONS":
                edge_color = "#00f0ff"

            vis_edges.append({
                "from": u,
                "to": v,
                "label": rel,
                "color": {"color": edge_color, "highlight": "#00f0ff"},
                "arrows": "to" if rel in ("MENTIONS", "USES_TAG", "DISCUSSES") else ""
            })

        return {
            "graph": G,
            "vis_nodes": vis_nodes,
            "vis_edges": vis_edges,
            "influencers": influencers,
            "communities": community_summary,
            "user_communities": user_communities,
            "node_count": G.number_of_nodes(),
            "edge_count": G.number_of_edges()
        }

    def find_shortest_path(self, G: nx.DiGraph, source: str, target: str) -> List[str]:
        """
        Finds the intelligence connection path between two arbitrary entities.
        """
        try:
            return nx.shortest_path(G.to_undirected(), source=source, target=target)
        except Exception:
            return []
