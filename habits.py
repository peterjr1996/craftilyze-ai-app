# habits.py
habits = {
    "gym": False,
    "reading": False,
    "prayer": False,
    "study": False,
    "sleep": False
}

def complete_habit(habit):
    if habit in habits:
        habits[habit] = True
    return habits