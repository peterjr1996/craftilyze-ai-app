def break_goal_into_actions(goal):
    if "lose" in goal.lower():
        return ["Gym 3x per week", "Walk daily", "Eat healthy"]
    if "learn" in goal.lower():
        return ["Study 30 mins daily", "Practice speaking", "Review notes"]
    if "grow" in goal.lower():
        return ["Upload content 3x/week", "Engage audience", "Analyze metrics"]
    return ["Break goal into actionable steps"]
    