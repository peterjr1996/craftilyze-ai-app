import os
import requests
import streamlit as st

# Use local backend while building.
# Later, when you want to test against Render, change the default below
# to your Render URL or set API_BASE_URL in your environment.
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Craftilyze",
    page_icon="◆",
    layout="wide"
)

# ---------- Session State ----------
if "custom_schedule" not in st.session_state:
    st.session_state.custom_schedule = []

if "reflection_text" not in st.session_state:
    st.session_state.reflection_text = ""

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "wake_time": "",
        "priorities": "",
        "fixed_commitments": "",
        "best_focus_window": "",
        "schedule_feel": "Balanced",
        "avoid_patterns": ""
    }

# ---------- Helpers ----------
def safe_get(url):
    try:
        response = requests.get(url, timeout=90)
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, str(e)

def safe_post(url, json_data=None):
    try:
        response = requests.post(url, json=json_data, timeout=120)
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, str(e)

def parse_schedule_text_to_blocks(schedule_text):
    parsed = []
    lines = schedule_text.split("\n")
    for line in lines:
        if " - " in line:
            parts = line.split(" - ", 1)
            parsed.append({
                "time": parts[0].strip(),
                "task": parts[1].strip()
            })
        elif "-" in line:
            parts = line.split("-", 1)
            parsed.append({
                "time": parts[0].strip(),
                "task": parts[1].strip()
            })
    return parsed

def render_schedule_blocks(blocks):
    for item in blocks:
        st.markdown(
            f'<div class="schedule-item"><strong>{item["time"]}</strong> — {item["task"]}</div>',
            unsafe_allow_html=True
        )

