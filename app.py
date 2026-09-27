"""
Google Photos Memory Retrieval Intelligence Engine
Internal PM Intelligence Tool — Streamlit Native Application
Target: Google Photos Core Experience & Semantic Search Product Managers
"""

import streamlit as st
from corpus import default_python_corpus_store
from gemini_service import build_workflow_prompt, execute_gemini_inference, optimize_for_slides

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
# Google Material 3 Design System & Custom CSS
# ==============================================================================
MATERIAL_CSS = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500;600&family=Roboto:ital,wght@0,400;0,500;0,700;1,400&display=swap');

/* Reset and Global Typography */
html, body, [class*="css"], [class*="st-"] {
    font-family: 'Roboto', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #202124;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #202124 !important;
    font-weight: 600 !important;
}

/* Material 3 App Header */
.gp-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #ffffff;
    border-bottom: 1px solid #dadce0;
    padding: 12px 20px;
    margin-top: -50px;
    margin-bottom: 24px;
    border-radius: 8px;
    box-shadow: 0 1px 2px rgba(60, 64, 67, 0.08);
}

.gp-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.gp-titles {
    display: flex;
    flex-direction: column;
}

.gp-title {
    font-size: 17px;
    font-weight: 600;
    color: #202124;
    letter-spacing: -0.2px;
}

.gp-subtitle {
    font-size: 11.5px;
    color: #80868b;
}

.gp-badges {
    display: flex;
    align-items: center;
    gap: 8px;
}

.gp-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 11.5px;
    font-weight: 500;
    line-height: 1;
}

.gp-chip-slate {
    background-color: #f1f3f4;
    color: #5f6368;
    border: 1px solid #dadce0;
}

.gp-chip-blue {
    background-color: #e8f0fe;
    color: #1a73e8;
    border: 1px solid #aecbfa;
}

.gp-chip-green {
    background-color: #e6f4ea;
    color: #137333;
    border: 1px solid #ceead6;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
}

.dot-green { background-color: #34a853; box-shadow: 0 0 0 2px rgba(52, 168, 83, 0.2); }
.dot-gray { background-color: #9aa0a6; }

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
    border-right: 1px solid #dadce0;
    padding: 1rem 0.75rem;
}

[data-testid="stSidebar"] .stMarkdown h3 {
    font-size: 14px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #5f6368 !important;
    margin-top: 10px;
    margin-bottom: 4px;
}

/* Sidebar Cards */
.sidebar-panel {
    background-color: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 14px;
    box-shadow: 0 1px 2px rgba(60, 64, 67, 0.05);
}

.sidebar-panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}

.sidebar-panel-title {
    font-size: 13.5px;
    font-weight: 600;
    color: #202124;
    display: flex;
    align-items: center;
    gap: 6px;
}

.sidebar-panel-subtitle {
    font-size: 11px;
    color: #80868b;
    margin-bottom: 10px;
}

/* Workflow Trigger Buttons */
div.stButton > button {
    width: 100%;
    text-align: left !important;
    display: flex !important;
    justify-content: flex-start !important;
    background-color: #ffffff !important;
    border: 1px solid #dadce0 !important;
    border-radius: 10px !important;
    padding: 12px 14px !important;
    color: #202124 !important;
    font-weight: 500 !important;
    transition: all 150ms ease !important;
    box-shadow: 0 1px 2px rgba(60, 64, 67, 0.04) !important;
    margin-bottom: 8px !important;
}

div.stButton > button:hover {
    border-color: #1a73e8 !important;
    background-color: #fafbfc !important;
    box-shadow: 0 2px 6px rgba(26, 115, 232, 0.15) !important;
    transform: translateY(-1px);
}

div.stButton > button:active {
    background-color: #e8f0fe !important;
    transform: translateY(0);
}

/* Canvas Header */
.canvas-header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 18px;
    background-color: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 10px;
    margin-bottom: 18px;
    box-shadow: 0 1px 2px rgba(60, 64, 67, 0.05);
}

.canvas-header-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.workflow-badge-tag {
    font-size: 10.5px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    background-color: #f1f3f4;
    color: #5f6368;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.canvas-header-title {
    font-size: 15px;
    font-weight: 600;
    color: #202124;
}

/* IDLE View Presentation */
.idle-box {
    background: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 12px;
    padding: 32px 28px;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(60, 64, 67, 0.08);
}

.idle-pinwheel-hero {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 68px;
    height: 68px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(232, 240, 254, 0.8), rgba(254, 239, 195, 0.8));
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(60, 64, 67, 0.15);
}

