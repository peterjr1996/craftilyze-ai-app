import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def generate_personalized_schedule(wake_time, goals, style, preferences):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "Missing OPENAI_API_KEY in .env file."

    client = OpenAI(api_key=api_key)

    prompt = f"""
Build a personalized daily schedule.

User wake time: {wake_time}
User goals: {', '.join(goals)}
Planning style: {style}
User preferences: {preferences}

Requirements:
- realistic
- balanced
- clear and practical
- should reflect the user's preferences
- avoid overload
- include time blocks

Return EXACTLY in this format:
05:00 - Wake up
05:30 - Morning routine
06:00 - Workout
07:00 - Breakfast
08:00 - Focus work
12:00 - Lunch
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You help users build practical daily schedules based on goals, preferences, and personal style."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content