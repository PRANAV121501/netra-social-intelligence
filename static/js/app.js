/**
 * NETRA — AI-Powered Social Intelligence Platform (SIH26152)
 * High-Performance Frontend Interactive Controller
 */

let PIPELINE_DATA = null;
let MAIN_GRAPH = null;
let GRAPH_NODES = null;
let GRAPH_EDGES = null;

document.addEventListener("DOMContentLoaded", () => {
    initNavigationTabs();
    initMobileMenu();
    initKeyboardShortcuts();
    initGraph();
    loadBackendState();
    initAIAssistant();
    initLiveToggle();
    initVoiceSearch();
    initDataUpload();
});

// ===================== NAVIGATION TABS =====================
function initNavigationTabs() {
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            const targetTab = link.getAttribute("data-tab");
            switchTab(targetTab);
        });
    });
}

function initMobileMenu() {
    const menuBtn = document.getElementById("mobile-menu-btn");
    const sidebar = document.getElementById("netra-sidebar");
    const backdrop = document.getElementById("sidebar-backdrop");

    if (!menuBtn || !sidebar) return;

    function toggleSidebar() {
        sidebar.classList.toggle("sidebar-open");
        if (backdrop) backdrop.classList.toggle("active");
    }

    function closeSidebar() {
        sidebar.classList.remove("sidebar-open");
        if (backdrop) backdrop.classList.remove("active");
    }

    menuBtn.addEventListener("click", toggleSidebar);
    if (backdrop) backdrop.addEventListener("click", closeSidebar);

    // Auto-close on nav item click when on tablet/mobile screens
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            if (window.innerWidth <= 1024) {
                closeSidebar();
            }
        });
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 1024) {
            closeSidebar();
        }
        if (MAIN_GRAPH) {
            MAIN_GRAPH.fit();
        }
    });
}

function switchTab(tabId) {
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(l => l.classList.remove("active"));

    const matchingNav = document.querySelector(`.nav-link[data-tab='${tabId}']`);
    if (matchingNav) matchingNav.classList.add("active");

    const dashboardView = document.getElementById("view-dashboard");
    const tabContentView = document.getElementById("view-tab-content");
    const tabTitle = document.getElementById("tab-view-title");
    const tabBody = document.getElementById("tab-view-body");

    // New standalone panels
    const standalonePanels = ["tab-demographics", "tab-timeline", "tab-datasources"];
    document.querySelectorAll(".tab-panel").forEach(p => p.style.display = "none");

    if (tabId === "tab-dashboard") {
        dashboardView.style.display = "block";
        tabContentView.style.display = "none";
        if (MAIN_GRAPH) setTimeout(() => MAIN_GRAPH.fit(), 100);
    } else if (standalonePanels.includes(tabId)) {
        dashboardView.style.display = "none";
        tabContentView.style.display = "none";
        const panel = document.getElementById(tabId);
        if (panel) {
            panel.style.display = "block";
            // Initialize content for that panel
            if (tabId === "tab-demographics") renderDemographicsTab();
            if (tabId === "tab-timeline") renderSentimentTimeline();
            if (tabId === "tab-datasources") renderDataSourcesTab();
        }
    } else {
        dashboardView.style.display = "none";
        tabContentView.style.display = "block";
        renderDetailedTab(tabId, tabTitle, tabBody);
    }
}