.idle-heading {
    font-size: 22px;
    font-weight: 600;
    color: #202124;
    margin-bottom: 8px;
}

.idle-subtext {
    max-width: 620px;
    margin: 0 auto 20px auto;
    font-size: 14px;
    color: #5f6368;
    line-height: 1.6;
}

.idle-callout {
    background-color: #e8f0fe;
    border: 1px solid #aecbfa;
    border-radius: 8px;
    padding: 12px 18px;
    text-align: left;
    font-size: 13px;
    color: #174ea6;
    line-height: 1.5;
    margin-bottom: 24px;
}

.workflow-card-mini {
    background-color: #f8f9fa;
    border: 1px solid #dadce0;
    border-radius: 10px;
    padding: 14px;
    text-align: left;
    height: 100%;
}

.workflow-card-mini-title {
    font-size: 13.5px;
    font-weight: 600;
    color: #202124;
    margin-bottom: 6px;
}

.workflow-card-mini-desc {
    font-size: 12px;
    color: #5f6368;
    line-height: 1.45;
}

/* Verbatim Blockquote and Report Styling */
blockquote {
    border-left: 4px solid #1a73e8 !important;
    background-color: #f8f9fa !important;
    padding: 12px 18px !important;
    border-radius: 0 8px 8px 0 !important;
    font-style: italic !important;
    color: #3c4043 !important;
    margin: 14px 0 !important;
}

/* Footer Bar */
.gp-footer {
    border-top: 1px solid #dadce0;
    padding: 14px 20px;
    font-size: 11.5px;
    color: #80868b;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 40px;
}
</style>
"""
st.markdown(MATERIAL_CSS, unsafe_allow_html=True)

# Authentic Google Photos 4-Color Pinwheel SVG
PINWHEEL_SVG_32 = """
<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M16 4C11.5817 4 8 7.58172 8 12C8 16.4183 11.5817 16 16 16V4Z" fill="#EA4335"/>
  <path d="M28 16C28 11.5817 24.4183 8 20 8C15.5817 8 16 11.5817 16 16H28Z" fill="#FBBC04"/>
  <path d="M16 28C20.4183 28 24 24.4183 24 20C24 15.5817 20.4183 16 16 16V28Z" fill="#34A853"/>
  <path d="M4 16C4 20.4183 7.58172 24 12 24C16.4183 24 16 20.4183 16 16H4Z" fill="#1A73E8"/>
</svg>
"""

PINWHEEL_SVG_48 = """
<svg width="44" height="44" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M16 4C11.5817 4 8 7.58172 8 12C8 16.4183 11.5817 16 16 16V4Z" fill="#EA4335"/>
  <path d="M28 16C28 11.5817 24.4183 8 20 8C15.5817 8 16 11.5817 16 16H28Z" fill="#FBBC04"/>
  <path d="M16 28C20.4183 28 24 24.4183 24 20C24 15.5817 20.4183 16 16 16V28Z" fill="#34A853"/>
  <path d="M4 16C4 20.4183 7.58172 24 12 24C16.4183 24 16 20.4183 16 16H4Z" fill="#1A73E8"/>
</svg>
"""

# ==============================================================================
# Top Navigation Bar
# ==============================================================================
st.markdown(
    f"""
    <div class="gp-navbar">
        <div class="gp-brand">
            <div style="display: flex; align-items: center;">
                {PINWHEEL_SVG_32}
            </div>
            <div class="gp-titles">
                <div class="gp-title">Google Photos Memory Retrieval Intelligence Engine</div>
                <div class="gp-subtitle">Personal Search & Semantic Discovery • Core PM Intelligence Tool</div>
            </div>
        </div>
        <div class="gp-badges">
            <span class="gp-chip gp-chip-slate">Core PM Tool v1.0</span>
            <span class="gp-chip gp-chip-blue">Gemini 1.5 Flash (Temp: 0.2)</span>
            <span class="gp-chip gp-chip-green">
                <span class="status-dot dot-green"></span>
                Ready (Streamlit Native)
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# In-Memory Session State Initialization
if "api_key" not in st.session_state:
    default_key = ""
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            default_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        default_key = ""
    st.session_state.api_key = default_key

if "active_workflow" not in st.session_state:
    st.session_state.active_workflow = None

if "report_markdown" not in st.session_state:
    st.session_state.report_markdown = None

