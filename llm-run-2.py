import json
import subprocess


def run_ollama(prompt_template, json_data, model="llama3.2:3b"):
    """
    Run the LLaMA model locally using Ollama with a specific prompt and JSON data.

    Parameters:
        prompt_template (str): The template for the prompt.
        json_data (dict): The JSON data to include in the prompt.
        model (str): The name of the model to use.

    Returns:
        str: The model's response.
    """
    # Format the JSON data as a string
    json_input = json.dumps(json_data, indent=4)

    output_template = (
        "### Instructions:\n"
        "1. Performance Feedback:\n"
        "   Analyze the 'Squat Performance Analysis' data and identify issues with the user's squat performance. Provide constructive feedback to improve their form or execution.\n"
        "2. Personalized Motivation:\n"
        "   Use the user's 'User Personalization' data to craft motivational messages.\n"
        "   - Reference their main exercise objectives to remind them of their long-term goals.\n"
        "   - Incorporate their exercise preferences to align motivation with what they enjoy.\n"
        "   - Acknowledge their greatest achievement to build confidence.\n"
        "3. Tone and Style:\n"
        "   - Keep your tone positive, empathetic, and encouraging.\n"
        "   - Use simple language, avoiding overly technical terms unless necessary.\n"
        "4. Health Considerations:\n"
        "   Respect the user's medical history and suggest modifications if needed, ensuring the exercise is safe and sustainable.\n\n"
        "### Expected Output Format:\n"
        "#### Feedback Section:\n"
        "Provide detailed feedback and how to improve in each feedback section for each failed/improper repetition in the 'Squat Performance Analysis'. Example:\n"
        "- Repetition 0: [Feedback about the issue and how to fix it.]\n"
        "#### Motivation Section:\n"
        "Craft motivational messages based on their personal data. Example:\n"
        "- 'Your goal to improve cardiovascular fitness and mental health is inspiring! Remember, every small effort counts toward this long-term journey.'\n"
        "#### Safety Note Section:\n"
        "Provide a safety or health-related recommendation based on the 'Medical History and Physical Condition' data. Example:\n"
        "- 'Since you have a history of major injuries and respiratory issues, consult with a medical professional before attempting advanced movements.'"
    )

    # output_template = (
    #     "### Instructions:\n"
    #     "1. Performance Feedback:\n"
    #     "   Analyze the 'Squat Performance Analysis' data and identify issues with the user's squat performance. Provide constructive feedback to improve their form or execution.\n"
    #     "2. Personalized Motivation:\n"
    #     "   Use the user's 'User Personalization' data to craft motivational messages.\n"
    #     "   - Reference their main exercise objectives to remind them of their long-term goals.\n"
    #     "   - Incorporate their exercise preferences to align motivation with what they enjoy.\n"
    #     "   - Acknowledge their greatest achievement to build confidence.\n"
    #     "3. Tone and Style:\n"
    #     "   - Keep your tone positive, empathetic, and encouraging.\n"
    #     "   - Use simple language, avoiding overly technical terms unless necessary.\n"
    #     "4. Health Considerations:\n"
    #     "   Respect the user's medical history and suggest modifications if needed, ensuring the exercise is safe and sustainable.\n\n"
    #     "5. Output Format:\n"
    #     "   Return the output as a JSON object with the following keys:\n"
    #     "   - 'Feedback': A list of objects, where each object corresponds to a repetition from the input, containing:\n"
    #     "       - 'Repetition': The repetition number.\n"
    #     "       - 'State': The state ('FAILED' or 'CORRECT').\n"
    #     "       - 'Feedback': Feedback text for 'FAILED' repetitions, and 'None' for 'CORRECT'.\n"
    #     "   - 'Motivation': A string containing personalized motivational text.\n"
    #     "   - 'SafetyNote': A string with safety recommendations based on the user's medical history.\n"
    #     "6. Explanation of JSON Keys:\n"
    #     "   - 'Feedback': A detailed list of feedback for each repetition.\n"
    #     "       - 'Repetition': The index of the repetition being analyzed.\n"
    #     "       - 'State': Indicates whether the repetition was 'FAILED' or 'CORRECT'.\n"
    #     "       - 'Feedback': Constructive feedback and corrective measures for 'FAILED' repetitions.\n"
    #     "   - 'Motivation': A personalized motivational message that encourages the user based on their exercise goals and preferences.\n"
    #     "   - 'SafetyNote': A health-related suggestion to ensure safe exercise practices based on medical history."
    #     "\n"
    #     "### Expected JSON Output Format:\n"
    #     "{\n"
    #     "    \"Feedback\": [\n"
    #     "        {\n"
    #     "            \"Repetition\": 0,\n"
    #     "            \"State\": \"FAILED\",\n"
    #     "            \"Feedback\": \"Your knees are bending inward; try to keep them aligned with your toes.\"\n"
    #     "        },\n"
    #     "    ],\n"
    #     "    \"Motivation\": \"Your goal to improve cardiovascular fitness and mental health is inspiring! Remember, every small effort counts toward this long-term journey.\",\n"
    #     "    \"SafetyNote\": \"Since you have a history of major injuries and respiratory issues, consult with a medical professional before attempting advanced movements.\"\n"
    #     "}"
    # )

    # Combine the prompt template with the JSON input
    prompt = f"{prompt_template}\n\n{json_input}\n\n{output_template}"

    # Run the Ollama command
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running the model: {e.stderr}"


