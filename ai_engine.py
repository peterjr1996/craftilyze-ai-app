# ai_engine.py
def analyze_day(rating):
    if rating == "great":
        return "Your schedule worked well. Keep similar structure tomorrow."
    if rating == "okay":
        return "We'll try improving focus blocks tomorrow."
    if rating == "bad":
        return "Let's adjust your schedule for more breaks."
    return "Thanks for the feedback."