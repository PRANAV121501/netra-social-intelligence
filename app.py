"""
NETRA — AI-Powered Social Intelligence Platform (SIH26152)
Flask Application Backend

Translates large-scale social media streams into actionable intelligence
through NLP, Sentiment Vectors, Graph Centrality, Louvain Community Clustering,
Cascade Propagation Tracking, Bot / CIB Anomaly Detection, and Predictive Forecasting.
"""

from flask import Flask, render_template, request, jsonify, session, Response
import os
import json
import time
import csv
import io
from datetime import datetime
from functools import wraps

from engine.pipeline import IntelligencePipeline

app = Flask(__name__)
app.secret_key = os.environ.get("NETRA_SECRET", "netra-sip-2026-auth-token")

# Initialize master pipeline
pipeline = IntelligencePipeline()

# Load default sample stream into memory
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "sample_social_stream.json")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    INITIAL_POSTS = json.load(f)

# Run pipeline on startup
CURRENT_PIPELINE_RESULTS = pipeline.run(INITIAL_POSTS)

# Analyst / Intelligence Officer Profiles
PROFILES = {
    "admin":   {"name": "Dir. A. Kulkarni", "rank": "National Cyber Director", "dept": "NCIIPC / CERT-In Directorate", "level": 4, "pin": "1111", "badge": "DIR-01"},
    "io":      {"name": "Cmdr. R. Deshmukh", "rank": "Senior Threat Intel Officer", "dept": "Cognitive Warfare Division", "level": 3, "pin": "2222", "badge": "TIO-09"},
    "analyst": {"name": "P. Sharma", "rank": "OSINT & Graph Intelligence Analyst", "dept": "Social Dynamics Lab", "level": 2, "pin": "3333", "badge": "SIA-44"},
    "field":   {"name": "S. Iyer", "rank": "Tactical Field Operator", "dept": "Rapid Response Cyber Cell", "level": 1, "pin": "4444", "badge": "RRC-12"}
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            # For demonstration smoothness, default to analyst if not signed in
            session["user"] = "analyst"
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    user_key = session.get("user", "analyst")
    profile = PROFILES.get(user_key, PROFILES["analyst"])
    return render_template("index.html", profile=profile)

@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    data = request.get_json() or {}
    pin = data.get("pin", "").strip()
    for key, p in PROFILES.items():
        if p["pin"] == pin:
            session["user"] = key
            return jsonify({"status": "success", "profile": p})
    return jsonify({"status": "error", "message": "Invalid Intelligence Access PIN"}), 401

@app.route("/api/auth/logout", methods=["POST"])
def auth_logout():
    session.pop("user", None)
    return jsonify({"status": "success"})

@app.route("/api/pipeline/state", methods=["GET"])
def get_pipeline_state():
    """Returns the complete intelligence pipeline state."""
    global CURRENT_PIPELINE_RESULTS
    return jsonify(CURRENT_PIPELINE_RESULTS)

@app.route("/api/pipeline/run", methods=["POST"])
def re_run_pipeline():
    """Re-runs the intelligence pipeline with updated or uploaded posts."""
    global CURRENT_PIPELINE_RESULTS
    data = request.get_json()
    if data and "posts" in data and isinstance(data["posts"], list):
        CURRENT_PIPELINE_RESULTS = pipeline.run(data["posts"])
    else:
        CURRENT_PIPELINE_RESULTS = pipeline.run(INITIAL_POSTS)
    return jsonify(CURRENT_PIPELINE_RESULTS)

@app.route("/api/pipeline/query", methods=["POST"])
def assistant_query():
    """AI Tactical Intelligence Assistant endpoint."""
    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Empty query"}), 400
    response = pipeline.answer_query(prompt)
    return jsonify(response)

@app.route("/api/pipeline/path", methods=["GET"])
def graph_path():
    """Finds shortest path between two graph entities."""
    source = request.args.get("source", "").strip()
    target = request.args.get("target", "").strip()
    if not source or not target:
        return jsonify({"path": [], "found": False})
    path = pipeline.find_path(source, target)
    return jsonify({"path": path, "found": len(path) > 0})

@app.route("/api/pipeline/simulate", methods=["POST"])
def simulate_incoming_stream():
    """Simulates a live breaking post ingestion into the pipeline."""
    global CURRENT_PIPELINE_RESULTS
    new_post = {
        "id": f"post_live_{int(time.time())}",
        "author": "ThreatRadar_Global",
        "author_name": "Threat Radar Global Feed",
        "content": "BREAKING: Telemetry confirms anomalous data egress packets intercepted at Northern Power Substation. CERT-In countermeasures successfully prevented substation failover. #GridBreach #NationalSecurity",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "likes": 840,
        "retweets": 340,
        "replies": 62,
        "followers": 115000,
        "following": 320,
        "account_created": "2019-03-01",
        "location": "New Delhi",
        "verified": True,
        "urls": ["https://cert-in.org.in/bulletin-live"]
    }
    updated_posts = list(INITIAL_POSTS) + [new_post]
    CURRENT_PIPELINE_RESULTS = pipeline.run(updated_posts)
    return jsonify({"status": "simulated", "new_post": new_post, "results": CURRENT_PIPELINE_RESULTS})

@app.route("/api/export/dossier", methods=["GET"])
def export_dossier():
    """Generates an executive Intelligence Dossier in JSON or printable format."""
    state = CURRENT_PIPELINE_RESULTS
    dossier = {
        "classification": "RESTRICTED // LAW ENFORCEMENT & NATIONAL CYBER COMMAND",
        "system": "NETRA Social Intelligence Platform (SIH26152)",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "kpi_overview": state.get("summary_kpis", {}),
        "threat_alerts": state.get("alerts", []),
        "top_trends": state.get("trends", [])[:5],
        "emerging_narratives": state.get("narratives", [])[:5],
        "top_influencers": state.get("influencers", [])[:5],
        "predictive_forecast": state.get("predictions", [])[:5],
        "fact_checks": state.get("fact_checks", []),
        "cross_platform_hopping": state.get("cross_platform", [])
    }
    return Response(
        json.dumps(dossier, indent=2),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=NETRA_Intelligence_Dossier.json"}
    )

@app.route("/api/pipeline/upload", methods=["POST"])
def upload_dataset():
    """Ingests custom CSV or JSON dataset from the user and re-runs pipeline."""
    global CURRENT_PIPELINE_RESULTS
    parsed_posts = []

    if "file" in request.files:
        f = request.files["file"]
        filename = f.filename.lower()
        content = f.read().decode("utf-8", errors="ignore")

        if filename.endswith(".json"):
            try:
                parsed_posts = json.loads(content)
            except Exception as e:
                return jsonify({"status": "error", "message": f"Malformed JSON: {str(e)}"}), 400
        else:
            # Assume CSV
            try:
                reader = csv.DictReader(io.StringIO(content))
                for i, row in enumerate(reader):
                    post_text = row.get("content") or row.get("text") or row.get("tweet") or row.get("message") or ""
                    if not post_text.strip():
                        continue
                    author = row.get("author") or row.get("user") or row.get("username") or f"user_{i+1}"
                    followers = int(row.get("followers") or row.get("follower_count") or 1200)
                    following = int(row.get("following") or 250)
                    likes = int(row.get("likes") or row.get("favorites") or 50)
                    retweets = int(row.get("retweets") or row.get("shares") or 10)
                    location = row.get("location") or row.get("city") or "New Delhi"
                    platform = row.get("platform") or "Twitter"

                    parsed_posts.append({
                        "id": f"upload_post_{i+1}",
                        "author": author,
                        "author_name": author,
                        "content": post_text,
                        "timestamp": row.get("timestamp") or datetime.utcnow().isoformat() + "Z",
                        "followers": followers,
                        "following": following,
                        "likes": likes,
                        "retweets": retweets,
                        "replies": int(row.get("replies") or 5),
                        "location": location,
                        "platform": platform
                    })
            except Exception as e:
                return jsonify({"status": "error", "message": f"Failed to parse CSV: {str(e)}"}), 400
    elif request.is_json:
        data = request.get_json() or {}
        parsed_posts = data.get("posts", [])
    
    if not parsed_posts:
        return jsonify({"status": "error", "message": "No valid posts found in uploaded file"}), 400

    CURRENT_PIPELINE_RESULTS = pipeline.run(parsed_posts)
    return jsonify({
        "status": "success",
        "imported_count": len(parsed_posts),
        "results": CURRENT_PIPELINE_RESULTS
    })

@app.route("/dossier/print", methods=["GET"])
def print_dossier():
    """Renders a classified intelligence dossier formatted for printing or PDF export."""
    state = CURRENT_PIPELINE_RESULTS
    return render_template("dossier_print.html", state=state, now=datetime.utcnow().strftime("%d %b %Y %H:%M UTC"))


if __name__ == "__main__":
    print("=" * 60)
    print("  NETRA — AI-Powered Social Intelligence Platform (SIH26152)")
    print("  Operating at http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)
