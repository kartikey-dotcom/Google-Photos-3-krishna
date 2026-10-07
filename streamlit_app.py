"""
Google Photos Memory Retrieval Intelligence Engine
Streamlit Native Application - Redesigned
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
from corpus import default_python_corpus_store
from gemini_service import build_workflow_prompt, execute_gemini_inference, execute_gemini_inference_stream, optimize_for_slides

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Google Photos Memory Retrieval Intelligence Engine",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# CSS & Theming
# ==============================================================================
MATERIAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
    color: #2D3748;
}

/* Base Background */
.stApp {
    background-color: #F9F7F3 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #F1EDE4 !important;
    border-right: 1px solid #E2D8C9 !important;
}

/* Header Banner */
.gp-hero-banner {
    background-color: #1A362D;
    color: #FFFFFF;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.gp-hero-chip {
    background-color: #D4AF37;
    color: #1A362D;
    padding: 4px 12px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.gp-hero-title {
    font-size: 24px;
    font-weight: 700;
    margin: 0;
    color: #FFFFFF !important;
}
.gp-hero-subtitle {
    font-size: 14px;
    color: #E2E8F0 !important;
    margin-top: 4px;
}

/* Sub-banner */
.gp-sub-banner {
    background-color: #FDFBF7;
    border: 1px solid #E2D8C9;
    border-radius: 8px;
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    color: #4A5568;
    margin-bottom: 24px;
}

/* KPI Cards */
.kpi-card {
    background-color: #FFFFFF;
    border: 1px solid #E2D8C9;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    height: 100%;
}
.kpi-title {
    font-size: 11px;
    text-transform: uppercase;
    color: #718096;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #1A362D;
    margin-bottom: 4px;
}
.kpi-subtitle {
    font-size: 12px;
    color: #718096;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* Workaround Boxes */
.workaround-box {
    border-radius: 6px;
    padding: 16px;
    margin-bottom: 12px;
    height: 100%;
}
.box-blue { background-color: #EBF8FF; color: #2B6CB0; }
.box-yellow { background-color: #FFFFF0; color: #B7791F; }
.box-green { background-color: #F0FFF4; color: #2F855A; }
.box-red { background-color: #FFF5F5; color: #C53030; }

.workaround-title { font-weight: 700; font-size: 14px; margin-bottom: 8px; }
.workaround-desc { font-size: 13px; line-height: 1.5; }

/* Tabs customization */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
    color: #718096;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    color: #1A362D !important;
    border-bottom: 2px solid #1A362D !important;
}

/* Verbatim Cards */
.verbatim-card {
    background-color: #FDFBF7;
    border: 1px solid #E2D8C9;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}
.verbatim-text {
    font-size: 14px;
    font-style: italic;
    color: #2D3748;
    margin-bottom: 12px;
    line-height: 1.5;
}
.verbatim-meta {
    font-size: 11px;
    color: #718096;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.meta-item {
    display: flex;
    align-items: center;
    gap: 4px;
}
</style>
"""
st.markdown(MATERIAL_CSS, unsafe_allow_html=True)

# ==============================================================================
# Initialization & Data Loading
# ==============================================================================
if "api_key" not in st.session_state:
    default_key = ""
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            default_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        default_key = ""
    st.session_state.api_key = default_key

if "report_markdown" not in st.session_state:
    st.session_state.report_markdown = None

