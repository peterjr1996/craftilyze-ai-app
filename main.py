import os
import logging
from dotenv import load_dotenv
import openai
from fastapi import FastAPI
from pydantic import BaseModel

from personalized_scheduler import generate_personalized_schedule
from adaptive_scheduler import adjust_schedule
from scheduler import generate_daily_schedule
from goals import break_goal_into_actions
from habits import complete_habit
from ai_engine import analyze_day

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Default sample data used for the basic routes
user_data = {
    "wake_time": "07:30",
    "goals": ["Lose 20 pounds", "Learn Spanish", "Grow YouTube channel"]
}

class GenerateRequest(BaseModel):
    wake_time: str
    goals: list
    style: str
    preferences: str

class AdjustRequest(BaseModel):
    schedule: list
    feedback: str

@app.get("/")
def home():
    return {"app": "Craftilyze AI Scheduler"}

@app.get("/schedule")
def get_schedule():
    return generate_daily_schedule(user_data)

@app.get("/goals")
def get_goals():
    goal_actions = {goal: break_goal_into_actions(goal) for goal in user_data["goals"]}
    return goal_actions

@app.post("/habit/{habit}")
def mark_habit(habit: str):
    return complete_habit(habit)

@app.post("/daily_checkin/{rating}")
def daily_checkin(rating: str):
    return {"ai_feedback": analyze_day(rating)}

@app.post("/generate_schedule")
def generate_schedule(request: GenerateRequest):
    schedule = generate_personalized_schedule(
        request.wake_time,
        request.goals,
        request.style,
        request.preferences
    )
    return {"generated_schedule": schedule}

@app.post("/adjust_schedule")
def adjust_tomorrow(request: AdjustRequest):
    new_schedule = adjust_schedule(request.schedule, request.feedback)
    return {"adjusted_schedule": new_schedule}