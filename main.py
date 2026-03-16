# main.py
from fastapi import FastAPI
from scheduler import generate_daily_schedule
from goals import break_goal_into_actions
from habits import complete_habit
from ai_engine import analyze_day

app = FastAPI()

# Sample user data
user_data = {
    "wake_time": "07:30",
    "goals": ["Lose 20 pounds", "Learn Spanish", "Grow YouTube channel"]
}

@app.get("/")
def home():
    return {"app": "Craftilyze AI Scheduler"}

@app.get("/schedule")
def get_schedule():
    return generate_daily_schedule(user_data)

@app.get("/goals")
def get_goals():
    goal_actions = {}
    for goal in user_data["goals"]:
        goal_actions[goal] = break_goal_into_actions(goal)
    return goal_actions

@app.post("/habit/{habit}")
def mark_habit(habit):
    return complete_habit(habit)

@app.post("/daily_checkin/{rating}")
def daily_checkin(rating):
    return {"ai_feedback": analyze_day(rating)}