function renderDetailedTab(tabId, titleEl, bodyEl) {
    if (!PIPELINE_DATA) return;

    if (tabId === "tab-narratives") {
        titleEl.innerText = "Narrative Analysis & Stance Breakdown";
        bodyEl.innerHTML = `
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                ${PIPELINE_DATA.narratives.map(n => `
                    <div style="background:#111a2d; border:1px solid #1e293b; border-radius:6px; padding:14px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                            <b style="color:#fff; font-size:13px;">${n.narrative}</b>
                            <span style="font-size:10px; background:#0284c7; color:#fff; padding:2px 6px; border-radius:3px;">${n.stance}</span>
                        </div>
                        <div style="font-size:11px; color:#94a3b8; margin-bottom:8px;">"${n.sample_excerpt}"</div>
                        <div style="font-size:11px; color:#38bdf8;">Drivers: ${n.primary_drivers.join(", ")}</div>
                    </div>
                `).join("")}
            </div>
        `;
    } else if (tabId === "tab-trends") {
        titleEl.innerText = "Trending Topics & Acceleration Matrix";
        bodyEl.innerHTML = `
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                ${PIPELINE_DATA.trends.map(t => `
                    <div style="background:#111a2d; border:1px solid #1e293b; border-radius:6px; padding:14px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                            <b style="color:#fff; font-size:14px;">${t.topic}</b>
                            <span style="font-size:10px; background:rgba(16,185,129,0.2); color:#10b981; border:1px solid #10b981; padding:2px 8px; border-radius:3px;">${t.stage}</span>
                        </div>
                        <div style="font-size:12px; color:#cbd5e1; margin-bottom:6px;">Velocity: +${t.growth_rate_pct}% | Score: ${t.trend_score}/100</div>
                        <div style="font-size:11px; color:#94a3b8;">${t.sample_headline}</div>
                    </div>
                `).join("")}
            </div>
        `;
    } else if (tabId === "tab-communities") {
        titleEl.innerText = "Community Detection (Louvain Modularity)";
        bodyEl.innerHTML = `
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                ${PIPELINE_DATA.communities.map(c => `
                    <div style="background:#111a2d; border:1px solid #1e293b; border-left:4px solid ${c.color}; border-radius:6px; padding:14px;">
                        <div style="font-weight:700; color:#fff; font-size:13px; margin-bottom:4px;">${c.name}</div>
                        <div style="font-size:11px; color:#94a3b8; margin-bottom:6px;">Archetype: ${c.archetype} | Members: ${c.member_count}</div>
                        <div style="font-size:11px; color:#38bdf8;">Dominant Topic: ${c.dominant_topic}</div>
                    </div>
                `).join("")}
            </div>
        `;
    } else if (tabId === "tab-influencers") {
        titleEl.innerText = "Influencer Centrality Leaderboard";
        bodyEl.innerHTML = `
            <table style="width:100%; border-collapse:collapse; font-size:12px; text-align:left;">
                <tr style="border-bottom:1px solid #1e293b; color:#94a3b8;">
                    <th style="padding:10px;">User Node</th><th>Influence Score</th><th>PageRank</th><th>Betweenness</th><th>Followers</th><th>Impact Tier</th>
                </tr>
                ${PIPELINE_DATA.influencers.map(u => `
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05); color:#cbd5e1;">
                        <td style="padding:10px; color:#38bdf8; font-weight:600;">@${u.username}</td>
                        <td><b style="color:#fff;">${u.influence_score}</b>/100</td>
                        <td style="font-family:var(--font-mono);">${u.pagerank}</td>
                        <td style="font-family:var(--font-mono);">${u.betweenness}</td>
                        <td>${u.followers.toLocaleString()}</td>
                        <td><span style="font-size:10px; background:#1e293b; padding:2px 6px; border-radius:3px;">${u.impact_tier}</span></td>
                    </tr>
                `).join("")}
            </table>
        `;
    } else if (tabId === "tab-alerts") {
        titleEl.innerText = "Threat & Bot Anomaly Alerts (CIB Forensics)";
        bodyEl.innerHTML = `
            <div style="display:flex; flex-direction:column; gap:12px;">
                ${PIPELINE_DATA.alerts.map(a => `
                    <div style="background:rgba(239,68,68,0.06); border:1px solid rgba(239,68,68,0.3); border-radius:6px; padding:14px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                            <b style="color:#fff; font-size:13px;">${a.title}</b>
                            <span style="background:#ef4444; color:#fff; font-size:10px; font-weight:700; padding:2px 6px; border-radius:3px;">${a.severity}</span>
                        </div>
                        <div style="font-size:11px; color:#94a3b8; margin-bottom:6px;">Pattern: ${a.pattern} | Target: ${a.target_topic}</div>
                        <div style="font-size:11px; color:#f87171; margin-bottom:6px;">Sample Payload: "${a.sample_text}"</div>
                        <div style="background:#0b1120; border:1px dashed #1e293b; padding:6px 10px; border-radius:4px; font-size:11px; color:#38bdf8;">
                            Recommended Action: ${a.recommended_action}
                        </div>
                    </div>
                `).join("")}
            </div>
        `;
    } else if (tabId === "tab-predictive") {
        titleEl.innerText = "Predictive Intelligence & 24h–72h Forecasts";
        bodyEl.innerHTML = `
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                ${PIPELINE_DATA.predictions.map(p => `
                    <div style="background:#111a2d; border:1px solid #1e293b; border-radius:6px; padding:14px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                            <b style="color:#fff; font-size:13px;">${p.entity_name}</b>
                            <span style="background:rgba(168,85,247,0.2); color:#c084fc; font-size:10px; padding:2px 6px; border-radius:3px;">${p.confidence_score} CONFIDENCE</span>
                        </div>
                        <div style="font-size:12px; color:#10b981; font-weight:600; margin-bottom:4px;">Projected Velocity: ${p.projected_24h_velocity_change}</div>
                        <div style="font-size:11px; color:#cbd5e1; margin-bottom:6px;">State: ${p.predicted_state}</div>
                        <div style="font-size:10.5px; color:#94a3b8;">${p.forecast_reasoning}</div>
                    </div>
                `).join("")}
            </div>
        `;
    } else if (tabId === "tab-reports") {
        titleEl.innerText = "Intelligence Dossier & Reports";
        bodyEl.innerHTML = `
            <div style="background:#111a2d; border:1px solid #1e293b; border-radius:6px; padding:20px; text-align:center;">
                <h3 style="color:#fff; margin-bottom:8px;">Ready for Download</h3>
                <p style="font-size:12px; color:#94a3b8; max-width:500px; margin:0 auto 16px auto;">
                    Generates a comprehensive executive intelligence dossier incorporating the active knowledge graph, PageRank leaderboard, CIB alerts, and predictive narrative trajectories.
                </p>
                <a href="/api/export/dossier" target="_blank" style="background:#0284c7; color:#fff; text-decoration:none; padding:8px 18px; border-radius:5px; font-weight:600; font-size:12px; display:inline-block;">
                    Download Intelligence Dossier (JSON / Printable)
                </a>
            </div>
        `;
    } else if (tabId === "tab-graph-explorer") {
        titleEl.innerText = "Network Explorer";
        bodyEl.innerHTML = `
            <div style="font-size:12px; color:#94a3b8; margin-bottom:12px;">Full screen exploration of relationships across all multi-relational nodes.</div>
            <div id="explorer-graph-canvas" style="height:500px; background:#080c16; border-radius:6px; border:1px solid #1e293b;"></div>
        `;
        setTimeout(() => {
            const expContainer = document.getElementById("explorer-graph-canvas");
            if (expContainer && GRAPH_NODES && GRAPH_EDGES) {
                new vis.Network(expContainer, { nodes: GRAPH_NODES, edges: GRAPH_EDGES }, {
                    nodes: { shape: "dot", font: { color: "#f8fafc", face: "Inter", size: 12 } },
                    edges: { smooth: { type: "continuous" }, color: { color: "rgba(255,255,255,0.12)" } },
                    physics: { barnesHut: { gravitationalConstant: -3500, centralGravity: 0.3 } }
                });
            }
        }, 100);
    } else if (tabId === "tab-geo") {
        titleEl.innerText = "Geospatial Threat Intelligence (India Map)";
        bodyEl.innerHTML = `
            <div style="display:grid; grid-template-columns: 2fr 1fr; gap:16px;">
                <div>
                    <div style="font-size:12px; color:#94a3b8; margin-bottom:10px;">Regional narrative velocity, coordinated bot clusters, and threat hotspot density across India.</div>
                    <div id="india-leaflet-map" style="height:480px; width:100%; border-radius:8px; border:1px solid #1e293b;"></div>
                </div>
                <div style="background:#111a2d; border:1px solid #1e293b; border-radius:8px; padding:14px; max-height:510px; overflow-y:auto;">
                    <div style="font-size:12px; font-weight:700; color:#fff; margin-bottom:10px; border-bottom:1px solid #1e293b; padding-bottom:6px;">Regional Threat Density</div>
                    <div style="display:flex; flex-direction:column; gap:8px;">
                        ${(PIPELINE_DATA.geo_intel || []).map(g => `
                            <div style="background:#0f172a; border:1px solid #1e293b; border-radius:6px; padding:10px;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <b style="color:#fff; font-size:12.5px;">${g.city}</b>
                                    <span style="font-size:9.5px; font-weight:700; padding:2px 6px; border-radius:3px; background:${g.threat_level === 'CRITICAL' ? '#ef4444' : (g.threat_level === 'HIGH' ? '#f59e0b' : '#10b981')}; color:#fff;">${g.threat_level}</span>
                                </div>
                                <div style="font-size:11px; color:#94a3b8; margin-top:3px;">${g.state} (${g.region})</div>
                                <div style="font-size:10.5px; color:#38bdf8; margin-top:4px;">Volume: ${g.volume} posts | Engagement: ${g.total_engagement.toLocaleString()}</div>
                            </div>
                        `).join("")}
                    </div>
                </div>
            </div>
        `;
        setTimeout(() => {
            const mapContainer = document.getElementById("india-leaflet-map");
            if (mapContainer && typeof L !== "undefined") {
                if (window._indiaMapInstance) {
                    try { window._indiaMapInstance.remove(); } catch(e){}
                    window._indiaMapInstance = null;
                }

                const map = L.map("india-leaflet-map", {
                    center: [22.5937, 78.9629],
                    zoom: 5,
                    minZoom: 4,
                    maxZoom: 12
                });
                window._indiaMapInstance = map;

                // OpenStreetMap Free Public Tiles (100% Free, Zero API Keys, Zero Watermarks)
                L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>',
                    subdomains: ["a", "b", "c"],
                    maxZoom: 18
                }).addTo(map);

                (PIPELINE_DATA.geo_intel || []).forEach(g => {
                    const color = g.threat_level === "CRITICAL" ? "#ef4444" : (g.threat_level === "HIGH" ? "#f59e0b" : "#10b981");
                    const circle = L.circleMarker([g.lat, g.lon], {
                        radius: Math.max(9, Math.min(22, g.volume * 3)),
                        fillColor: color,
                        color: "#ffffff",
                        weight: 2,
                        opacity: 1,
                        fillOpacity: 0.8
                    }).addTo(map);

                    circle.bindPopup(`
                        <div style="font-family:Inter,sans-serif; padding:4px;">
                            <b style="color:#fff; font-size:13px; letter-spacing:0.5px;">${g.city}, ${g.state}</b><br>
                            <div style="margin:4px 0;">
                                <span style="display:inline-block; font-size:10px; font-weight:700; padding:2px 7px; border-radius:3px; background:${color}; color:#fff;">
                                    THREAT: ${g.threat_level} (${g.threat_score}/100)
                                </span>
                            </div>
                            <div style="font-size:11px; color:#94a3b8;">Analyzed Posts: <b style="color:#fff;">${g.volume}</b></div>
                            <div style="font-size:11px; color:#38bdf8;">Engagement: <b style="color:#fff;">${g.total_engagement.toLocaleString()}</b></div>
                            <div style="font-size:11px; color:${g.bot_activity_flag ? '#f87171' : '#10b981'}; margin-top:2px;">
                                Bot Telemetry: ${g.bot_activity_flag ? '⚠️ DETECTED' : '✓ Normal'}
                            </div>
                        </div>
                    `);
                });
            }
        }, 150);
    } else if (tabId === "tab-factcheck") {
        titleEl.innerText = "Fact-Check & Misinformation Debunking Radar";
        bodyEl.innerHTML = `
            <div style="font-size:12px; color:#94a3b8; margin-bottom:14px;">
                Continuous cross-referencing of viral narratives against official Indian truth registries (PIB Fact Check, CERT-In, SEBI, NCIIPC).
            </div>
            <div style="display:flex; flex-direction:column; gap:14px;">
                ${(PIPELINE_DATA.fact_checks || []).map(fc => `
                    <div style="background:#111a2d; border:1px solid #1e293b; border-left:4px solid ${fc.manipulation_index > 75 ? '#ef4444' : '#f59e0b'}; border-radius:6px; padding:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
                            <div>
                                <span style="font-size:10px; font-weight:700; background:#1e293b; color:#38bdf8; padding:2px 7px; border-radius:3px; margin-right:8px;">${fc.topic}</span>
                                <b style="color:#fff; font-size:13.5px;">${fc.verdict}</b>
                            </div>
                            <span style="font-size:10px; font-weight:800; background:${fc.official_status === 'DEBUNKED' ? '#ef4444' : '#f97316'}; color:#fff; padding:3px 8px; border-radius:3px;">
                                ${fc.official_status}
                            </span>
                        </div>
                        <div style="font-size:11.5px; color:#fca5a5; margin-bottom:8px; font-style:italic;">
                            Claim: "${fc.claim_sample}"
                        </div>
                        <div style="background:#090d18; border:1px solid #1e293b; border-radius:6px; padding:10px 12px; margin-bottom:10px;">
                            <div style="font-size:11px; font-weight:700; color:#10b981; margin-bottom:2px;">VERIFIED GROUND TRUTH:</div>
                            <div style="font-size:12px; color:#e2e8f0; line-height:1.45;">${fc.fact}</div>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px; color:#94a3b8;">
                            <div>Official Registry: <b style="color:#cbd5e1;">${fc.registry_source}</b></div>
                            <div style="display:flex; gap:14px;">
                                <span>Credibility: <b style="color:#f87171;">${fc.credibility_score}%</b></span>
                                <span>Manipulation Index: <b style="color:#ef4444;">${fc.manipulation_index}%</b></span>
                            </div>
                        </div>
                    </div>
                `).join("")}
            </div>
        `;
    } else if (tabId === "tab-hopping") {
        titleEl.innerText = "Cross-Platform Narrative Migration Hopping";
        bodyEl.innerHTML = `
            <div style="font-size:12px; color:#94a3b8; margin-bottom:14px;">
                Traces multi-platform narrative migration sequences across DarkWeb/Telegram, Reddit, Twitter/X, and News Portals.
            </div>
            <div style="display:flex; flex-direction:column; gap:16px;">
                ${(PIPELINE_DATA.cross_platform || []).map(cp => `
                    <div style="background:#111a2d; border:1px solid #1e293b; border-radius:8px; padding:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                            <div>
                                <b style="color:#fff; font-size:14px;">${cp.narrative}</b>
                                <div style="font-size:11px; color:#94a3b8; margin-top:2px;">Origin: ${cp.origin_platform} &bull; Reach: <b style="color:#38bdf8;">${cp.cross_platform_reach}</b></div>
                            </div>
                            <span style="font-size:10.5px; background:rgba(2,132,199,0.15); color:#38bdf8; border:1px solid #0284c7; padding:3px 9px; border-radius:4px; font-weight:600;">
                                ${cp.speed_multiplier}
                            </span>
                        </div>
                        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; margin-top:10px;">
                            ${cp.stages.map((st, idx) => `
                                <div style="background:#090d18; border:1px solid ${st.status.includes('ACTIVE') ? '#0284c7' : '#1e293b'}; border-radius:6px; padding:10px;">
                                    <div style="display:flex; justify-content:space-between; font-size:11px; color:#94a3b8; margin-bottom:4px;">
                                        <span>Hop ${idx + 1}</span>
                                        <span style="color:#cbd5e1; font-family:var(--font-mono);">${st.time_offset}</span>
                                    </div>
                                    <div style="font-weight:700; color:#fff; font-size:12px; margin-bottom:4px;">${st.icon} ${st.platform}</div>
                                    <div style="font-size:10.5px; color:#94a3b8; margin-bottom:6px;">${st.role}</div>
                                    <span style="font-size:9px; font-weight:700; padding:1px 5px; border-radius:3px; background:${st.status === 'COMPLETED' ? '#1e293b' : (st.status.includes('ACTIVE') ? '#0284c7' : '#334155')}; color:#fff;">
                                        ${st.status}
                                    </span>
                                </div>
                            `).join("")}
                        </div>
                    </div>
                `).join("")}
            </div>
        `;
    }
}

