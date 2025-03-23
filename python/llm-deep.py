import json
import os
from dotenv import load_dotenv
from openai import OpenAI

system_prompt = (
    """
    Based on the following context, create motivational messages/words to maintain and even increase the user's motivation to maintain the user's consistency in doing self-squat exercises to prevent the user from experiencing muscle weakness in old age.

    Keep your tone positive, empathetic, and encouraging. Generate the following data as the output that will be responded to:
    
    1. **performance_feedback**: Based on the current session of performance data from context, only list IMPROPER/FAILED reps. Provide constructive feedback to improve their form or execution. Focus on providing feedback in explaining the errors made by users based on the system pose analysis. IMPROPER is a Squat performed with an incorrect posture but is still considered a successful squat, while FAILED is a Squat that does not fulfill all the phases (Stand - Transition - Squat) required in one rep.
    2. **motivation**: Contains suggestions to maintain and increase the user's motivation to continue squat training based on the user's personalized data. Consider the Motivation that has been given to the user in the previous session along with the interaction provided by the user in creating the motivation message.
    3. **safety**: Provide a safety or health-related recommendation based on the health conditions data.
    4. **suggestion**: based on the analysis of the input data from the user, suggest to the user the composition of the number of reps that the user can perform for the next session. Make it clear to increase, decrease, or stick with maximizing performance.
    
    context:
    User Personalization:
    "User Personalization": [
      {"question": "Name", "answer": "Muhammad Irwan Yanwari"},
      {"question": "Age", "answer": "35 years"},
      {"question": "Gender", "answer": "Male"},
      {"question": "Height", "answer": "165 cm"},
      {"question": "Weight", "answer": "75 kg"},
      {"question": "Do you have prior experience with squat training?", "answer": "No"},
      {"question": "How often do you perform squat exercises per week?", "answer": "Never"},
      {"question": "How many squat repetitions do you usually perform in one training session?", "answer": "Less than 10"},
      {"question": "Do you have a fixed training routine or schedule?", "answer": "No"},
      {"question": "How difficult is it for you to exercise consistently? (Scale 1-5, 1 = very easy, 5 = very difficult)", "answer": "8"},
      {"question": "What other purposes do you have for squatting other than to prevent muscle weakening in old age?", "answer": "Increasing leg muscle strength"},
      {"question": "What usually motivates you to keep training?", "answer": ["Receiving support from others", "Achieving set goals"]},
      {"question": "How much do you rely on external motivation from a coach or system? (Scale 1-5, 1 = not at all, 5 = very much)", "answer": "1"},
      {"question": "What type of motivation is most effective for you?", "answer": "Socializing or not doing it alone"},
      {"question": "What is your biggest challenge in maintaining squat training consistency?", "answer": "Lack of motivation"},
      {"question": "How do you usually overcome these challenges?", "answer": "Find a friend to do it together"},
      {"question": "Do you have any injury history or health conditions that should be considered during squat exercises?", "answer": "No"},
      {"question": "Do you experience pain or discomfort while performing squats?", "answer": "Yes"},
      {"question": "How important is it for you to receive safety recommendations during training? (Scale 1-5, 1 = not important, 5 = very important)", "answer": "8"}
    ]
    
    History of squat training sessions:
    "History of Squat Training Session": []
    
    Current session of squat performance analysis:
    "Squat Performance Analysis": [
        {
            "repetition": 0,
            "state": "CORRECT",
            "mistakes": []
        },
        {
            "repetition": 1,
            "state": "FAILED",
            "mistakes": []
        },
        {
            "repetition": 2,
            "state": "FAILED",
            "mistakes": [
                "Your knees are too low, making them closer to your toes"
            ]
        },
        {
            "repetition": 3,
            "state": "FAILED",
            "mistakes": []
        },
        {
            "repetition": 4,
            "state": "CORRECT",
            "mistakes": []
        },
        {
            "repetition": 5,
            "state": "FAILED",
            "mistakes": [
                "Your knees are too low, making them closer to your toes"
            ]
        },
        {
            "repetition": 6,
            "state": "FAILED",
            "mistakes": []
        },
        {
            "repetition": 7,
            "state": "FAILED",
            "mistakes": []
        },
        {
            "repetition": 8,
            "state": "FAILED",
            "mistakes": []
        },
        {
            "repetition": 9,
            "state": "FAILED",
            "mistakes": []
        }
    ]
    
    Pre-exercise questionnaire:
    [
      {"question": "Do you have fever?", "answer": "No"},
      {"question": "Does your body feel sluggish?", "answer": "No"},
      {"question": "Did you get enough sleep yesterday?", "answer": "Yes"},
      {"question": "Do you have an appetite?", "answer": "Yes"},
      {"question": "Do you have diarrhoea?", "answer": "No"},
      {"question": "Do you have headache or chest pain?", "answer": "No"},
      {"question": "Are there any joint pains?", "answer": "No"},
      {"question": "Are you overworked?", "answer": "No"},
      {"question": "Are you still tired from your last sporting event?", "answer": "Yes"},
      {"question": "How motivated are you to exercise today?", "answer": "5"}
    ]
    
    ONLY OUTPUT RAW JSON. Use this structure:
    {
        "performance_feedback": str,
        "motivation": str,
        "safety": str,
        "susggestion": str
    }
    """
)

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API"),
    base_url="https://api.deepseek.com",
)

messages = [{"role": "user", "content": system_prompt}]

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)

print(response)
print(response.choices[0].message.content)
print(response.choices[0].message.reasoning_content)
# print(json.loads(response.choices[0].message.content))