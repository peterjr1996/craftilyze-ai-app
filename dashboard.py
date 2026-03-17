import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "https://craftilyze-ai-app.onrender.com")

st.set_page_config(
    page_title="Craftilyze",
    page_icon="◆",
    layout="wide"
)

# ---------- Helpers ----------
def safe_get(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, str(e)

def safe_post(url):
    try:
        response = requests.post(url, timeout=30)
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, str(e)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0b1020 0%, #111827 100%);
        color: #f8fafc;
    }

    .hero {
        padding: 1.6rem 1.8rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        margin-bottom: 1rem;
    }

    .card {
        background: rgba(17, 24, 39, 0.88);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 1rem 1rem 0.8rem 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    }

    .metric-card {
        background: rgba(17, 24, 39, 0.88);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    }

    .muted {
        color: #94a3b8;
        font-size: 0.95rem;
    }

    .schedule-item {
        background: rgba(30, 41, 59, 0.9);
        border-radius: 14px;
        padding: 0.8rem 0.9rem;
        margin-bottom: 0.55rem;
        border-left: 4px solid #818cf8;
    }

    .pill {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.18);
        color: #c7d2fe;
        font-size: 0.85rem;
        margin-bottom: 0.6rem;
    }

    .goal-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.title("Craftilyze")
st.sidebar.caption("Craft your schedule. Analyze your outcome.")

page = st.sidebar.radio(
    "Navigate",
    ["Today", "Goals", "Habits", "Reflection", "Tomorrow", "Settings"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Momentum**")
st.sidebar.progress(62)
st.sidebar.caption("A steady day builds a stronger week.")

# ---------- Load shared data ----------
schedule, schedule_error = safe_get(f"{API_BASE_URL}/schedule")
goals, goals_error = safe_get(f"{API_BASE_URL}/goals")

# ---------- TODAY ----------
if page == "Today":
    st.markdown("""
    <div class="hero">
        <div class="pill">Daily System</div>
        <h1 style="margin:0;">Craft your schedule. Analyze your outcome.</h1>
        <p class="muted" style="margin-top:0.5rem;">
            Build structure around your goals, track your consistency, and understand what actually works.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        count = len(schedule) if schedule and not schedule_error else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="muted">Today's Flow Items</div>
            <h2>{count}</h2>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        gcount = len(goals) if goals and not goals_error else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="muted">Goals in Progress</div>
            <h2>{gcount}</h2>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="muted">System Status</div>
            <h2>Live</h2>
        </div>
        """, unsafe_allow_html=True)

    left, right = st.columns([1.4, 1])

    with left:
        st.subheader("Today's Flow")
        if schedule_error:
            st.error(schedule_error)
        else:
            for item in schedule:
                st.markdown(
                    f"""
                    <div class="schedule-item">
                        <strong>{item['time']}</strong> — {item['task']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with right:
        st.subheader("Insight")
        st.markdown("""
        <div class="card">
            <div class="goal-title">Pattern to watch</div>
            <p class="muted">
                Your planner works best when the day feels structured but realistic.
                Use this space later for reflection-based guidance and tomorrow adjustments.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Quick Focus")
        focus_note = st.text_area(
            "What matters most today?",
            placeholder="Example: Finish my main work block, complete gym, and stay consistent.",
            height=130
        )
        if focus_note:
            st.success("Focus note saved for this session.")

# ---------- GOALS ----------
elif page == "Goals":
    st.subheader("Goals in Progress")

    if goals_error:
        st.error(goals_error)
    else:
        for idx, (goal, actions) in enumerate(goals.items(), start=1):
            progress = min(20 * idx, 95)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="goal-title">{goal}</div>', unsafe_allow_html=True)
            st.progress(progress)
            st.caption(f"Progress estimate: {progress}%")
            for action in actions:
                st.write(f"• {action}")
            st.markdown('</div>', unsafe_allow_html=True)

# ---------- HABITS ----------
elif page == "Habits":
    st.subheader("Consistency Tracker")
    st.caption("Use habits to measure rhythm, not perfection.")

    h1, h2 = st.columns(2)

    with h1:
        if st.button("Complete Gym", use_container_width=True):
            result, error = safe_post(f"{API_BASE_URL}/habit/gym")
            if error:
                st.error(error)
            else:
                st.success("Gym completed")

    with h2:
        if st.button("Complete Reading", use_container_width=True):
            result, error = safe_post(f"{API_BASE_URL}/habit/reading")
            if error:
                st.error(error)
            else:
                st.success("Reading completed")

    st.markdown("""
    <div class="card">
        <div class="goal-title">Consistency note</div>
        <p class="muted">
            The goal is not to build a perfect streak. The goal is to understand which behaviors help you move forward.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------- REFLECTION ----------
elif page == "Reflection":
    st.subheader("Daily Reflection")
    st.caption("Review the day without overreacting to it.")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Great", use_container_width=True):
            result, error = safe_post(f"{API_BASE_URL}/daily_checkin/great")
            if error:
                st.error(error)
            else:
                st.success(result["ai_feedback"])

    with c2:
        if st.button("Okay", use_container_width=True):
            result, error = safe_post(f"{API_BASE_URL}/daily_checkin/okay")
            if error:
                st.error(error)
            else:
                st.info(result["ai_feedback"])

    with c3:
        if st.button("Bad", use_container_width=True):
            result, error = safe_post(f"{API_BASE_URL}/daily_checkin/bad")
            if error:
                st.error(error)
            else:
                st.warning(result["ai_feedback"])

    st.text_area(
        "What influenced your outcome today?",
        placeholder="What helped? What got in the way? What should change tomorrow?",
        height=180
    )

# ---------- TOMORROW ----------
elif page == "Tomorrow":
    st.subheader("Tomorrow Preview")
    st.markdown("""
    <div class="card">
        <div class="goal-title">Next phase</div>
        <p class="muted">
            This section is where tomorrow adjustments, rebuilt schedules, and pattern-based suggestions will appear.
        </p>
        <p class="muted">
            We can wire this up next using your adaptive scheduler endpoint.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------- SETTINGS ----------
elif page == "Settings":
    st.subheader("Settings")
    st.markdown("""
    <div class="card">
        <div class="goal-title">Workspace</div>
        <p class="muted">This is where theme options, preferences, and future account settings can go.</p>
    </div>
    """, unsafe_allow_html=True)