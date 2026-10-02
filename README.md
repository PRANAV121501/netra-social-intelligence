# NETRA — AI-Powered Social Intelligence Platform (SIH26152)

> **Transforming Social Media Streams into Actionable Intelligence through AI, NLP, Graph Analytics, and Predictive Forecasting.**

---

## 🎯 Executive Overview

Most social media analytics tools only perform basic keyword frequency counts, surface-level sentiment bar charts, and simple hashtag tallies.

**NETRA (National Electronic Threat & Narrative Reconnaissance Architecture)** is engineered specifically for **SIH26152** as a **Government-Grade Social Intelligence Platform**. Rather than merely monitoring posts, NETRA models the underlying socio-cognitive topology: who is initiating narratives, how information diffuses across network communities, which accounts exhibit synchronized astroturfing behavior, and which emerging themes are mathematically predicted to achieve viral saturation.

---

## 🔄 Core Intelligence Workflow

```
Social Media Dataset
        ↓
Data Processing & Normalization
        ↓
Multi-Entity Extraction (NER, spaCy, Orgs, Locations, Handles, Hashtags)
        ↓
Sentiment & Emotional Vector Analysis (Polarity, Stance, Threat Signals)
        ↓
Topic Detection & Velocity Engine (Growth Rate %, Acceleration, Lifecycle Stages)
        ↓
Community Detection (Louvain Modularity Partitioning & Echo Chamber Index)
        ↓
Influence Analysis (PageRank, Betweenness Centrality, Bridge Node Scoring)
        ↓
Information Propagation Analysis (Diffusion Trees, Cascade Depth, R₀ Virality Factor)
        ↓
Graph Intelligence (Heterogeneous Multi-Relational Knowledge Graph)
        ↓
Bot & Coordinated Inauthentic Behavior (CIB) Detection
        ↓
Predictive Intelligence (24h–72h Trajectory Modeling & Anomaly Forecasting)
        ↓
Interactive Intelligence Dashboard & AI Tactical Assistant (NAT)
```

---

## ⚡ Core Features & Capabilities

### 1. Entity Extraction
- Extracts **Usernames (`@`)**, **Hashtags (`#`)**, **Organizations (`ORG`)**, **Geographic Locations (`GPE`/`LOC`)**, **Topics**, **Mentions**, and **URLs**.
- Combines **spaCy NER** with curated tactical entity catalogs (CERT-In, NCIIPC, ISRO, DRDO, WHO, SEBI, UNESCO, etc.) for zero-latency enrichment.

### 2. Sentiment Intelligence & Emotional Vectors
- Classifies polarity: **Positive**, **Negative**, **Neutral**.
- Extracts multi-dimensional emotional signals: **Fear**, **Anger**, **Joy**, **Trust**, **Urgency**.
- Categorizes intelligence stances: *Authoritative/Factual*, *Sensational/Alarmist*, *Analytical/Discussion*.
- Tracks sentiment vectors over time and grouped by topic and community.

### 3. Trend Detection & Velocity Engine
- Analyzes volume, engagement multiplication, and temporal acceleration.
- Computes **Trend Score (0–100)**, **Growth Velocity (+% rate)**, and **Lifecycle Stages** (*Emerging*, *Accelerating*, *Peaking*, *Stabilizing*, *Decaying*).

### 4. Narrative Detection & Stance Decomposition
- Breaks macro-topics into emerging sub-narratives (e.g., within *Artificial Intelligence*: "Autonomous Code Disruption & Job Consolidation", "Sovereign AI Regulations & UNESCO Bias Audits", "Open Weights Defense vs Big Tech Capture").
- Maps narrative sentiment, engagement volume, and key amplifier handles.

### 5. Community Detection & Echo Chamber Partitioning
- Utilizes **Louvain Modularity Clustering** on the user interaction subgraph to partition the network into distinct ideological and operational clusters.
- Computes community size, activity level, dominant topics, and synthetic bot density.

### 6. Graph Centrality & Influence Analysis
- Computes **PageRank** (authoritative standing) and **Betweenness Centrality** (bridge nodes connecting disparate communities).
- Calculates a composite **Influence Score (0–100)** while applying severe algorithmic penalties to detected bot accounts.
- Categorizes nodes into *Alpha Influencers*, *Key Amplifiers*, and *Periphery Nodes*.

