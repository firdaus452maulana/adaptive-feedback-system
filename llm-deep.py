import json
import os
from dotenv import load_dotenv
from openai import OpenAI

user_personalization = os.getenv("USER_PERSONAL")

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
    {user_personalization}
    
    History of squat training sessions:
    {history_squat_training_sessions}
    
    Current session of squat performance analysis:
    {current_session}
    
    Pre-exercise questionnaire:
    {preex_questionnaire}
    
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