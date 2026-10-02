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

    if (tabId === "tab-dashboard") {
        dashboardView.style.display = "block";
        tabContentView.style.display = "none";
        if (MAIN_GRAPH) setTimeout(() => MAIN_GRAPH.fit(), 100);
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

                // Esri World Dark Gray Canvas — zero API key required, no watermarks
                L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
                    attribution: '&copy; Esri, DeLorme, NAVTEQ',
                    maxZoom: 16
                }).addTo(map);

                // Esri Reference Labels Layer
                L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}", {
                    attribution: '',
                    maxZoom: 16
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
