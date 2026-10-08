
import streamlit as st
import pandas as pd

from src.api_client import fetch_dev_articles, merge_with_local_resources
from src.learning_logic import get_learning_profile
from src.recommender import rank_resources

st.set_page_config(
    page_title="StudyWise | Context-Aware Recommender",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    :root {
        --sw-purple: #6d4aff;
        --sw-indigo: #4f46e5;
        --sw-blue: #168cff;
        --sw-cyan: #12b8d6;
        --sw-teal: #11b5a4;
        --sw-pink: #ec4899;
        --sw-orange: #f59e0b;
        --sw-ink: #172554;
    }

    .block-container {
        padding-top: 1.1rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f7ff 0%, #eef5ff 55%, #f7fbff 100%);
        border-right: 1px solid #dfe5f5;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.1rem;
    }

    [data-testid="stSidebar"] .stRadio label {
        border-radius: 12px;
        padding: .38rem .55rem;
    }

    [data-testid="stSidebar"] .stButton button {
        border-radius: 13px;
        border: 0;
        background: linear-gradient(90deg, #6d4aff, #8b5cf6);
        color: white;
        font-weight: 750;
        box-shadow: 0 8px 20px rgba(109,74,255,.24);
    }

    /* Keep the light sidebar readable in BOTH Streamlit light and dark themes. */
    [data-testid="stSidebar"] {
        color: #172554 !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h4 {
        color: #172554 !important;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {
        color: #172554 !important;
        -webkit-text-fill-color: #172554 !important;
        background: #ffffff !important;
    }

    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] textarea::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] div[data-baseweb="select"],
    [data-testid="stSidebar"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #172554 !important;
    }

    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: #ffffff !important;
    }

    [data-testid="stSidebar"] div[data-baseweb="select"] input {
        color: #172554 !important;
        -webkit-text-fill-color: #172554 !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: #172554 !important;
    }

    [data-testid="stSidebar"] .stRadio label * {
        color: #172554 !important;
    }

    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #64748b !important;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: .7rem;
        padding: .15rem 0 .7rem;
    }

    .brand-icon {
        width: 43px;
        height: 43px;
        display: grid;
        place-items: center;
        border-radius: 13px;
        background: linear-gradient(135deg, #4f46e5, #8b5cf6);
        color: white;
        font-size: 1.45rem;
        box-shadow: 0 8px 20px rgba(79,70,229,.22);
    }

    .brand-name {
        font-size: 1.45rem;
        font-weight: 850;
        color: #172554;
        letter-spacing: -.03em;
    }

    .brand-name span {
        color: #6d4aff;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.1rem 2.2rem;
        border-radius: 25px;
        border: 1px solid rgba(255,255,255,.35);
        background:
            radial-gradient(circle at 92% 18%, rgba(255,255,255,.30) 0 7%, transparent 8%),
            radial-gradient(circle at 82% 78%, rgba(255,255,255,.16) 0 11%, transparent 12%),
            linear-gradient(110deg, #2636c9 0%, #5a38db 48%, #9b5de5 100%);
        color: white;
        margin-bottom: 1.25rem;
        box-shadow: 0 16px 34px rgba(79,70,229,.20);
    }

    .hero:after {
        content: "🎓   📚   ▶   💡   💻";
        position: absolute;
        right: 2rem;
        bottom: 1.25rem;
        font-size: 2.2rem;
        letter-spacing: .45rem;
        opacity: .78;
    }

    .hero-title {
        font-size: 2.35rem;
        font-weight: 850;
        line-height: 1.08;
        margin: 0;
        color: white;
        max-width: 760px;
        letter-spacing: -.035em;
    }

    .hero-subtitle {
        margin-top: .65rem;
        color: rgba(255,255,255,.86);
        font-size: 1.03rem;
        max-width: 760px;
    }

    .section-label {
        font-size: .78rem;
        text-transform: uppercase;
        letter-spacing: .12em;
        color: #dbeafe;
        font-weight: 800;
        margin-bottom: .45rem;
    }

    .mini-card {
        position: relative;
        overflow: hidden;
        padding: 1.05rem 1.15rem;
        border-radius: 18px;
        border: 1px solid rgba(99,102,241,.10);
        min-height: 118px;
        box-shadow: 0 8px 24px rgba(31,41,55,.07);
    }

    .mini-card:nth-child(1) { background: linear-gradient(135deg,#f0eaff,#e4ddff); }
    .mini-card:nth-child(2) { background: linear-gradient(135deg,#dcfff6,#d7f7ef); }
    .mini-card:nth-child(3) { background: linear-gradient(135deg,#fff0dc,#ffe7c4); }
    .mini-card:nth-child(4) { background: linear-gradient(135deg,#e2f2ff,#d9ecff); }

    .mini-title {
        font-size: .86rem;
        color: #64748b;
        margin-bottom: .2rem;
        font-weight: 650;
    }

    .mini-value {
        font-size: 1.48rem;
        font-weight: 850;
        color: #172554;
        letter-spacing: -.025em;
    }

    .feature {
        padding: 1.15rem 1.2rem;
        border-radius: 18px;
        border: 1px solid #e3e8f5;
        background: linear-gradient(145deg,#ffffff,#f8faff);
        height: 100%;
        box-shadow: 0 7px 20px rgba(31,41,55,.055);
    }

    .feature h4 {
        margin: .2rem 0 .35rem 0;
        color: #172554;
    }

    .feature p {
        color: #64748b;
        margin-bottom: 0;
        line-height: 1.5;
    }

    .score-pill {
        display: inline-block;
        padding: .3rem .65rem;
        border-radius: 999px;
        font-weight: 750;
        background: #eee9ff;
        color: #5b36d6;
        font-size: .84rem;
    }

    .resource-desc {
        color: #64748b;
        line-height: 1.55;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: .82rem;
        padding-top: 1.8rem;
    }

    /* Color the Streamlit bordered containers used for resources. */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 19px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 7px 22px rgba(30,41,59,.055);
        background: #ffffff;
    }

    /* Brighten primary controls and tabs/buttons. */
    .stLinkButton a, .stButton button {
        border-radius: 12px !important;
        font-weight: 700 !important;
    }

    .stLinkButton a {
        border: 1px solid #c4b5fd !important;
        color: #5b36d6 !important;
        background: #faf9ff !important;
    }

    .stLinkButton a:hover {
        background: #f0ebff !important;
        border-color: #8b5cf6 !important;
    }

    h1, h2, h3 {
        color: #172554;
        letter-spacing: -.025em;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# State
# -----------------------------
if "ranked" not in st.session_state:
    st.session_state.ranked = []
if "resources" not in st.session_state:
    st.session_state.resources = []
if "profile" not in st.session_state:
    st.session_state.profile = None
if "api_used" not in st.session_state:
    st.session_state.api_used = False
if "inputs" not in st.session_state:
    st.session_state.inputs = None

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">🎓</div>
            <div>
                <div class="brand-name">Study<span>Wise</span></div>
                <div style="color:#64748b;font-size:.76rem;">Context-Aware Study Resource Recommender</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🎯 Recommendations", "📚 Resource Explorer", "📈 Analytics", "🔗 API Integration", "ℹ️ About"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### 🎯 Learning Context")

    topic = st.text_input(
        "Topic",
        value=(st.session_state.inputs or {}).get("topic", ""),
        placeholder="e.g., Python, SQL, Machine Learning",
    )

    previous_score = st.number_input(
        "Previous Score (%)",
        min_value=0,
        max_value=100,
        value=int((st.session_state.inputs or {}).get("previous_score", 60)),
        step=1,
    )

    difficulty = st.selectbox(
        "Difficulty Level",
        ["Beginner", "Intermediate", "Advanced"],
        index=["Beginner", "Intermediate", "Advanced"].index(
            (st.session_state.inputs or {}).get("difficulty", "Beginner")
        ),
    )

    preferred_format = st.selectbox(
        "Preferred Learning Format",
        ["Video", "Article", "Documentation", "Practice", "Course"],
        index=["Video", "Article", "Documentation", "Practice", "Course"].index(
            (st.session_state.inputs or {}).get("preferred_format", "Video")
        ),
    )

    learning_goal = st.selectbox(
        "Learning Goal",
        ["Understand Concepts", "Improve Score", "Practice Problems", "Revision", "Advanced Learning"],
        index=["Understand Concepts", "Improve Score", "Practice Problems", "Revision", "Advanced Learning"].index(
            (st.session_state.inputs or {}).get("learning_goal", "Improve Score")
        ),
    )

    get_recommendations = st.button(
        "✨ Generate Recommendations",
        use_container_width=True,
        type="primary",
    )

    st.divider()
    st.caption("Python • Streamlit • REST API • JSON")
    st.caption("Explainable rule-based ranking")

# -----------------------------
# Recommendation generation
# -----------------------------
if get_recommendations:
    if not topic.strip():
        st.error("Please enter a topic first.")
        st.stop()

    st.session_state.inputs = {
        "topic": topic.strip(),
        "previous_score": previous_score,
        "difficulty": difficulty,
        "preferred_format": preferred_format,
        "learning_goal": learning_goal,
    }

    profile = get_learning_profile(
        previous_score, difficulty, preferred_format, learning_goal
    )

    with st.spinner("Finding and ranking personalized resources..."):
        live_articles = fetch_dev_articles(topic)
        resources, api_used = merge_with_local_resources(topic, live_articles)
        ranked = rank_resources(
            resources=resources,
            topic=topic,
            difficulty=difficulty,
            preferred_format=preferred_format,
            previous_score=previous_score,
            learning_goal=learning_goal,
            top_n=5,
        )

    st.session_state.profile = profile
    st.session_state.resources = resources
    st.session_state.ranked = ranked
    st.session_state.api_used = api_used
    st.session_state.inputs["api_status"] = (
        "Live DEV Community articles + local library"
        if api_used
        else "Local fallback library"
    )

    st.toast("Personalized recommendations are ready!", icon="🎯")

# -----------------------------
# Helpers
# -----------------------------
def render_hero(title, subtitle, eyebrow="STUDYWISE"):
    st.markdown(
        f"""
        <div class="hero">
            <div class="section-label">🎓 {eyebrow}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(title, value, caption=""):
    icons = {
        "Previous Score": "📊",
        "Performance": "🎯",
        "Difficulty": "📚",
        "Format": "🎥",
        "Level": "🧠",
        "Retrieved": "🌐",
        "Recommended": "⭐",
        "Score": "📈",
    }
    icon = icons.get(title, "✨")
    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-title">{icon} {title}</div>
            <div class="mini-value">{value}</div>
            <div class="mini-title">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_recommendations(items):
    if not items:
        st.info("No recommendations yet. Use the learning controls in the sidebar and generate recommendations.")
        return

    for i, item in enumerate(items, start=1):
        with st.container(border=True):
            left, right = st.columns([4.5, 1.2])

            with left:
                st.markdown(f"### {i}. {item['title']}")
                st.markdown(
                    f"<div class='resource-desc'>{item.get('description', 'No description available.')}</div>",
                    unsafe_allow_html=True,
                )
                st.caption(
                    f"📌 {item['resource_type']}   •   "
                    f"📚 {item['difficulty']}   •   "
                    f"🌐 {item['source']}"
                )

                with st.expander("🧠 Why was this recommended?"):
                    st.write(item["reason"])

            with right:
                st.metric("Match", f"{item['final_score']:.1f}/100")
                st.link_button("Open Resource ↗", item["url"], use_container_width=True)

# -----------------------------
# Pages
# -----------------------------
inputs = st.session_state.inputs
profile = st.session_state.profile
ranked = st.session_state.ranked
resources = st.session_state.resources

if page == "🏠 Dashboard":
    render_hero(
        "Learn smarter, not harder.",
        "Personalized study resources ranked around your topic, performance, difficulty, format, and learning goal.",
    )

    if not inputs or not profile:
        st.markdown("### 👋 Welcome")
        st.write(
            "Build a personalized learning path in a few seconds. Enter your learning context in the sidebar and generate recommendations."
        )

        st.markdown("### ✨ What this platform does")
        cols = st.columns(3)
        features = [
            ("🎯 Context-Aware", "Uses your current learning situation instead of showing the same resources to everyone."),
            ("🧠 Explainable Ranking", "Every recommendation receives a score based on clearly defined factors."),
            ("🌐 Live + Fallback", "Uses live DEV Community articles and a local resource library when the API is unavailable."),
        ]
        for col, (title, desc) in zip(cols, features):
            with col:
                st.markdown(
                    f"<div class='feature'><h4>{title}</h4><p>{desc}</p></div>",
                    unsafe_allow_html=True,
                )

        st.markdown("### 🔄 How it works")
        st.write("**1. Enter context → 2. Retrieve resources → 3. Score resources → 4. Rank → 5. Recommend**")

    else:
        st.markdown("### 📊 Your current learning snapshot")
        cols = st.columns(4)
        with cols[0]:
            render_metric_card("Previous Score", f"{inputs['previous_score']}%", "Current performance")
        with cols[1]:
            render_metric_card("Performance", profile["performance_level"], "Learning profile")
        with cols[2]:
            render_metric_card("Difficulty", inputs["difficulty"], "Target level")
        with cols[3]:
            render_metric_card("Format", inputs["preferred_format"], "Preferred format")

        st.markdown("### 🧭 Current learning context")
        st.info(
            f"**{inputs['topic']}** • {inputs['learning_goal']} • "
            f"{len(resources)} resources retrieved • "
            f"{'Live API + local library' if st.session_state.api_used else 'Local fallback library'}"
        )

        st.markdown("### 🏆 Top recommendations")
        show_recommendations(ranked[:3])

elif page == "🎯 Recommendations":
    render_hero(
        "Personalized Recommendations",
        "Resources are ranked using your learning context and the project's explainable scoring model.",
        "RECOMMENDATIONS",
    )

    if not ranked:
        st.info("Generate recommendations from the sidebar to see your personalized results.")
    else:
        st.success(
            f"Found {len(resources)} relevant resources and selected the top {len(ranked)} recommendations."
        )
        show_recommendations(ranked)

elif page == "📚 Resource Explorer":
    render_hero(
        "Resource Explorer",
        "Browse the resources retrieved for your selected topic.",
        "RESOURCE LIBRARY",
    )

    if not resources:
        st.info("Generate recommendations first to populate the resource explorer.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            type_options = ["All"] + sorted({x.get("resource_type", "Unknown") for x in resources})
            selected_type = st.selectbox("Filter by resource type", type_options)
        with col2:
            diff_options = ["All"] + sorted({x.get("difficulty", "Unknown") for x in resources})
            selected_diff = st.selectbox("Filter by difficulty", diff_options)

        filtered = [
            x for x in resources
            if (selected_type == "All" or x.get("resource_type") == selected_type)
            and (selected_diff == "All" or x.get("difficulty") == selected_diff)
        ]

        st.caption(f"Showing {len(filtered)} of {len(resources)} resources")

        for item in filtered:
            with st.container(border=True):
                a, b = st.columns([5, 1])
                with a:
                    st.markdown(f"### {item['title']}")
                    st.write(item.get("description", "No description available."))
                    st.caption(
                        f"📌 {item.get('resource_type', 'Resource')} • "
                        f"📚 {item.get('difficulty', 'Unknown')} • "
                        f"🌐 {item.get('source', 'Unknown')}"
                    )
                with b:
                    st.link_button("Open ↗", item["url"], use_container_width=True)

elif page == "📈 Analytics":
    render_hero(
        "Learning Analytics",
        "Understand how your context influences the recommendation results.",
        "ANALYTICS",
    )

    if not ranked or not profile:
        st.info("Generate recommendations first to view analytics.")
    else:
        cols = st.columns(4)
        with cols[0]:
            render_metric_card("Score", f"{inputs['previous_score']}%", "Previous result")
        with cols[1]:
            render_metric_card("Level", profile["performance_level"], "Performance band")
        with cols[2]:
            render_metric_card("Retrieved", len(resources), "Relevant resources")
        with cols[3]:
            render_metric_card("Recommended", len(ranked), "Top ranked")

        st.markdown("### 📊 Recommendation scores")
        chart_data = pd.DataFrame({
            "Resource": [f"#{i}" for i in range(1, len(ranked) + 1)],
            "Recommendation Score": [x["final_score"] for x in ranked],
        }).set_index("Resource")
        st.bar_chart(chart_data)

        st.markdown("### 🔍 Scoring breakdown")
        details = pd.DataFrame([
            {
                "Resource": x["title"],
                "Topic": x["topic_score"],
                "Difficulty": x["difficulty_score"],
                "Format": x["format_score"],
                "Performance": x["performance_score"],
                "Quality": x["quality_score"],
                "Final": x["final_score"],
            }
            for x in ranked
        ])
        st.dataframe(details, use_container_width=True, hide_index=True)

        st.caption(
            "Scoring weights: Topic 30% • Difficulty 20% • Format 20% • Performance 20% • Quality 10%"
        )

elif page == "🔗 API Integration":
    render_hero(
        "API Integration",
        "A dedicated space for the partner API workflow required for the lab counterpart integration.",
        "INTEGRATION",
    )

    st.markdown("### 🔄 Counterpart workflow")
    st.code(
        """Partner E-Learning Platform
          ↓
Student learning context (JSON)
          ↓
Your Recommendation API
          ↓
Context-aware scoring engine
          ↓
Personalized resources (JSON)
          ↓
Partner platform""",
        language="text",
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="feature">
                <h4>📥 Input context</h4>
                <p>Student/course context can include topic, difficulty, assessment score, progress, completed lessons, and preferred format.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="feature">
                <h4>📤 Recommendation response</h4>
                <p>The recommendation engine returns ranked learning resources with their type, score, explanation, and URL.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info(
        "Partner endpoint details will be connected here after the counterpart API specification is finalized."
    )

elif page == "ℹ️ About":
    render_hero(
        "About the Project",
        "An Advanced Python project for explainable, context-aware study resource recommendation.",
        "PROJECT",
    )

    st.markdown("### 🎓 Project Overview")
    st.write(
        "The system recommends study resources by considering a student's topic, previous performance, "
        "difficulty level, preferred learning format, and learning goal. It uses an explainable rule-based "
        "scoring and ranking approach rather than a machine-learning model."
    )

    st.markdown("### 🛠️ Technologies")
    cols = st.columns(4)
    tech = [
        ("🐍 Python", "Core application and recommendation logic"),
        ("⚡ Streamlit", "Interactive web interface"),
        ("🌐 Requests", "Live resource API communication"),
        ("🧪 Pytest", "Automated testing"),
    ]
    for col, (title, desc) in zip(cols, tech):
        with col:
            st.markdown(
                f"<div class='feature'><h4>{title}</h4><p>{desc}</p></div>",
                unsafe_allow_html=True,
            )

    st.markdown("### ⚖️ Recommendation Model")
    st.dataframe(
        pd.DataFrame(
            [
                ["Topic Relevance", "30%"],
                ["Difficulty Match", "20%"],
                ["Preferred Format", "20%"],
                ["Performance Match", "20%"],
                ["Resource Quality", "10%"],
            ],
            columns=["Factor", "Weight"],
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### 🔌 Resource retrieval")
    st.write(
        "Live resources are retrieved from the DEV Community public API. If the external API is unavailable, "
        "the application falls back to the local JSON resource library."
    )

st.markdown(
    "<div class='footer'>Context-Aware Study Resource Recommender • Advanced Python Programming Project</div>",
    unsafe_allow_html=True,
)