// ===================== KEYBOARD SHORTCUTS & SEARCH =====================
function initKeyboardShortcuts() {
    window.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
            e.preventDefault();
            const searchInput = document.getElementById("global-search-input");
            if (searchInput) searchInput.focus();
        }
    });

    const searchInput = document.getElementById("global-search-input");
    if (searchInput) {
        searchInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                const query = searchInput.value.trim();
                if (query) {
                    locateNodeOrAskAI(query);
                }
            }
        });
    }
}

function locateNodeOrAskAI(query) {
    const clean = query.replace(/^[@#]/, "").toLowerCase();
    let found = false;

    if (GRAPH_NODES) {
        GRAPH_NODES.forEach(node => {
            if (node.label && node.label.toLowerCase().includes(clean)) {
                MAIN_GRAPH.focus(node.id, { scale: 1.5, animation: { duration: 600 } });
                MAIN_GRAPH.selectNodes([node.id]);
                found = true;
            }
        });
    }

    if (!found) {
        askAI(query);
    }
}

// ===================== CONSTELLATION GRAPH INITIALIZATION =====================
function initGraph() {
    const container = document.getElementById("main-network-graph");
    if (!container) return;

    // Define the specific constellation clusters matching the user's uploaded mockup:
    // Centers: #IndiaAI (cyan), Cybersecurity (red), Climate Action (green), Stock Rally (purple), Policy & Governance (yellow), Tech Startups (orange)
    const clusterCenters = [
        { id: "hub_india_ai", label: "#IndiaAI", color: "#38bdf8", size: 30, group: "hashtag" },
        { id: "hub_cybersec", label: "Cybersecurity", color: "#ef4444", size: 24, group: "topic" },
        { id: "hub_climate", label: "Climate Action", color: "#10b981", size: 22, group: "topic" },
        { id: "hub_stock", label: "Stock Rally", color: "#a855f7", size: 22, group: "topic" },
        { id: "hub_policy", label: "Policy & Governance", color: "#facc15", size: 22, group: "topic" },
        { id: "hub_startups", label: "Tech Startups", color: "#fb923c", size: 22, group: "topic" }
    ];

    const nodesList = [...clusterCenters];
    const edgesList = [
        { from: "hub_india_ai", to: "hub_cybersec", color: "rgba(56, 189, 248, 0.4)" },
        { from: "hub_india_ai", to: "hub_climate", color: "rgba(56, 189, 248, 0.4)" },
        { from: "hub_india_ai", to: "hub_stock", color: "rgba(56, 189, 248, 0.4)" },
        { from: "hub_india_ai", to: "hub_policy", color: "rgba(56, 189, 248, 0.4)" },
        { from: "hub_india_ai", to: "hub_startups", color: "rgba(56, 189, 248, 0.4)" }
    ];

    // Generate surrounding satellite nodes
    const satellites = [
        { name: "TechInsights", parent: "hub_india_ai", color: "#38bdf8", type: "user" },
        { name: "DrRajeshPatel", parent: "hub_cybersec", color: "#ef4444", type: "user" },
        { name: "CERT-In", parent: "hub_cybersec", color: "#facc15", type: "organization" },
        { name: "PIB_FactCheck", parent: "hub_policy", color: "#facc15", type: "organization" },
        { name: "SEBI", parent: "hub_stock", color: "#facc15", type: "organization" },
        { name: "EcoFuture", parent: "hub_climate", color: "#10b981", type: "community" },
        { name: "New Delhi", parent: "hub_policy", color: "#fb923c", type: "location" },
        { name: "Bengaluru", parent: "hub_startups", color: "#fb923c", type: "location" },
        { name: "#DigitalIndia", parent: "hub_india_ai", color: "#c084fc", type: "hashtag" },
        { name: "#Infosec", parent: "hub_cybersec", color: "#c084fc", type: "hashtag" }
    ];

    // Add extra decorative nodes for the constellation feel
    for (let i = 1; i <= 35; i++) {
        const parentHub = clusterCenters[i % clusterCenters.length];
        nodesList.push({
            id: `sat_node_${i}`,
            label: i % 4 === 0 ? `@node_${i}` : "",
            color: parentHub.color,
            size: 6 + (i % 6),
            group: "satellite"
        });
        edgesList.push({
            from: parentHub.id,
            to: `sat_node_${i}`,
            color: "rgba(255, 255, 255, 0.12)"
        });
    }

    satellites.forEach((sat, idx) => {
        nodesList.push({
            id: `sat_spec_${idx}`,
            label: sat.name,
            color: sat.color,
            size: 14,
            group: sat.type
        });
        edgesList.push({
            from: sat.parent,
            to: `sat_spec_${idx}`,
            color: "rgba(255, 255, 255, 0.2)"
        });
    });

    GRAPH_NODES = new vis.DataSet(nodesList);
    GRAPH_EDGES = new vis.DataSet(edgesList);

    const options = {
        nodes: {
            shape: "dot",
            font: { color: "#f8fafc", face: "Inter", size: 11, strokeWidth: 0 },
            borderWidth: 1.5,
            borderColor: "rgba(255,255,255,0.2)"
        },
        edges: {
            smooth: { type: "continuous" },
            width: 1
        },
        physics: {
            barnesHut: { gravitationalConstant: -2800, centralGravity: 0.35, springLength: 75 },
            stabilization: { iterations: 100 }
        },
        interaction: { hover: true, tooltipDelay: 100, zoomView: true }
    };

    MAIN_GRAPH = new vis.Network(container, { nodes: GRAPH_NODES, edges: GRAPH_EDGES }, options);

    // Overlay controls
    document.getElementById("graph-tool-zoom-in")?.addEventListener("click", () => {
        const scale = MAIN_GRAPH.getScale() * 1.3;
        MAIN_GRAPH.moveTo({ scale: scale });
    });

    document.getElementById("graph-tool-zoom-out")?.addEventListener("click", () => {
        const scale = MAIN_GRAPH.getScale() * 0.7;
        MAIN_GRAPH.moveTo({ scale: scale });
    });

    document.getElementById("graph-tool-fit")?.addEventListener("click", () => {
        MAIN_GRAPH.fit();
    });

    document.getElementById("btn-graph-fullscreen")?.addEventListener("click", () => {
        MAIN_GRAPH.fit();
    });

    // Toggle Co-occurrence / Community
    const coBtn = document.getElementById("btn-toggle-cooccur");
    const commBtn = document.getElementById("btn-toggle-comm");
    if (coBtn && commBtn) {
        coBtn.addEventListener("click", () => {
            coBtn.classList.add("active");
            commBtn.classList.remove("active");
        });
        commBtn.addEventListener("click", () => {
            commBtn.classList.add("active");
            coBtn.classList.remove("active");
        });
    }
}

// ===================== LOAD BACKEND PIPELINE STATE =====================
async function loadBackendState() {
    try {
        const resp = await fetch("/api/pipeline/state");
        PIPELINE_DATA = await resp.json();
        console.log("NETRA Pipeline State Loaded:", PIPELINE_DATA.summary_kpis);
    } catch (err) {
        console.warn("Could not load backend pipeline state:", err);
    }
}

// ===================== LIVE TOGGLE =====================
function initLiveToggle() {
    const liveBtn = document.getElementById("btn-live-toggle");
    if (!liveBtn) return;

    liveBtn.addEventListener("click", async () => {
        liveBtn.style.opacity = "0.6";
        try {
            const resp = await fetch("/api/pipeline/simulate", { method: "POST" });
            const data = await resp.json();
            alert(`Live telemetry packet received!\nPost: ${data.new_post.content}`);
        } catch (e) {
            console.error("Simulation error:", e);
        } finally {
            liveBtn.style.opacity = "1";
        }
    });
}

// ===================== AI ASSISTANT =====================
function initAIAssistant() {
    const sendBtn = document.getElementById("ai-quick-send-btn");
    const input = document.getElementById("ai-quick-input");

    if (sendBtn && input) {
        sendBtn.addEventListener("click", () => {
            const q = input.value.trim();
            if (q) {
                input.value = "";
                askAI(q);
            }
        });
        input.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                const q = input.value.trim();
                if (q) {
                    input.value = "";
                    askAI(q);
                }
            }
        });
    }
}