# ==============================================================================
# Left Control Sidebar (30% Width Ratio in Desktop Grid)
# ==============================================================================
with st.sidebar:
    st.markdown("### Control & Configuration")

    # Card 1: API Key Configuration Panel
    st.markdown(
        """
        <div class="sidebar-panel">
            <div class="sidebar-panel-header">
                <span class="sidebar-panel-title">🔑 API Key Configuration</span>
            </div>
            <div class="sidebar-panel-subtitle">Zero-trust runtime memory lifecycle (never persisted to disk)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    api_key_input = st.text_input(
        "Google AI Studio Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="Paste AI Studio Key (AIzaSy...)",
        help="Held strictly in runtime memory. Never saved to local storage, cookies, or external databases.",
        label_visibility="collapsed",
    )

    clean_key = api_key_input.strip().strip("'\"")
    st.session_state.api_key = clean_key

    # Status indicator
    if clean_key:
        st.markdown(
            '<div style="font-size: 11.5px; color: #137333; display: flex; align-items: center; gap: 6px; margin-bottom: 14px;">'
            '<span class="status-dot dot-green"></span> Key Configured (In-Memory Only) • 🔒 Secure'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="font-size: 11.5px; color: #80868b; display: flex; align-items: center; gap: 6px; margin-bottom: 14px;">'
            '<span class="status-dot dot-gray"></span> No Key Entered (Memory Only)'
            '</div>',
            unsafe_allow_html=True,
        )

    # Card 2: Corpus Source Filter Panel
    st.markdown(
        """
        <div class="sidebar-panel">
            <div class="sidebar-panel-header">
                <span class="sidebar-panel-title">📊 Corpus Source Filter</span>
            </div>
            <div class="sidebar-panel-subtitle">Active multi-channel customer conversations</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_src1, col_src2 = st.columns([3, 1])
    with col_src1:
        src_reddit = st.checkbox("r/GooglePhotos (Reddit)", value=True, key="src_reddit")
    with col_src2:
        st.markdown('<span style="font-size:11px; color:#5f6368; line-height:2.4;">3 recs</span>', unsafe_allow_html=True)

    col_src3, col_src4 = st.columns([3, 1])
    with col_src3:
        src_playstore = st.checkbox("Google Play Store", value=True, key="src_playstore")
    with col_src4:
        st.markdown('<span style="font-size:11px; color:#5f6368; line-height:2.4;">1 rec</span>', unsafe_allow_html=True)

    col_src5, col_src6 = st.columns([3, 1])
    with col_src5:
        src_appstore = st.checkbox("Apple App Store", value=True, key="src_appstore")
    with col_src6:
        st.markdown('<span style="font-size:11px; color:#5f6368; line-height:2.4;">1 rec</span>', unsafe_allow_html=True)

    col_src7, col_src8 = st.columns([3, 1])
    with col_src7:
        src_support = st.checkbox("Google Support Forum", value=True, key="src_support")
    with col_src8:
        st.markdown('<span style="font-size:11px; color:#5f6368; line-height:2.4;">2 recs</span>', unsafe_allow_html=True)

    # Calculate active records using in-memory CorpusStore
    source_filters = {
        "r/GooglePhotos": src_reddit,
        "Play Store": src_playstore,
        "App Store": src_appstore,
        "Google Support Forum": src_support,
    }
    active_records = default_python_corpus_store.get_active_records(source_filters)
    active_records_count = len(active_records)
    total_records_count = len(default_python_corpus_store.get_all_records())

    if active_records_count > 0:
        st.markdown(
            f'<div style="font-size:11.5px; font-weight:600; color:#1a73e8; background:#e8f0fe; padding:4px 10px; border-radius:12px; display:inline-block; margin-bottom:18px;">'
            f'Active: {active_records_count} of {total_records_count} Records Ingested</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="font-size:11.5px; font-weight:600; color:#c5221f; background:#fce8e6; padding:4px 10px; border-radius:12px; display:inline-block; margin-bottom:18px;">'
            '⚠️ 0 Sources Selected (Select at least 1)</div>',
            unsafe_allow_html=True,
        )

    # Card 3: Standardized Analytical Workflows
    st.markdown(
        """
        <div class="sidebar-panel">
            <div class="sidebar-panel-header">
                <span class="sidebar-panel-title">⚡ Analytical Workflows</span>
            </div>
            <div class="sidebar-panel-subtitle">Deterministic prompts • Beyond review summarization</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Workflow 1
    if st.button("🏷️ 01. Taxonomy of 'Lost' Photos", use_container_width=True, key="btn_wf1"):
        st.session_state.active_workflow = {
            "id": "taxonomy",
            "tag": "Edge Cases",
            "title": "Taxonomy of 'Lost' Photos",
            "desc": "Isolates high-friction search failure edge-cases grounded in real user quotes.",
        }

    # Workflow 2
    if st.button("📊 02. Cognitive Gap Matrix", use_container_width=True, key="btn_wf2"):
        st.session_state.active_workflow = {
            "id": "cognitive_gap",
            "tag": "T-Chart",
            "title": "Cognitive Gap Matrix",
            "desc": "Deconstructs episodic human memory anchors vs. rigid system index demands.",
        }

    # Workflow 3
    if st.button("⚙️ 03. Behavioral Workarounds", use_container_width=True, key="btn_wf3"):
        st.session_state.active_workflow = {
            "id": "workarounds",
            "tag": "Friction Scores",
            "title": "Behavioral Workarounds",
            "desc": "Maps manual compensatory actions with High/Medium/Low friction ratings.",
        }

    # Workflow 4
    if st.button("🚀 04. Product Opportunity Synthesis", use_container_width=True, key="btn_wf4"):
        st.session_state.active_workflow = {
            "id": "poa",
            "tag": "POAs & Matrix",
            "title": "Product Opportunity Synthesis",
            "desc": "Synthesizes 2 POAs + mandatory Comparison and Trade-off Matrix.",
        }

# ==============================================================================
# Main Reading Canvas (70% Width Ratio in Desktop Grid)
# ==============================================================================
active_wf = st.session_state.active_workflow
badge_tag = active_wf["tag"] if active_wf else "IDLE"
workflow_title = active_wf["title"] if active_wf else "Awaiting Workflow Selection"

# Canvas Header Bar
st.markdown(
    f"""
    <div class="canvas-header-bar">
        <div class="canvas-header-left">
            <span class="workflow-badge-tag">{badge_tag}</span>
            <span class="canvas-header-title">{workflow_title}</span>
        </div>
        <div>
            <span style="font-size: 12px; color: #5f6368;">
                {active_records_count} Records Active • Gemini 1.5 Flash
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Canvas Content Surface
if active_wf is None:
    # IDLE State Presentation
    st.markdown(
        f"""
        <div class="idle-box">
            <div class="idle-pinwheel-hero">
                {PINWHEEL_SVG_48}
            </div>
            <div class="idle-heading">Google Photos Memory Retrieval Intelligence Engine</div>
            <div class="idle-subtext">
                Deconstruct human memory retrieval failures & bridge the <strong>Semantic-Episodic Gap</strong> using empirical Voice-of-Customer feedback and conversations at scale.
            </div>
            <div class="idle-callout">
                💡 <strong>Deterministic RAG Pipeline — Not a Chatbot:</strong>
                Select one of the 4 standardized analytical workflows in the left sidebar to execute structured, low-temperature prompt directives against real user data.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4 Workflow Overview Cards in 2x2 Grid
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown(
            """
            <div class="workflow-card-mini">
                <div class="workflow-card-mini-title">🏷️ 01. Taxonomy of "Lost" Photos</div>
                <div class="workflow-card-mini-desc">
                    Isolates search failure edge-cases (incidental screenshots, situational vibes, relative-temporal queries) with direct verbatim user citations.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="workflow-card-mini">
                <div class="workflow-card-mini-title">⚙️ 03. Behavioral Workarounds</div>
                <div class="workflow-card-mini-desc">
                    Catalogs brute-force compensatory patterns (Person Pivot, External App Audit, Chronological Scrubbing) with explicit friction scores.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_w2:
        st.markdown(
            """
            <div class="workflow-card-mini">
                <div class="workflow-card-mini-title">📊 02. Cognitive Gap Matrix</div>
                <div class="workflow-card-mini-desc">
                    Generates a structured 3-column T-Chart comparing retained human episodic anchors against rigid system metadata demands.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="workflow-card-mini">
                <div class="workflow-card-mini-title">🚀 04. Product Opportunity Synthesis</div>
                <div class="workflow-card-mini-desc">
                    Synthesizes 2 high-impact POAs with testable hypotheses, concluded by a side-by-side Comparison & Trade-off Matrix.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

else:
    # Selected Workflow State
    if active_records_count == 0:
        st.error("⚠️ **No Active Data Sources**: Please check at least one feedback source in the sidebar to feed data to the engine.")
    elif not clean_key:
        st.warning("⚠️ **Gemini API Key Required**: Enter your Google AI Studio API key in the left sidebar to execute this analytical workflow.")
    else:
        col_exec1, col_exec2 = st.columns([3, 1])
        with col_exec1:
            st.info(f"**Selected Workflow:** {active_wf['title']} — *{active_wf['desc']}*")
        with col_exec2:
            trigger_synthesis = st.button("▶️ Execute Synthesis", type="primary", use_container_width=True, key="btn_exec_synthesis")

        # If user clicks synthesize
        if trigger_synthesis:
            with st.spinner(f"Synthesizing {active_wf['title']} at Temperature 0.2 against {active_records_count} records..."):
                prompt = build_workflow_prompt(active_wf["id"], active_records)
                result = execute_gemini_inference(prompt, clean_key)

                if result["success"]:
                    st.session_state.report_markdown = result["data"]
                    st.success("✓ Synthesis Complete! See consultant-grade structured report below.")
                else:
                    st.session_state.report_markdown = None
                    st.error(result["error"])

        # Display rendered report if available
        if st.session_state.report_markdown:
            st.markdown("---")
            st.markdown(st.session_state.report_markdown)
            st.markdown("---")

            # Phase 6: Slide Export & Clipboard Controls
            st.markdown("#### 📤 Export Deliverable for Google Slides & Docs")
            col_exp1, col_exp2 = st.columns(2)

            slide_text = optimize_for_slides(st.session_state.report_markdown)

            with col_exp1:
                st.download_button(
                    label="📊 Download for Google Slides (.txt)",
                    data=slide_text,
                    file_name=f"google_photos_{active_wf['id']}_slides.txt",
                    mime="text/plain",
                    help="Optimized for Google Slides: formatted headers, clean quotes, and tab-delimited tables that paste directly into slide table cells.",
                    use_container_width=True,
                )

            with col_exp2:
                st.download_button(
                    label="📄 Download Raw Markdown (.md)",
                    data=st.session_state.report_markdown,
                    file_name=f"google_photos_voc_{active_wf['id']}_report.md",
                    mime="text/markdown",
                    help="Full executive Markdown report suitable for PRDs, Google Docs, and GitHub issues.",
                    use_container_width=True,
                )

            with st.expander("📋 View Plaintext Formatted for Google Slides (Click to copy text)", expanded=False):
                st.text_area(
                    "Slide Formatted Text",
                    value=slide_text,
                    height=240,
                    help="Copy this text to paste directly into Google Slides or Google Docs text boxes without garbled characters.",
                )

        # Inspect Assembled Prompt (Auditability for PMs)
        with st.expander("🛠️ Inspect Assembled System Prompt & Injected Payload", expanded=False):
            raw_prompt = build_workflow_prompt(active_wf["id"], active_records)
            st.code(raw_prompt, language="markdown")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
with st.expander(f"📁 Ingested VoC Ground Truth Corpus ({active_records_count} Active / {total_records_count} Total Records)", expanded=False):
    for rec in active_records:
        meta = rec["metadata"]
        meta_details = []
        if meta.get("rating"):
            meta_details.append(f"⭐ Rating: {meta['rating']}/5")
        if meta.get("device"):
            meta_details.append(f"📱 Device: {meta['device']}")
        if meta.get("upvotes") is not None:
            meta_details.append(f"👍 Upvotes: {meta['upvotes']}")

        meta_str = " • ".join(meta_details)
        if meta_str:
            meta_str = f" • {meta_str}"

        tags_str = " ".join([f"`#{t}`" for t in meta.get("tags", [])])
        st.markdown(
            f"**`{rec['id']}`** — **{rec['source']}** ({rec['type']}) • *{meta.get('date', 'Unknown')}*{meta_str}\n\n"
            f"> \"{rec['content']}\"\n\n"
            f"🏷️ {tags_str}"
        )
        st.markdown("---")

# ==============================================================================
# Canvas Footer / Metadata Bar
# ==============================================================================
st.markdown(
    """
    <div class="gp-footer">
        <div>
            <strong>Grounding Corpus:</strong> 7 Ingested Multi-Channel Records (Reddit, Play Store, App Store, Google Support)
        </div>
        <div>
            <strong>Engine:</strong> Gemini 1.5 Flash (Temp: 0.2, Top_P: 0.8) • <strong>Security:</strong> Ephemeral Memory Lifecycle
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
