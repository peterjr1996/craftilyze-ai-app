import streamlit as st
import requests

st.title("Craftilyze AI Planner")

# --- Daily Schedule ---
st.header("Your Daily Schedule")
schedule = requests.get("http://127.0.0.1:8000/schedule").json()
for item in schedule:
    st.write(f"{item['time']} — {item['task']}")

# --- Goals ---
st.header("Your Goals")
goals = requests.get("http://127.0.0.1:8000/goals").json()
for goal, actions in goals.items():
    st.subheader(goal)
    for action in actions:
        st.write(f"- {action}")

# --- Habit Tracker ---
st.header("Habit Tracker")
habit_names = ["gym", "reading", "prayer", "study", "sleep"]
completed_habits = {}

for habit in habit_names:
    checked = st.checkbox(habit.capitalize())
    if checked:
        requests.post(f"http://127.0.0.1:8000/habit/{habit}")
        completed_habits[habit] = True
    else:
        completed_habits[habit] = False

# --- Daily Check-In ---
st.header("Daily Check-In")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Great Day"):
        feedback = requests.post("http://127.0.0.1:8000/daily_checkin/great").json()
        st.write(feedback["ai_feedback"])

with col2:
    if st.button("Okay Day"):
        feedback = requests.post("http://127.0.0.1:8000/daily_checkin/okay").json()
        st.write(feedback["ai_feedback"])

with col3:
    if st.button("Bad Day"):
        feedback = requests.post("http://127.0.0.1:8000/daily_checkin/bad").json()
        st.write(feedback["ai_feedback"])