async function askAI(promptText, speak = false) {
    const modal = document.getElementById("ai-briefing-modal");
    const body = document.getElementById("ai-modal-response-body");
    if (!modal || !body) return;

    modal.style.display = "flex";
    body.innerHTML = `<div style="color:#38bdf8; font-family:var(--font-mono);">[COMPUTING TACTICAL BRIEFING ON: "${promptText}"...]</div>`;

    try {
        const resp = await fetch("/api/pipeline/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: promptText })
        });
        const data = await resp.json();

        body.innerHTML = `
            <div style="margin-bottom:8px; font-weight:700; color:#38bdf8; font-size:14px;">
                ${promptText}
            </div>
            <div style="background:#111a2d; border-left:3px solid #0284c7; padding:10px 12px; margin-bottom:12px; border-radius:0 4px 4px 0;">
                ${data.executive_briefing || 'Analysis complete.'}
            </div>
            ${data.evidence_points ? `
                <div style="margin-bottom:12px;">
                    <b style="font-size:11px; color:#94a3b8; text-transform:uppercase;">Identified Evidence & Graph Signals:</b>
                    <ul style="margin:6px 0 0 16px; font-size:12px; color:#cbd5e1;">
                        ${data.evidence_points.map(p => `<li style="margin-bottom:4px;">${p}</li>`).join("")}
                    </ul>
                </div>
            ` : ''}
            ${data.actionable_recommendations ? `
                <div style="background:rgba(16,185,129,0.08); border:1px dashed #10b981; padding:8px 12px; border-radius:4px;">
                    <b style="color:#10b981; font-size:11px; text-transform:uppercase;">Recommended Tactical Action:</b>
                    <div style="font-size:11.5px; color:#cbd5e1; margin-top:4px;">
                        ${data.actionable_recommendations.join(" ")}
                    </div>
                </div>
            ` : ''}
        `;

        if (speak && data.executive_briefing) {
            speakBriefing(data.executive_briefing);
        }
    } catch (e) {
        body.innerHTML = `<span style="color:#ef4444;">Error retrieving tactical intelligence briefing.</span>`;
    }
}

