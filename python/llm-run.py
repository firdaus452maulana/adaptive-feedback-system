import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Ollama


# Prompt Template
def build_prompt(input_json):
    template = (
        "You are an AI Assistant specialized in exercise coaching and motivation. "
        "Your task is to provide feedback and personalized motivational messages based on the user's performance analysis and their personal details. "
        "Consider the user's goals, preferences, and history to make the feedback effective and tailored to their needs. "
        "Use the data provided in the JSON format below:\n\n"
        "{input_json}\n\n"
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
        "Provide detailed feedback for each failed repetition in the 'Squat Performance Analysis'. Example:\n"
        "- Repetition 0: [Feedback about the issue and how to fix it.]\n"
        "#### Motivation Section:\n"
        "Craft motivational messages based on their personal data. Example:\n"
        "- 'Your goal to improve cardiovascular fitness and mental health is inspiring! Remember, every small effort counts toward this long-term journey.'\n"
        "#### Safety Note Section:\n"
        "Provide a safety or health-related recommendation based on the 'Medical History and Physical Condition' data. Example:\n"
        "- 'Since you have a history of major injuries and respiratory issues, consult with a medical professional before attempting advanced movements.'"
    )
    return template.format(input_json=json.dumps(input_json, indent=4))


# Main Execution
def main():
    # Initialize the Ollama LLM
    llm = Ollama(model="llama-3.1")

    # Sample input JSON
    input_data = {
        "Case ID": 1,
        "User Personalization": {
            "User Identification": {
                "Name": "User_1",
                "Age": 23,
                "Gender": "Female",
                "Height": 190,
                "Weight": 79
            },
            "Exercise Objectives": {
                "Main Objective": [
                    "Improve cardiovascular fitness",
                    "Improve mental health"
                ],
                "Timeframe": "More than 12 months",
                "Past Goals": "Yes",
                "Past Goals Result": "N/A"
            },
            "Discipline & Exercise Habits": {
                "Weekly Frequency": "1 time",
                "Duration": "30-60 minutes",
                "Regular Schedule": "Yes",
                "Consistency Difficulty": "Neutral"
            },
            "Exercise Preferences": {
                "Preferred Exercise": [
                    "Home workouts",
                    "Yoga or Pilates"
                ],
                "Group Preference": "Large group",
                "Variety Importance": "Not too important"
            },
            "Progress and Achievements": {
                "Participated Structured Program": "Yes",
                "Progress Result": "N/A",
                "Greatest Achievement": "Gained 3 kg of muscle mass in 10 months"
            },
            "Intrinsic and Extrinsic Motivation": {
                "Main Reason": [
                    "For physical appearance"
                ],
                "Motivation Type": "Both in balance",
                "Support Need": "No"
            },
            "Mental Health and Emotions": {
                "Emotional State": "Good",
                "Stress Level": "Sometimes",
                "Exercise Helps Stress": "Yes"
            },
            "Social Support": {
                "Supportive Friends/Family": "No",
                "Training with Others": "Rarely",
                "Support Importance": "Quite important"
            },
            "Medical History and Physical Condition": {
                "Injury History": "Major injury",
                "Current Medication": "Yes",
                "Respiratory/Cardiovascular Issues": "Yes"
            }
        },
        "Squat Performance Analysis": [
            {"repetition": 0, "state": "FAILED", "feedback": []},
            {"repetition": 1, "state": "FAILED", "feedback": []},
            {"repetition": 2, "state": "FAILED", "feedback": []},
            {"repetition": 3, "state": "FAILED", "feedback": []},
            {"repetition": 4, "state": "FAILED", "feedback": []},
            {"repetition": 5, "state": "FAILED", "feedback": []},
            {"repetition": 6, "state": "FAILED", "feedback": []}
        ]
    }

    # Build the prompt
    prompt = build_prompt(input_data)

    # Use LangChain's LLMChain to generate a response
    chain = LLMChain(llm=llm, prompt=PromptTemplate(template=prompt, input_variables=[]))
    response = chain.run({})

    print(response)


if __name__ == "__main__":
    main()
