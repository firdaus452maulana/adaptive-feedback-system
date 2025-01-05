import random


# Function to generate "Greatest Achievement"
def generate_greatest_achievement():
    achievements = [
        "Successfully completed a 10 km run in under an hour",
        "Achieved a personal best squat of {} kg",
        "Lost {} kg of weight in {} months through consistent training",
        "Improved flexibility by being able to perform a full split",
        "Recovered fully from a major injury after consistent rehabilitation exercises",
        "Won first place in a local fitness competition",
        "Successfully performed {} consecutive push-ups",
        "Increased endurance by completing a {}-hour cycling session",
        "Gained {} kg of muscle mass in {} months",
        "Successfully maintained a regular exercise schedule for {} weeks without skipping a session"
    ]
    # Generate random parameters
    weight_loss = random.randint(5, 20)
    squat_weight = random.randint(50, 150)
    months = random.randint(1, 12)
    pushups = random.randint(20, 100)
    cycling_hours = random.randint(2, 8)
    muscle_gain = random.randint(1, 10)
    weeks_consistent = random.randint(4, 24)

    # Fill placeholders
    filled_achievements = [
        achievements[0],
        achievements[1].format(squat_weight),
        achievements[2].format(weight_loss, months),
        achievements[3],
        achievements[4],
        achievements[5],
        achievements[6].format(pushups),
        achievements[7].format(cycling_hours),
        achievements[8].format(muscle_gain, months),
        achievements[9].format(weeks_consistent)
    ]
    return random.choice(filled_achievements)


# Function to generate a single case
def generate_case(case_id):
    # Generate User Personalization
    user_personalization = {
        "User Identification": {
            "Name": f"User_{case_id}",
            "Age": random.randint(18, 60),
            "Gender": random.choice(["Male", "Female"]),
            "Height": random.randint(150, 200),
            "Weight": random.randint(50, 120),
        },
        "Exercise Objectives": {
            "Main Objective": random.sample([
                "Increase muscle strength",
                "Lose weight",
                "Improve cardiovascular fitness",
                "Improving flexibility",
                "Injury rehabilitation",
                "Preparing for competitions",
                "Improve mental health"
            ], random.randint(1, 3)),
            "Timeframe": random.choice(["1-3 months", "3-6 months", "6-12 months", "More than 12 months"]),
            "Past Goals": random.choice(["Yes", "No"]),
            "Past Goals Result": random.choice(["Achieved", "Failed", "N/A"])
        },
        "Discipline & Exercise Habits": {
            "Weekly Frequency": random.choice(["1 time", "2-3 times", "4-5 times", "Every day"]),
            "Duration": random.choice(["<30 minutes", "30-60 minutes", "60-90 minutes", ">90 minutes"]),
            "Regular Schedule": random.choice(["Yes", "No"]),
            "Consistency Difficulty": random.choice(
                ["Very difficult", "Somewhat difficult", "Neutral", "Somewhat easy", "Very easy"]),
        },
        "Exercise Preferences": {
            "Preferred Exercise": random.sample([
                "Weightlifting",
                "Cardio",
                "Yoga or Pilates",
                "HIIT",
                "Team sports",
                "Home workouts"
            ], random.randint(1, 3)),
            "Group Preference": random.choice(["Individual", "Small group", "Large group"]),
            "Variety Importance": random.choice(
                ["Very important", "Quite important", "Not too important", "Not important at all"]),
        },
        "Progress and Achievements": {
            "Participated Structured Program": random.choice(["Yes", "No"]),
            "Progress Result": random.choice(["Very good", "Good", "Fair", "Poor", "N/A"]),
            "Greatest Achievement": generate_greatest_achievement()
        },
        "Intrinsic and Extrinsic Motivation": {
            "Main Reason": random.sample([
                "For long-term health",
                "For physical appearance",
                "To reduce stress or anxiety",
                "To increase energy",
                "To gain social recognition"
            ], random.randint(1, 2)),
            "Motivation Type": random.choice(["External rewards", "Internal satisfaction", "Both in balance"]),
            "Support Need": random.choice(["Yes", "No", "Not sure"])
        },
        "Mental Health and Emotions": {
            "Emotional State": random.choice(["Very good", "Good", "Fair", "Bad", "Very bad"]),
            "Stress Level": random.choice(["Never", "Sometimes", "Often", "Very often"]),
            "Exercise Helps Stress": random.choice(["Yes", "No", "Not sure"]),
        },
        "Social Support": {
            "Supportive Friends/Family": random.choice(["Yes", "No"]),
            "Training with Others": random.choice(["Always", "Sometimes", "Rarely", "Never"]),
            "Support Importance": random.choice(
                ["Very important", "Quite important", "Not very important", "Not important at all"]),
        },
        "Medical History and Physical Condition": {
            "Injury History": random.choice(["None", "Minor injury", "Major injury"]),
            "Current Medication": random.choice(["Yes", "No"]),
            "Respiratory/Cardiovascular Issues": random.choice(["Yes", "No"]),
        },
    }

    # Generate Squat Performance
    squat_performance = []
    if case_id % 7 in [0, 1]:  # Special cases: all CORRECT or all FAILED
        state = "CORRECT" if random.random() > 0.5 else "FAILED"
        for i in range(random.randint(5, 10)):
            squat_performance.append({
                "repetition": i,
                "state": state,
                "feedback": []
            })
    else:
        for i in range(random.randint(5, 10)):
            state = random.choice(["CORRECT", "IMPROPER", "FAILED"])
            feedback = []
            if state != "CORRECT":
                feedback_pool = [
                    "Your back is leaning too forward",
                    "Your back is not forward enough",
                    "Your knees are too low, making them closer to your toes",
                    "Your thighs drop too below your knees"
                ]
                feedback = random.sample(feedback_pool, random.randint(1, 2))
                if "Your back is leaning too forward" in feedback and "Your back is not forward enough" in feedback:
                    feedback.remove("Your back is not forward enough")
            squat_performance.append({
                "repetition": i,
                "state": state,
                "feedback": feedback
            })

    return {
        "Case ID": case_id,
        "User Personalization": user_personalization,
        "Squat Performance Analysis": squat_performance
    }


# Function to generate multiple cases
def generate_cases(num_cases):
    cases = [generate_case(i) for i in range(1, num_cases + 1)]
    return cases


# Example usage
cases = generate_cases(1000)
for case in cases:
    print(case)