// ===================== VOICE SEARCH & SPEECH SYNTHESIS =====================
function initVoiceSearch() {
    const voiceBtn = document.getElementById("ai-voice-btn");
    const input = document.getElementById("ai-quick-input");
    if (!voiceBtn || !input) return;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        voiceBtn.title = "Voice recognition not supported in this browser (use Chrome/Edge)";
        voiceBtn.style.opacity = "0.5";
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-IN";

    let isListening = false;

    voiceBtn.addEventListener("click", () => {
        if (isListening) {
            recognition.stop();
            return;
        }
        try {
            recognition.start();
            isListening = true;
            voiceBtn.classList.add("listening");
            input.placeholder = "Listening... Speak your query";
        } catch (e) {
            console.error("Speech recognition error:", e);
        }
    });

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        input.value = transcript;
        voiceBtn.classList.remove("listening");
        input.placeholder = "Type or speak question...";
        isListening = false;
        askAI(transcript, true);
    };

    recognition.onerror = () => {
        voiceBtn.classList.remove("listening");
        input.placeholder = "Type or speak question...";
        isListening = false;
    };

    recognition.onend = () => {
        voiceBtn.classList.remove("listening");
        input.placeholder = "Type or speak question...";
        isListening = false;
    };
}

function speakBriefing(text) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const cleanText = text.replace(/\[.*?\]/g, '').replace(/https?:\/\/\S+/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText.substring(0, 180));
    utterance.rate = 1.05;
    utterance.pitch = 0.95;
    window.speechSynthesis.speak(utterance);
}

