"""
Test Flask REST endpoints for NETRA Social Intelligence Platform.
"""

from app import app
import json

def test_endpoints():
    client = app.test_client()

    # 1. Main UI
    res = client.get("/")
    assert res.status_code == 200, f"Root returned {res.status_code}"
    print("GET / -> 200 OK")

    # 2. Pipeline state
    res = client.get("/api/pipeline/state")
    assert res.status_code == 200, f"/api/pipeline/state returned {res.status_code}"
    data = res.get_json()
    assert "summary_kpis" in data
    assert "trends" in data
    assert "influencers" in data
    assert "knowledge_graph" in data
    print(f"GET /api/pipeline/state -> 200 OK (KPIs: {data['summary_kpis']})")

    # 3. AI Assistant query
    res = client.post("/api/pipeline/query", json={"prompt": "Show top influencers discussing AI"})
    assert res.status_code == 200
    ai_data = res.get_json()
    assert "executive_briefing" in ai_data
    print("POST /api/pipeline/query -> 200 OK")

    # 4. Graph path finding
    res = client.get("/api/pipeline/path?source=TechInsights&target=IndiaAI")
    assert res.status_code == 200
    path_data = res.get_json()
    assert path_data.get("found") is True
    print(f"GET /api/pipeline/path -> 200 OK (path: {path_data['path']})")

    # 5. Live Simulation
    res = client.post("/api/pipeline/simulate")
    assert res.status_code == 200
    sim_data = res.get_json()
    assert sim_data.get("status") == "simulated"
    print("POST /api/pipeline/simulate -> 200 OK")

    # 6. Dossier Export (JSON)
    res = client.get("/api/export/dossier")
    assert res.status_code == 200
    dossier = res.get_json()
    assert "classification" in dossier
    print("GET /api/export/dossier -> 200 OK")

    # 7. Dossier Print (HTML)
    res = client.get("/dossier/print")
    assert res.status_code == 200
    assert b"NETRA TACTICAL INTELLIGENCE BRIEFING" in res.data
    print("GET /dossier/print -> 200 OK (Classified Dossier View)")

    # 8. Upload Dataset API
    sample_csv = "author,content,likes,retweets,followers,location\nTestNode,Critical radar test for intelligence upload #CyberSecurity,100,20,5000,New Delhi\n"
    import io
    data = {'file': (io.BytesIO(sample_csv.encode('utf-8')), 'test_stream.csv')}
    res = client.post("/api/pipeline/upload", data=data, content_type='multipart/form-data')
    assert res.status_code == 200
    up_data = res.get_json()
    assert up_data.get("status") == "success"
    print(f"POST /api/pipeline/upload -> 200 OK (Imported: {up_data['imported_count']} posts)")

    # 9. Connectors API (SIH Component A)
    res = client.get("/api/connectors/status")
    assert res.status_code == 200
    conn_data = res.get_json()
    assert "connectors" in conn_data
    print("GET /api/connectors/status -> 200 OK")

    res = client.post("/api/connectors/fetch", json={"platform": "twitter"})
    assert res.status_code == 200
    fetch_data = res.get_json()
    assert fetch_data.get("status") == "success"
    print(f"POST /api/connectors/fetch (Twitter) -> 200 OK (Fetched: {fetch_data['fetched']} posts)")

    print("\nALL FLASK ENDPOINTS VERIFIED & WORKING FLAWLESSLY!")

if __name__ == "__main__":
    test_endpoints()