### 7. Information Propagation & Cascade Tracking
- Reconstructs narrative diffusion trees: **Originator Node ➔ Key Amplifiers ➔ Community Hubs ➔ Mass Audience**.
- Computes **Diffusion Velocity (hops/hr)** and the **Virality Reproduction Index ($R_0$)**.

### 8. Heterogeneous Knowledge Graph
- Interactive canvas powered by **Vis.js** modeling multiple node types (*Users*, *Topics*, *Hashtags*, *Organizations*, *Locations*) and edges (*DISCUSSES*, *MENTIONS*, *LOCATED_IN*, *COORDINATED_WITH*).
- Features **Node Search**, **Zoom/Fit Controls**, **Community Highlighting**, and **Path Finding** (identifying shortest connection paths between two arbitrary entities).

### 9. Bot & Coordinated Inauthentic Behavior (CIB) Detection
- Detects synchronized astroturfing and duplicate copy-paste messaging across distinct handles within narrow time windows.
- Evaluates account anomaly signals: extreme following-to-follower ratios, synthetic nomenclature signatures, and account recency.
- Generates tactical **Risk Alerts** with severity ratings (*CRITICAL*, *HIGH*, *MEDIUM*) and recommended countermeasures.

### 10. Predictive Intelligence (24h–72h Horizon)
- Forecasts trend velocity trajectories, projected 24-hour volume changes (+X%), and future emerging narratives.
- Computes confidence scores (e.g. 92% Confidence) based on cascade reproduction factors and cross-community spillover.

### 11. AI Tactical Intelligence Assistant (NAT)
- Natural Language Command Interface answering queries such as:
  - *"Show top influencers discussing AI"*
  - *"Find communities discussing cybersecurity"*
  - *"Explain why #GridBreach is trending"*
  - *"Show how Narrative Y spread"*
  - *"Are there bot clusters or coordinated campaigns?"*
  - *"Which topics are likely to trend next?"*
- Generates military/intelligence-grade structured briefings with executive summaries, evidence citations, entity links, and actionable countermeasures.

---

## 🖥️ 11 Dedicated Dashboard Sections

| # | Section | Key Capabilities |
|---|---|---|
| **1** | **Total Posts Analysed & Live Status** | Live ingestion counter, total entities, active communities, quarantine metrics |
| **2** | **Trending Topics** | Trend scores, velocity %, lifecycle stage badges, hashtag clouds |
| **3** | **Sentiment Overview** | Polarity balance bar, emotion intensity vectors, topic sentiment matrices |
| **4** | **Top Influencers** | Centrality leaderboard, PageRank, betweenness, follower ratio, bot penalties |
| **5** | **Community Network Graph** | Louvain modularity clusters, synthetic density %, dominant discourse |
| **6** | **Narrative Map** | Topic-to-subnarrative decomposition, stance indicators, driver handles |
| **7** | **Propagation Tracker** | Root originator tracing, hop delay timeline, viral reproduction index ($R_0$) |
| **8** | **Risk Alerts & CIB Monitor** | Astroturfing swarm alerts, copy-paste cluster inspector, actionable advisories |
| **9** | **Geographic Distribution** | Interactive Leaflet geospatial map with threat-level color coding and chatter volume |
| **10** | **Predictive Insights** | 24h–72h narrative trajectory forecasts, confidence scores, early warning signals |
| **11** | **AI Tactical Assistant** | Interactive intelligence conversational terminal with one-click query pills |

---

## 🚀 Quickstart & Execution

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Flask, NetworkX, Pandas, NumPy, spaCy

### Run Web Platform
```bash
cd C:\Users\prana\.gemini\antigravity\scratch\netra-social-intelligence
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

### Run Native Desktop Application
```bash
python desktop.py
```
Launches NETRA inside an isolated, borderless native application window via `pywebview`.

---

## 🧪 Verification & Automated Tests

Run the pipeline and endpoint validation suites:
```bash
# 1. Test core algorithmic pipeline (NLP, Louvain, PageRank, Cascades, Predictions)
python test_pipeline.py

# 2. Test Flask REST API endpoints and simulation
python test_app_endpoints.py

# 3. Generate high-volume simulated social media intelligence stream (150+ posts)
python data/synthetic_generator.py
```

---