// ===================== CUSTOM DATASET INGESTION =====================
function initDataUpload() {
    const openBtn = document.getElementById("btn-open-upload");
    const closeBtn = document.getElementById("btn-close-upload");
    const modal = document.getElementById("upload-modal");
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const submitBtn = document.getElementById("btn-submit-upload");
    const statusDiv = document.getElementById("upload-status");
    const templateBtn = document.getElementById("download-template-btn");

    if (!modal) return;

    if (openBtn) {
        openBtn.addEventListener("click", () => {
            modal.style.display = "flex";
            if (statusDiv) statusDiv.style.display = "none";
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            modal.style.display = "none";
        });
    }

    modal.addEventListener("click", (e) => {
        if (e.target === modal) modal.style.display = "none";
    });

    if (dropZone && fileInput) {
        dropZone.addEventListener("click", () => fileInput.click());

        dropZone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropZone.style.borderColor = "#0284c7";
            dropZone.style.background = "rgba(2,132,199,0.1)";
        });

        dropZone.addEventListener("dragleave", () => {
            dropZone.style.borderColor = "#334155";
            dropZone.style.background = "#111a2d";
        });

        dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropZone.style.borderColor = "#334155";
            dropZone.style.background = "#111a2d";
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                showSelectedFile(fileInput.files[0].name);
            }
        });

        fileInput.addEventListener("change", () => {
            if (fileInput.files.length) {
                showSelectedFile(fileInput.files[0].name);
            }
        });
    }

    function showSelectedFile(name) {
        if (!statusDiv) return;
        statusDiv.style.display = "block";
        statusDiv.style.background = "rgba(56,189,248,0.12)";
        statusDiv.style.border = "1px solid #0284c7";
        statusDiv.style.color = "#38bdf8";
        statusDiv.innerText = `Selected: ${name} — Click 'Run Intelligence Analysis' to begin.`;
    }

    if (submitBtn) {
        submitBtn.addEventListener("click", async () => {
            if (!fileInput.files || !fileInput.files.length) {
                alert("Please select a CSV or JSON dataset to ingest.");
                return;
            }

            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append("file", file);

            submitBtn.innerText = "Processing 10-Stage Pipeline...";
            submitBtn.disabled = true;

            try {
                const resp = await fetch("/api/pipeline/upload", {
                    method: "POST",
                    body: formData
                });
                const result = await resp.json();

                if (result.status === "success") {
                    PIPELINE_DATA = result.results;
                    updateDashboardWithBackendData();
                    statusDiv.style.background = "rgba(16,185,129,0.15)";
                    statusDiv.style.border = "1px solid #10b981";
                    statusDiv.style.color = "#10b981";
                    statusDiv.innerText = `Success! Ingested ${result.imported_count} posts. All graphs and intelligence metrics updated.`;

                    setTimeout(() => {
                        modal.style.display = "none";
                        submitBtn.innerText = "Run Intelligence Analysis";
                        submitBtn.disabled = false;
                        switchTab("tab-dashboard");
                    }, 1400);
                } else {
                    statusDiv.style.background = "rgba(239,68,68,0.15)";
                    statusDiv.style.border = "1px solid #ef4444";
                    statusDiv.style.color = "#ef4444";
                    statusDiv.innerText = `Upload Error: ${result.message}`;
                    submitBtn.innerText = "Run Intelligence Analysis";
                    submitBtn.disabled = false;
                }
            } catch (err) {
                alert("Failed to upload dataset: " + err.message);
                submitBtn.innerText = "Run Intelligence Analysis";
                submitBtn.disabled = false;
            }
        });
    }

    if (templateBtn) {
        templateBtn.addEventListener("click", () => {
            const csvContent = "data:text/csv;charset=utf-8,author,content,likes,retweets,followers,location,platform\n" +
                "TechObserver_IN,Critical breakthrough achieved by national AI labs in sovereign foundational models. #IndiaAI,840,210,45000,New Delhi,Twitter\n" +
                "CyberDefense_Cell,Advisory: High-frequency scanning intercepted on telecommunications switches. Countermeasures active. #NationalSecurity,1250,560,98000,Bengaluru,Twitter\n" +
                "MarketWatcher,Heavy trading volumes witnessed across technology and defense equities today. #StockRally,430,95,31000,Mumbai,Twitter\n" +
                "bot_swarm_delta_01,URGENT: Grid collapse imminent across northern sector power corridor. Retweet fast! #GridFailure,120,410,12,New Delhi,Twitter\n";
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "NETRA_sample_stream_template.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }
}

// =========================================================================
// DEMOGRAPHICS TAB RENDERER
// =========================================================================
function renderDemographicsTab() {
    if (!PIPELINE_DATA || !PIPELINE_DATA.demographics) return;
    const demo = PIPELINE_DATA.demographics;

    // Age Distribution
    const ageEl = document.getElementById("demo-age-chart");
    if (ageEl && demo.age_distribution) {
        ageEl.innerHTML = demo.age_distribution.map(item => {
            const label = item.name || item.bracket || "Unknown";
            return `
            <div style="margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                    <span style="font-weight:600; color:#e2e8f0;">${label} Years</span>
                    <span style="color:#38bdf8; font-family:var(--font-mono);">${item.count} users (${item.pct}%)</span>
                </div>
                <div style="height:8px; background:#1e293b; border-radius:4px; overflow:hidden;">
                    <div style="height:100%; width:${item.pct}%; background:linear-gradient(90deg, #0284c7, #38bdf8); border-radius:4px;"></div>
                </div>
            </div>
        `;}).join("");
    }

    // Language Distribution
    const langEl = document.getElementById("demo-lang-chart");
    if (langEl && demo.language_distribution) {
        const langColors = {"English": "#3b82f6", "Hindi": "#f59e0b", "Tamil": "#ec4899", "Telugu": "#8b5cf6", "Bengali": "#10b981", "Marathi": "#06b6d4"};
        langEl.innerHTML = demo.language_distribution.map(item => {
            const lang = item.name || item.language || "English";
            const col = langColors[lang] || "#0284c7";
            return `
            <div style="margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                    <span style="font-weight:600; color:#e2e8f0;">${lang}</span>
                    <span style="color:${col}; font-family:var(--font-mono);">${item.count} (${item.pct}%)</span>
                </div>
                <div style="height:8px; background:#1e293b; border-radius:4px; overflow:hidden;">
                    <div style="height:100%; width:${item.pct}%; background:${col}; border-radius:4px;"></div>
                </div>
            </div>
        `;}).join("");
    }

    // Persona Distribution
    const personaEl = document.getElementById("demo-persona-chart");
    if (personaEl && demo.persona_distribution) {
        const personaIcons = {
            "Power User": "⚡", "Influencer": "⭐", "Active Citizen": "👤",
            "Casual User": "💬", "Bot-Risk": "🤖"
        };
        personaEl.innerHTML = demo.persona_distribution.map(item => {
            const pName = item.name || item.persona || "User";
            return `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 12px; background:#111a2d; border-radius:6px; margin-bottom:8px; border:1px solid #1e293b;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span>${personaIcons[pName] || "🔹"}</span>
                    <span style="font-size:12.5px; font-weight:600; color:#f1f5f9;">${pName}</span>
                </div>
                <span style="font-size:11.5px; font-family:var(--font-mono); color:${pName === 'Bot-Risk' ? '#ef4444' : '#38bdf8'}; font-weight:700;">
                    ${item.count} (${item.pct}%)
                </span>
            </div>
        `;}).join("");
    }

    // Professional Interests
    const interestsEl = document.getElementById("demo-interests-chart");
    if (interestsEl && demo.interest_distribution) {
        interestsEl.innerHTML = demo.interest_distribution.map(item => {
            const intName = item.name || item.interest || "Interest";
            return `
            <div style="background:#111a2d; border:1px solid #1e293b; padding:10px 14px; border-radius:8px; display:flex; align-items:center; gap:10px;">
                <div style="width:32px; height:32px; border-radius:6px; background:rgba(56,189,248,0.1); display:flex; align-items:center; justify-content:center; color:#38bdf8; font-size:14px;">🎯</div>
                <div>
                    <div style="font-size:12px; font-weight:600; color:#fff;">${intName}</div>
                    <div style="font-size:11px; color:#94a3b8; font-family:var(--font-mono);">${item.count} posts • ${item.pct}% volume</div>
                </div>
            </div>
        `;}).join("");
    }

    // Sentiment by Age
    const sentAgeEl = document.getElementById("demo-sentiment-age");
    if (sentAgeEl && demo.sentiment_by_age) {
        sentAgeEl.innerHTML = `
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px;">
                ${Object.entries(demo.sentiment_by_age).map(([bracket, score]) => {
                    const isPos = score >= 0;
                    const col = isPos ? '#10b981' : '#ef4444';
                    return `
                    <div style="background:#111a2d; border:1px solid #1e293b; padding:14px; border-radius:8px; text-align:center;">
                        <div style="font-size:12px; color:#94a3b8; margin-bottom:6px;">Age Bracket: <b style="color:#fff;">${bracket}</b></div>
                        <div style="font-size:22px; font-weight:800; font-family:var(--font-mono); color:${col};">
                            ${isPos ? '+' : ''}${typeof score === 'number' ? score.toFixed(2) : score}
                        </div>
                        <div style="font-size:10.5px; color:#64748b; margin-top:4px;">${isPos ? 'Net Positive Sentiment' : 'Net Negative Sentiment'}</div>
                    </div>
                    `;
                }).join("")}
            </div>
        `;
    }
}

// =========================================================================
// SENTIMENT TIMELINE TAB RENDERER
// =========================================================================
let _timelineChartInstance = null;

function renderSentimentTimeline() {
    if (!PIPELINE_DATA) return;
    const timeline = PIPELINE_DATA.sentiment_timeline || [];
    const posts = PIPELINE_DATA.posts || [];

    // Main Chart.js Timeline Chart
    const canvas = document.getElementById("sentiment-timeline-chart");
    if (canvas && window.Chart) {
        if (_timelineChartInstance) {
            _timelineChartInstance.destroy();
        }

        let labels = [];
        let scores = [];
        let posPct = [];
        let negPct = [];

        if (timeline.length > 1) {
            labels = timeline.map(t => t.date);
            scores = timeline.map(t => t.avg_score);
            posPct = timeline.map(t => t.positive_pct);
            negPct = timeline.map(t => t.negative_pct);
        } else {
            const now = new Date();
            for (let i = 6; i >= 0; i--) {
                const d = new Date(now);
                d.setDate(d.getDate() - i);
                labels.push(d.toISOString().slice(5, 10));
            }
            scores = [-0.15, -0.32, -0.05, 0.18, 0.42, 0.28, 0.35];
            posPct = [25, 18, 38, 55, 68, 58, 62];
            negPct = [60, 72, 45, 28, 15, 22, 19];
        }

        const ctx = canvas.getContext("2d");
        _timelineChartInstance = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Compound Sentiment Index (-1 to +1)",
                        data: scores,
                        borderColor: "#38bdf8",
                        backgroundColor: "rgba(56, 189, 248, 0.1)",
                        tension: 0.35,
                        fill: true,
                        yAxisID: "y"
                    },
                    {
                        label: "Positive %",
                        data: posPct,
                        borderColor: "#10b981",
                        borderDash: [4, 4],
                        tension: 0.35,
                        yAxisID: "y1"
                    },
                    {
                        label: "Negative %",
                        data: negPct,
                        borderColor: "#ef4444",
                        borderDash: [4, 4],
                        tension: 0.35,
                        yAxisID: "y1"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(51,65,85,0.3)" }
                    },
                    y: {
                        type: "linear",
                        display: true,
                        position: "left",
                        min: -1.0,
                        max: 1.0,
                        ticks: { color: "#38bdf8" },
                        grid: { color: "rgba(51,65,85,0.3)" }
                    },
                    y1: {
                        type: "linear",
                        display: true,
                        position: "right",
                        min: 0,
                        max: 100,
                        ticks: { color: "#94a3b8" },
                        grid: { drawOnChartArea: false }
                    }
                },
                plugins: {
                    legend: { labels: { color: "#e2e8f0", font: { size: 11 } } }
                }
            }
        });
    }

    // Dominant Emotions Timeline
    const emoList = document.getElementById("emotion-timeline-list");
    if (emoList) {
        const emotionIcons = {
            fear: "😨 Fear", anxiety: "😰 Anxiety", anger: "😡 Anger",
            joy: "😊 Joy", excitement: "🔥 Excitement", trust: "🛡️ Trust",
            urgency: "⚡ Urgency", sarcasm: "😏 Sarcasm"
        };
        const sampleEmos = [
            { date: "Day -3", emo: "fear", val: "Critical (0.82)", note: "Triggered by Power Substation disinformation" },
            { date: "Day -2", emo: "anxiety", val: "Elevated (0.65)", note: "Viral echo chambers debating grid reliability" },
            { date: "Day -1", emo: "trust", val: "Rising (0.74)", note: "PIB and CERT-In advisories actively debunking" },
            { date: "Today", emo: "excitement", val: "Dominant (0.78)", note: "National AI mission and space sector announcements" }
        ];
        emoList.innerHTML = sampleEmos.map(item => `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; background:#111a2d; border-radius:6px; margin-bottom:8px; border:1px solid #1e293b;">
                <div>
                    <span style="font-weight:700; color:#38bdf8; font-size:12px; margin-right:8px;">${item.date}</span>
                    <span style="font-size:12.5px; color:#fff; font-weight:600;">${emotionIcons[item.emo] || item.emo}</span>
                    <div style="font-size:11px; color:#64748b; margin-top:2px;">${item.note}</div>
                </div>
                <span style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); padding:3px 8px; border-radius:12px; font-size:11px; font-family:var(--font-mono);">
                    ${item.val}
                </span>
            </div>
        `).join("");
    }

    // Sarcasm Statistics
    const sarcasmEl = document.getElementById("sarcasm-stats");
    if (sarcasmEl) {
        const total = posts.length || 1;
        const sarcasticCount = posts.filter(p => (p.sentiment && p.sentiment.sarcasm_score > 0.3)).length;
        const sarcasmPct = Math.round((sarcasticCount / total) * 100);
        sarcasmEl.innerHTML = `
            <div style="font-size:26px; font-weight:800; font-family:var(--font-mono); color:#f59e0b;">
                ${sarcasmPct}%
            </div>
            <div style="font-size:12px; color:#94a3b8; margin-top:4px;">${sarcasticCount} out of ${total} posts exhibit sarcastic or ironic tone</div>
            <div style="height:6px; background:#1e293b; border-radius:3px; overflow:hidden; margin-top:10px;">
                <div style="height:100%; width:${sarcasmPct}%; background:#f59e0b;"></div>
            </div>
        `;
    }

    // Stance Statistics
    const stanceEl = document.getElementById("stance-stats");
    if (stanceEl) {
        const total = posts.length || 1;
        const supportive = posts.filter(p => (p.sentiment && p.sentiment.support_stance === "Supportive")).length;
        const against = posts.filter(p => (p.sentiment && p.sentiment.support_stance === "Against")).length;
        const neutral = total - supportive - against;
        const supPct = Math.round((supportive / total) * 100);
        const agnPct = Math.round((against / total) * 100);

        stanceEl.innerHTML = `
            <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:12px;">
                <span style="color:#10b981; font-weight:600;">Supportive: ${supportive} (${supPct}%)</span>
                <span style="color:#ef4444; font-weight:600;">Against: ${against} (${agnPct}%)</span>
            </div>
            <div style="height:8px; background:#1e293b; border-radius:4px; overflow:hidden; display:flex;">
                <div style="height:100%; width:${supPct}%; background:#10b981;"></div>
                <div style="height:100%; width:${agnPct}%; background:#ef4444;"></div>
            </div>
            <div style="font-size:11px; color:#64748b; margin-top:8px;">Neutral/Observation: ${neutral} posts</div>
        `;
    }
}

