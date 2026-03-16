import ast
import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_daily_schedule(user_data):
    wake_time = user_data["wake_time"]
    goals = user_data["goals"]
    habits = [habit for habit, done in user_data.get("habits", {}).items() if done]

    prompt = f"""
    Create a realistic daily schedule for a person with:
    - Wake up time: {wake_time}
    - Goals: {', '.join(goals)}
    - Completed habits: {', '.join(habits) if habits else 'none'}

    Return the schedule as a Python list of dictionaries like:
    [{{"time": "07:30", "task": "Wake up"}}, ...]
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        text = response["choices"][0]["message"]["content"]
        schedule = ast.literal_eval(text)

    except:
        schedule = [
            {"time": wake_time, "task": "Wake up"},
            {"time": "08:00", "task": "Breakfast"},
            {"time": "08:30", "task": "Gym (strength training)"},
            {"time": "10:00", "task": "Work block"},
            {"time": "12:30", "task": "Lunch"},
            {"time": "19:00", "task": "Evening wind down"}


    return schedule