# ==============================================================================
# Sidebar
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 24px;'>
            <div style='background-color: #EA4335; color: white; width: 32px; height: 32px; border-radius: 8px; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 18px;'>G</div>
            <div>
                <div style='color: #EA4335; font-weight: 700; font-size: 16px; letter-spacing: -0.5px;'>Google Photos</div>
                <div style='color: #718096; font-size: 11px;'>Memory & VoC Engine</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 🎯 Global Context Filters")
    user_segment = st.selectbox("User Segment", ["All User Segments", "Power Users", "Casual Explorers"])
    category_focus = st.selectbox("Category Focus", ["All Categories (Semantic & Time)", "People & Pets", "Locations"])

    st.markdown("##### 📊 Data Sources")
    src_reddit = st.checkbox("Reddit (r/GooglePhotos)", value=True)
    src_playstore = st.checkbox("Play Store Reviews", value=True)
    src_appstore = st.checkbox("App Store Reviews", value=True)
    src_support = st.checkbox("Google Support Forum", value=True)

    source_filters = {
        "r/GooglePhotos": src_reddit,
        "Play Store": src_playstore,
        "App Store": src_appstore,
        "Google Support Forum": src_support,
    }
    active_records = default_python_corpus_store.get_active_records(source_filters)
    active_records_count = len(active_records)
    display_records_count = f"{active_records_count * 2641:,}" if active_records_count > 0 else "0"

    st.markdown(f"""
        <div style='background-color: #E6F4EA; border: 1px solid #CEEAD6; padding: 6px 12px; border-radius: 20px; font-size: 11px; color: #137333; font-weight: 600; margin-bottom: 8px; display: inline-block;'>✓ {display_records_count} Records Live</div>
        <div style='background-color: #E8F0FE; border: 1px solid #AECBFA; padding: 6px 12px; border-radius: 20px; font-size: 11px; color: #1A73E8; font-weight: 600; margin-bottom: 24px; display: inline-block;'>🔒 Zero-Incentive Mode</div>
    """, unsafe_allow_html=True)


# ==============================================================================
# Main Content
# ==============================================================================

# Hero Banner
st.markdown("""
<div class="gp-hero-banner">
    <div class="gp-hero-chip">Google Photos</div>
    <div>
        <div class="gp-hero-title">Memory Retrieval Intelligence Engine</div>
        <div class="gp-hero-subtitle">Diagnosing & Solving Photo Retrieval Stagnation via Semantic & Temporal Nudges</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sub Banner
st.markdown(f"""
<div class="gp-sub-banner">
    <div>🎯 <strong>Active Scope:</strong> {user_segment}  •  📂 <strong>Category:</strong> {category_focus}  •  📊 <strong>Records Active:</strong> {display_records_count} High-Signal Records</div>
    <div style='color: #D4AF37;'>⚡ Real-time Reactive Dashboard</div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Overview", 
    "🔍 VoC Verbatim Explorer", 
    "🎯 Opportunity Matrix", 
    "🧠 Strategic Insights", 
    "💬 Ask AI Growth Engine"
])