// =========================================================================
// DATA SOURCES CONNECTORS HANDLERS
// =========================================================================
async function renderDataSourcesTab() {
    try {
        const res = await fetch("/api/connectors/status");
        const data = await res.json();
        const twBadge = document.getElementById("tw-status-badge");
        const tgBadge = document.getElementById("tg-status-badge");
        const sumEl = document.getElementById("connector-summary");

        if (data.connectors) {
            data.connectors.forEach(c => {
                if (c.platform === "Twitter/X" && twBadge) {
                    twBadge.innerHTML = c.connected
                        ? "<span style='color:#10b981;'>● Connected (Live Mode)</span>"
                        : "<span style='color:#64748b;'>● Disconnected (Sample Mode)</span>";
                }
                if (c.platform === "Telegram" && tgBadge) {
                    tgBadge.innerHTML = c.connected
                        ? "<span style='color:#10b981;'>● Connected (Live Mode)</span>"
                        : "<span style='color:#64748b;'>● Disconnected (Sample Mode)</span>";
                }
            });
        }
        if (sumEl) {
            sumEl.innerHTML = `
                Active configured live pipelines: <b style="color:#38bdf8;">${data.total_configured}</b> |
                Default engine operational state: <b style="color:#10b981;">Normal (SIH26152 Multistream Ready)</b>
            `;
        }
    } catch (e) {
        console.error("Failed to load connector status:", e);
    }
}