def profile_priorities_list():
    raw = st.session_state.user_profile.get("priorities", "").strip()
    if not raw:
        return []
    return [p.strip() for p in raw.split(",") if p.strip()]

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
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    }

    .schedule-item {
        background: rgba(30, 41, 59, 0.9);
        border-radius: 14px;
        padding: 0.8rem 0.9rem;
        margin-bottom: 0.55rem;
        border-left: 4px solid #818cf8;
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

    .small-pill {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.18);
        color: #c7d2fe;
        font-size: 0.85rem;
        margin-right: 0.45rem;
        margin-bottom: 0.45rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.title("Craftilyze")
st.sidebar.caption("Craft your schedule. Analyze your outcome.")

page = st.sidebar.radio(
    "Navigate",
    ["Today", "Build", "Reflect", "Tomorrow", "Settings"]
)

# Sidebar quick summary
st.sidebar.markdown("---")
st.sidebar.markdown("**Current setup**")
if st.session_state.user_profile["wake_time"]:
    st.sidebar.caption(f"Start time: {st.session_state.user_profile['wake_time']}")
if st.session_state.user_profile["schedule_feel"]:
    st.sidebar.caption(f"Day feel: {st.session_state.user_profile['schedule_feel']}")
if profile_priorities_list():
    st.sidebar.caption("Priorities:")
    for item in profile_priorities_list()[:4]:
        st.sidebar.write(f"• {item}")

# ---------- TODAY ----------
if page == "Today":
    st.markdown("""
    <div class="hero">
        <h1 style="margin:0;">Craft your schedule. Analyze your outcome.</h1>
        <p class="muted" style="margin-top:0.5rem;">
            Build around what matters, reflect honestly, and refine tomorrow with insight.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        schedule_count = len(st.session_state.custom_schedule)
        st.markdown(f"""
        <div class="metric-card">
            <div class="muted">Current Schedule Items</div>
            <h2>{schedule_count}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        priorities_count = len(profile_priorities_list())
        st.markdown(f"""
        <div class="metric-card">
            <div class="muted">Current Priorities</div>
            <h2>{priorities_count}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        reflection_saved = "Yes" if st.session_state.reflection_text.strip() else "No"
        st.markdown(f"""
        <div class="metric-card">
            <div class="muted">Reflection Saved</div>
            <h2>{reflection_saved}</h2>
        </div>
        """, unsafe_allow_html=True)

    left, right = st.columns([1.35, 1])

    with left:
        st.subheader("Today's Flow")

        if st.session_state.custom_schedule:
            render_schedule_blocks(st.session_state.custom_schedule)
        else:
            schedule, schedule_error = safe_get(f"{API_BASE_URL}/schedule")
            if schedule_error:
                st.error(schedule_error)
            else:
                render_schedule_blocks(schedule)

    with right:
        st.subheader("Current Priorities")

        priorities = profile_priorities_list()
        if priorities:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            for item in priorities:
                st.markdown(f'<div class="small-pill">{item}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card">
                <p class="muted">
                    No personal priorities saved yet. Go to Build and use “Generate one for me”
                    to shape the app around what matters to you.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("Your Rhythm")
        st.markdown(f"""
        <div class="card">
            <p><strong>Wake time:</strong> {st.session_state.user_profile.get("wake_time") or "Not set"}</p>
            <p><strong>Best focus window:</strong> {st.session_state.user_profile.get("best_focus_window") or "Not set"}</p>
            <p><strong>Desired day feel:</strong> {st.session_state.user_profile.get("schedule_feel") or "Not set"}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- BUILD ----------
elif page == "Build":
    st.subheader("Build Your Day")

    mode = st.radio(
        "Choose how you want to plan",
        ["Create my own schedule", "Generate one for me", "Refine an existing one"],
        horizontal=True
    )

    if mode == "Create my own schedule":
        st.markdown("### Add a schedule item")

        col1, col2 = st.columns([1, 2])

        with col1:
            time_input = st.text_input("Time", placeholder="08:30")

        with col2:
            task_input = st.text_input("Task", placeholder="Client work")

        if st.button("Add to Schedule"):
            if time_input and task_input:
                st.session_state.custom_schedule.append({
                    "time": time_input,
                    "task": task_input
                })
                st.success("Added to your schedule.")
            else:
                st.warning("Enter both a time and a task.")

        st.markdown("### Your Schedule")
        if st.session_state.custom_schedule:
            render_schedule_blocks(st.session_state.custom_schedule)
        else:
            st.info("No schedule items yet.")

    elif mode == "Generate one for me":
        st.markdown("### Personal Inputs")

        wake_time = st.text_input(
            "When do you usually start your day?",
            value=st.session_state.user_profile.get("wake_time", "07:30")
        )

        priorities = st.text_area(
            "What matters most right now?",
            value=st.session_state.user_profile.get("priorities", ""),
            placeholder="Example: finish client work, make time for reading, protect family time, keep my evenings lighter",
            height=120
        )

        fixed_commitments = st.text_area(
            "What parts of your day are fixed?",
            value=st.session_state.user_profile.get("fixed_commitments", ""),
            placeholder="Example: work 9-5, school pickup at 3:30 PM, dinner with family at 7 PM",
            height=120
        )

        best_focus_window = st.text_input(
            "When do you usually focus best?",
            value=st.session_state.user_profile.get("best_focus_window", ""),
            placeholder="Example: 10:00 AM - 1:00 PM"
        )

        schedule_feel = st.selectbox(
            "How do you want the day to feel?",
            ["Balanced", "Focused", "Flexible", "Light", "Structured"],
            index=["Balanced", "Focused", "Flexible", "Light", "Structured"].index(
                st.session_state.user_profile.get("schedule_feel", "Balanced")
            ) if st.session_state.user_profile.get("schedule_feel", "Balanced") in ["Balanced", "Focused", "Flexible", "Light", "Structured"] else 0
        )

        avoid_patterns = st.text_area(
            "What should this plan avoid?",
            value=st.session_state.user_profile.get("avoid_patterns", ""),
            placeholder="Example: long idle gaps, hard tasks late at night, too many transitions",
            height=120
        )

        if st.button("Generate Suggested Day"):
            st.session_state.user_profile = {
                "wake_time": wake_time,
                "priorities": priorities,
                "fixed_commitments": fixed_commitments,
                "best_focus_window": best_focus_window,
                "schedule_feel": schedule_feel,
                "avoid_patterns": avoid_patterns
            }

            payload = {
                "wake_time": wake_time,
                "priorities": priorities,
                "fixed_commitments": fixed_commitments,
                "best_focus_window": best_focus_window,
                "schedule_feel": schedule_feel,
                "avoid_patterns": avoid_patterns
            }

            result, error = safe_post(f"{API_BASE_URL}/generate_schedule", json_data=payload)

            if error:
                st.error(error)
            else:
                if "generated_schedule" in result:
                    st.session_state.custom_schedule = parse_schedule_text_to_blocks(result["generated_schedule"])
                    st.success("Your personalized schedule is ready.")
                else:
                    st.error(result)

        if st.session_state.custom_schedule:
            st.markdown("### Suggested Schedule")
            render_schedule_blocks(st.session_state.custom_schedule)

    elif mode == "Refine an existing one":
        existing_schedule_text = st.text_area(
            "Paste your schedule",
            placeholder="07:30 - Wake up\n08:30 - Client work\n10:00 - Reading\n12:30 - Lunch",
            height=180
        )

        if st.button("Save Existing Schedule"):
            st.session_state.custom_schedule = parse_schedule_text_to_blocks(existing_schedule_text)
            st.success("Existing schedule saved.")

        if st.session_state.custom_schedule:
            st.markdown("### Current Saved Schedule")
            render_schedule_blocks(st.session_state.custom_schedule)

# ---------- REFLECT ----------
elif page == "Reflect":
    st.subheader("Analyze Your Outcome")

    day_rating = st.selectbox("How did today go?", ["Great", "Okay", "Bad"])
    energy = st.selectbox("Energy level", ["High", "Medium", "Low"])
    what_worked = st.text_area(
        "What worked?",
        placeholder="Example: I stayed focused when I started with one clear priority."
    )
    what_didnt = st.text_area(
        "What didn’t work?",
        placeholder="Example: too many transitions in the afternoon broke momentum."
    )

    if st.button("Save Reflection"):
        st.session_state.reflection_text = f"""
Day rating: {day_rating}
Energy level: {energy}
What worked: {what_worked}
What didn't work: {what_didnt}
"""
        st.success("Reflection saved.")

# ---------- TOMORROW ----------
elif page == "Tomorrow":
    st.subheader("Tomorrow, Refined")

    reflection = st.text_area(
        "What should improve tomorrow?",
        value=st.session_state.reflection_text,
        height=150
    )

    if st.button("Build Tomorrow"):
        schedule_to_use = st.session_state.custom_schedule

        if not schedule_to_use:
            schedule_to_use, error = safe_get(f"{API_BASE_URL}/schedule")
            if error:
                st.error(error)
                schedule_to_use = None

        if schedule_to_use:
            payload = {
                "schedule": schedule_to_use,
                "feedback": reflection
            }

            result, error = safe_post(f"{API_BASE_URL}/adjust_schedule", json_data=payload)

            if error:
                st.error(error)
            else:
                if "adjusted_schedule" in result:
                    adjusted_blocks = parse_schedule_text_to_blocks(result["adjusted_schedule"])
                    st.markdown("### Tomorrow's Refined Plan")
                    render_schedule_blocks(adjusted_blocks)
                else:
                    st.error(result)

# ---------- SETTINGS ----------
elif page == "Settings":
    st.subheader("Settings")
    st.markdown(f"""
    <div class="card">
        <p><strong>Current API base:</strong> {API_BASE_URL}</p>
        <p class="muted">
            While developing locally, keep this on <code>http://127.0.0.1:8000</code>.
            Later, switch it to your Render backend.
        </p>
    </div>
    """, unsafe_allow_html=True)