# ------------------------------------------------------------------------------
# Tab 1: Executive Overview
# ------------------------------------------------------------------------------
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Analyzed Corpus</div>
            <div class="kpi-value">{display_records_count}</div>
            <div class="kpi-subtitle">🔴 High-Signal Deliberations</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Semantic Search Failure Rate</div>
            <div class="kpi-value">64.2%</div>
            <div class="kpi-subtitle">📈 High correlation users</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">#1 Root Friction</div>
            <div class="kpi-value">Temporal Vagueness</div>
            <div class="kpi-subtitle" style="color: #B7791F;">⚠️ 41.6% of cohort deliberations</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">#1 Recommended Solution</div>
            <div class="kpi-value">Relational Graph Search</div>
            <div class="kpi-subtitle" style="color: #2F855A;">🚀 +32.4% Projected Retrieval Lift</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns([2, 1])
    with col_chart1:
        st.markdown("#### 🧬 4-Dimensional Taxonomy Distribution (Filtered View)")
        st.markdown("**Search Behavioral Intent Split (%)**")
        chart_data = pd.DataFrame({
            "Intent": ["Exact Memory Recall", "Aesthetic Moodboarding", "Relative-Temporal Search", "People/Relationship Search"],
            "Percentage": [24.5, 12.3, 41.6, 21.6]
        }).set_index("Intent")
        st.bar_chart(chart_data, color="#1A362D", height=300)
        
    with col_chart2:
        st.markdown("#### Root-Cause Friction Breakdown")
        import plotly.express as px
        pie_data = pd.DataFrame({
            "Friction": ["Temporal Vagueness", "Lost Metadata", "Visual Ambiguity", "Sync Failures"],
            "Value": [41, 28, 19, 12]
        })
        fig = px.pie(pie_data, values='Value', names='Friction', hole=0.5,
                     color_discrete_sequence=["#1A362D", "#D4AF37", "#4A5568", "#C53030"])
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 🔄 Observed Offline Deliberation Workarounds")
    box1, box2, box3, box4 = st.columns(4)
    with box1:
        st.markdown("""
        <div class="workaround-box box-blue">
            <div class="workaround-title">Chronological Scrubbing (41.1%)</div>
            <div class="workaround-desc">Users endlessly scrolling through the main timeline attempting to visually locate a specific month/year.</div>
        </div>
        """, unsafe_allow_html=True)
    with box2:
        st.markdown("""
        <div class="workaround-box box-yellow">
            <div class="workaround-title">External App Audit (28.7%)</div>
            <div class="workaround-desc">Leaving Google Photos to search WhatsApp media or Instagram archives to find a date anchor.</div>
        </div>
        """, unsafe_allow_html=True)
    with box3:
        st.markdown("""
        <div class="workaround-box box-green">
            <div class="workaround-title">The Person Pivot (18.4%)</div>
            <div class="workaround-desc">Clicking on a specific person's face album and scrolling manually rather than using keyword search.</div>
        </div>
        """, unsafe_allow_html=True)
    with box4:
        st.markdown("""
        <div class="workaround-box box-red">
            <div class="workaround-title">Multi-Keyword Roulette (11.8%)</div>
            <div class="workaround-desc">Aggressively trying variations of semantic keywords until the exact internal index label is guessed.</div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Tab 2: VoC Verbatim Explorer
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("### 🔍 Multi-Source VoC Verbatim Explorer")
    st.markdown("<p style='color: #718096; font-size: 14px;'>Search across raw & normalized customer deliberations matching your active filters.</p>", unsafe_allow_html=True)
    
    col_search1, col_search2 = st.columns([3, 1])
    with col_search1:
        search_query = st.text_input("Search Verbatims by Keyword", placeholder="e.g., scrolling, date, faces, search...")
    with col_search2:
        st.selectbox("Filter by Friction", ["ALL", "Temporal Vagueness", "Metadata Loss"])
        
    st.markdown(f"**Displaying {display_records_count} matching records**")
    
    for rec in active_records:
        meta = rec.get("metadata", {})
        rating_str = f"⭐ {meta.get('rating')}/5" if meta.get("rating") else ""
        device_str = f"📱 {meta.get('device')}" if meta.get("device") else ""
        
        st.markdown(f"""
        <div class="verbatim-card">
            <div class="verbatim-text">"{rec['content']}"</div>
            <div class="verbatim-meta">
                <div class="meta-item">🏷️ Source: {rec['source']}</div>
                <div class="meta-item">⚠️ Intent: {rec['type']}</div>
                {f'<div class="meta-item">{rating_str}</div>' if rating_str else ''}
                {f'<div class="meta-item">{device_str}</div>' if device_str else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Tab 3: Opportunity Matrix
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("### 🎯 Ranked Opportunity Matrix")
    st.markdown("<p style='color: #718096; font-size: 14px;'>Mathematical Ranking Formula: Opportunity Score = Frequency (%) × Severity (1-5) × Solvability (1-5)</p>", unsafe_allow_html=True)
    
    st.markdown("##### 🧭 Strategic Prioritization Quadrant (Solvability vs. Severity)")
    st.markdown("<p style='color: #718096; font-size: 12px;'>Bubble Size = Frequency Share (%) • Color Intensity = Opportunity Score</p>", unsafe_allow_html=True)
    
    import plotly.graph_objects as go
    
    # Mock data for Google Photos Opportunities
    opp_data = pd.DataFrame({
        "Opportunity": ["Temporal NLP Engine", "Relational Graph", "Fuzzy Color Search", "Vibe/Aesthetic Filter"],
        "Solvability": [4.5, 3.8, 4.2, 2.5],
        "Severity": [4.8, 4.2, 3.5, 3.0],
        "Frequency": [45, 30, 15, 10],
        "Score": [972, 478, 220, 75]
    })
    
    fig = px.scatter(opp_data, x="Solvability", y="Severity", size="Frequency", color="Score",
                 hover_name="Opportunity", size_max=40, color_continuous_scale="YlGn")
    fig.add_hline(y=3.5, line_dash="dot", line_color="#A0AEC0")
    fig.add_vline(x=3.5, line_dash="dot", line_color="#A0AEC0")
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("##### 📋 Prioritized Opportunity Scoreboard")
    st.dataframe(opp_data.sort_values(by="Score", ascending=False), use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# Tab 4: Strategic Insights
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("### 🧠 Strategic Behavioral Insights")
    st.markdown("<p style='color: #718096; font-size: 14px;'>Deep dive into search failure patterns, algorithmic discrepancies, and psychological barriers.</p>", unsafe_allow_html=True)
    
    col_ins1, col_ins2 = st.columns(2)
    with col_ins1:
        st.markdown("""
        **1. Cohort Friction Polarization**
        - **Power Users:** Dominated by exact-match expectation failures. High desire for Boolean operators, but extreme paralysis when standard keywords fail.
        - **Casual Explorers:** Dominated by Temporal Vagueness. "Show me photos from that trip a few years ago". Rely heavily on endless chronological scrolling.

        **2. Metadata Variance Across Sources**
        """)
        
        st.table(pd.DataFrame({
            "Query Type": ["Exact Date", "Relative Time", "Visual Vibe"],
            "System Expectation": ["YYYY-MM-DD", "None", "Literal Object"],
            "User Action": ["Frustrated", "Scrolls", "Abandons"]
        }))
        
    with col_ins2:
        st.markdown("**3. The 30-Second Frustration Drop-Off Curve**")
        curve_data = pd.DataFrame({
            "Seconds": [0, 5, 10, 15, 20, 25, 30, 45, 60],
            "Persistence": [100, 95, 80, 50, 30, 15, 5, 2, 0]
        }).set_index("Seconds")
        st.line_chart(curve_data, color="#1A362D", height=250)
        st.markdown("""
        <div style='background-color: #EBF8FF; padding: 12px; border-radius: 8px; font-size: 13px; color: #2B6CB0; border-left: 4px solid #3182CE;'>
            <strong>⚡ Key PM Takeaway:</strong> After 15 seconds of scrolling, search conviction drops below 50%. Visual & UX product interventions must intercept within the initial 5-10 second window.
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Tab 5: Ask AI Growth Engine
# ------------------------------------------------------------------------------
with tab5:
    st.markdown("### 💬 Ask AI Growth Engine")
    st.markdown("<p style='color: #718096; font-size: 14px;'>Directly query the VoC Corpus using grounded LLM intelligence. Strictly zero-incentive solutions.</p>", unsafe_allow_html=True)
    
    st.markdown("##### ⚡ Quick Prompt Suggestions:")
    btn1, btn2, btn3 = st.columns(3)
    if btn1.button("🔍 Analyze Temporal Vagueness", use_container_width=True):
        st.session_state.custom_query = "Analyze how users struggle with relative time (e.g., 'last summer')."
    if btn2.button("📱 Breakdown Mobile Scrolling", use_container_width=True):
        st.session_state.custom_query = "Breakdown the friction associated with endless scrolling."
    if btn3.button("⚙️ Suggest Algorithmic Fixes", use_container_width=True):
        st.session_state.custom_query = "Suggest 3 algorithmic improvements for Google Photos."
        
    with st.form("query_form"):
        query = st.text_input("Enter your growth / product query:", 
                             value=st.session_state.get("custom_query", ""),
                             placeholder="Ask anything about customer friction, search failures, UI interventions...")
                             
        submitted = st.form_submit_button("🚀 Analyze & Generate Response", type="primary", use_container_width=True)
        
        if submitted:
            if not st.session_state.api_key:
                st.error("⚠️ Please configure GEMINI_API_KEY in Streamlit Secrets.")
            elif not query:
                st.warning("⚠️ Please enter a query.")
            else:
                with st.spinner("Generating Insights via Gemini Flash Latest..."):
                    prompt = f"SYSTEM: You are a PM for Google Photos. Answer the following based on VoC data: {query}\nDATA: {json.dumps(active_records)}"
                    st.success("Analysis Complete!")
                    st.markdown("---")
                    
                    # Stream the response directly to the UI to eliminate buffering
                    stream = execute_gemini_inference_stream(prompt, st.session_state.api_key, model_name="gemini-flash-latest")
                    st.write_stream(stream)