async function configureConnector(platform) {
    let payload = { platform };
    const resEl = document.getElementById(platform === "twitter" ? "tw-result" : "tg-result");
    if (resEl) resEl.innerHTML = "Testing connection...";

    if (platform === "twitter") {
        const token = document.getElementById("tw-bearer-token")?.value.trim();
        payload.bearer_token = token;
    } else if (platform === "telegram") {
        payload.api_id = document.getElementById("tg-api-id")?.value.trim();
        payload.api_hash = document.getElementById("tg-api-hash")?.value.trim();
        payload.phone = document.getElementById("tg-phone")?.value.trim();
    }

    try {
        const res = await fetch("/api/connectors/configure", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (resEl) {
            if (data.test && data.test.status === "connected") {
                resEl.innerHTML = `<span style="color:#10b981;">✓ ${data.test.message}</span>`;
            } else {
                resEl.innerHTML = `<span style="color:#f59e0b;">⚠ ${data.test ? data.test.message : 'Sample fallback mode'}</span>`;
            }
        }
        renderDataSourcesTab();
    } catch (e) {
        if (resEl) resEl.innerHTML = `<span style="color:#ef4444;">Error: ${e.message}</span>`;
    }
}

async function fetchFromConnector(platform) {
    const resEl = document.getElementById(platform === "twitter" ? "tw-result" : "tg-result");
    if (resEl) resEl.innerHTML = "Fetching posts and running 14-stage pipeline...";

    let query = "#India";
    if (platform === "twitter") {
        query = document.getElementById("tw-query")?.value.trim() || "#India";
    } else if (platform === "telegram") {
        query = document.getElementById("tg-channel")?.value.trim() || "@india_news";
    }

    try {
        const res = await fetch("/api/connectors/fetch", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ platform, query })
        });
        const data = await res.json();
        if (data.status === "success") {
            if (resEl) resEl.innerHTML = `<span style="color:#10b981;">✓ Ingested ${data.fetched} posts from ${platform} (${data.mode}). Total posts: ${data.total_posts}</span>`;
            // Reload pipeline state
            if (typeof loadPipelineState === "function") {
                await loadPipelineState();
            }
        } else {
            if (resEl) resEl.innerHTML = `<span style="color:#ef4444;">Failed: ${data.error || 'Unknown error'}</span>`;
        }
    } catch (e) {
        if (resEl) resEl.innerHTML = `<span style="color:#ef4444;">Fetch Error: ${e.message}</span>`;
    }
}