if __name__ == "__main__":
    # Define the prompt template
    PROMPT_TEMPLATE = (
        "You are an AI Assistant specialized in exercise coaching and motivation. "
        "Your task is to provide feedback and personalized motivational messages based on the user's performance analysis and their personal details. "
        "Consider the user's goals, preferences, and history to make the feedback effective and tailored to their needs. "
        "You should only provide the output in JSON format and should not add any other information such as other words."
        "Use the data provided in the JSON format below:"
    )

    # Example JSON input
    JSON_INPUT = {
        "User Personalization": {
            "User Identification": {
                "Name": "Miyu_9",
                "Age": 51,
                "Gender": "Female",
                "Height": 156,
                "Weight": 68
            },
            "Exercise Objectives": {
                "Main Objective": [
                    "Lose weight"
                ],
                "Timeframe": "More than 12 months",
                "Past Goals": "Yes",
                "Past Goals Result": "Achieved"
            },
            "Discipline & Exercise Habits": {
                "Weekly Frequency": "1 time",
                "Duration": "30-60 minutes",
                "Regular Schedule": "Yes",
                "Consistency Difficulty": "Somewhat easy"
            },
            "Exercise Preferences": {
                "Preferred Exercise": [
                    "Cardio",
                    "Yoga or Pilates"
                ],
                "Group Preference": "Large group",
                "Variety Importance": "Very important"
            },
            "Progress and Achievements": {
                "Participated Structured Program": "Yes",
                "Progress Result": "Very good",
                "Greatest Achievement": "Lost 19 kg of weight in 2 months through consistent training"
            },
            "Intrinsic and Extrinsic Motivation": {
                "Main Reason": [
                    "To reduce stress or anxiety",
                    "For physical appearance"
                ],
                "Motivation Type": "External rewards",
                "Support Need": "Yes"
            },
            "Mental Health and Emotions": {
                "Emotional State": "Bad",
                "Stress Level": "Often",
                "Exercise Helps Stress": "Yes"
            },
            "Social Support": {
                "Supportive Friends/Family": "Yes",
                "Training with Others": "Sometimes",
                "Support Importance": "Not very important"
            },
            "Medical History and Physical Condition": {
                "Injury History": "Minor injury",
                "Current Medication": "Yes",
                "Respiratory/Cardiovascular Issues": "Yes"
            }
        },
        "Squat Performance Analysis": [
            {
                "repetition": 0,
                "state": "IMPROPER",
                "feedback": [
                    "Your back is leaning too forward",
                    "Your thighs drop too below your knees"
                ]
            },
            {
                "repetition": 1,
                "state": "CORRECT",
                "feedback": []
            },
            {
                "repetition": 2,
                "state": "CORRECT",
                "feedback": []
            },
            {
                "repetition": 3,
                "state": "CORRECT",
                "feedback": []
            },
            {
                "repetition": 4,
                "state": "FAILED",
                "feedback": [
                    "Your back is not forward enough"
                ]
            },
            {
                "repetition": 5,
                "state": "CORRECT",
                "feedback": []
            },
            {
                "repetition": 6,
                "state": "IMPROPER",
                "feedback": [
                    "Your back is leaning too forward"
                ]
            },
            {
                "repetition": 7,
                "state": "IMPROPER",
                "feedback": [
                    "Your back is leaning too forward",
                    "Your knees are too low, making them closer to your toes"
                ]
            },
            {
                "repetition": 8,
                "state": "CORRECT",
                "feedback": []
            },
            {
                "repetition": 9,
                "state": "IMPROPER",
                "feedback": [
                    "Your knees are too low, making them closer to your toes",
                    "Your back is leaning too forward"
                ]
            }
        ]
    }

    # Run the model
    response = run_ollama(PROMPT_TEMPLATE, JSON_INPUT)
    print(response)
