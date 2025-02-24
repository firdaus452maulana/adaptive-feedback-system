import json
import subprocess
import ollama

PROMPT_TEMPLATE = """
    **Task**: Generate structured exercise feedback in JSON format based on the following data:
    
    ### Input Data
    1. User Profile:
    {user_personalization}
    
    2. Current Session Analysis:
    {squat_performance}
    
    3. Historical Feedback:
    {history_feedback}
    
    ### Instructions
    - Analyze ONLY repetitions with "IMPROPER" or "FAILED" states
    - For each problematic repetition:
      - Copy exact "repetition" number
      - Keep original "state" value
      - Combine all feedback points into one string separated by commas
    - Create 3 motivational messages addressing:
      1. Weight loss progress
      2. Consistency encouragement
      3. Specific form improvement
    - Safety note should reference respiratory/cardiovascular history
    
    ### Required Output Format:
    {{
      "performance_feedback": [
        {{
          "rep": <repetition_number>,
          "state": "<IMPROPER/FAILED>", 
          "details": "<combined_feedback>"
        }}
      ],
      "motivation": [
        "<message1>",
        "<message2>",
        "<message3>"
      ],
      "safety": "<custom_health_note>"
    }}
    
    ### Example Output:
    {{
      "performance_feedback": [
        {{
          "rep": 0,
          "state": "IMPROPER",
          "details": "Knees too low, Back not forward enough"
        }}
      ],
      "motivation": [
        "Your weight loss journey is inspiring...",
        "Remember your 19kg achievement...",
        "Focus on keeping knees aligned..."
      ],
      "safety": "Given your cardiovascular history..."
    }}
    
    Now generate response for the provided data:
    """


def run_ollama(prompt_template, model="deepseek-r1"):
    # Load and format JSON data
    with open('user_data.json') as f:
        data = json.load(f)

    # Format the prompt with actual data sections
    formatted_prompt = prompt_template.format(
        user_personalization=json.dumps(data['user_personalization'], indent=2),
        squat_performance=json.dumps(data['squat_performance'], indent=2),
        history_feedback=json.dumps(data['feedback_history'], indent=2)
    )

    # Add system message prefix
    full_prompt = f"""SYSTEM: You are a JSON output generator. Follow these rules:
    1. Use only provided data
    2. Maintain original numerical values
    3. Never invent new data
    4. Use exact field names from example
    
    USER: {formatted_prompt}"""

    # Run Ollama with adjusted parameters
    try:
        response = ollama.generate(
            model='deepseek-r1',
            prompt=prompt_template,
            options={
                'temperature': 0.5,
                'top_p': 0.9,
                'max_tokens': 35000,
                'repeat_penalty': 1.1
            }
        )
        print(response['response'])
        return response['response']
    except subprocess.CalledProcessError as e:
        print("error")
        return f"Error: {e.stderr}"


def validate_response(response):
    try:
        data = json.loads(response)
        required_fields = ['performance_feedback', 'motivation', 'safety']
        if not all(field in data for field in required_fields):
            return False
        return True
    except json.JSONDecodeError:
        return False


# In main execution
if __name__ == "__main__":
    response = run_ollama(PROMPT_TEMPLATE)
    if validate_response(response):
        print(response)
    else:
        print("Error: Invalid response format")
