import json
import requests

# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = 'llama3.1'  # TODO: update this for whatever model you wish to use


def generate(prompt, context):
    r = requests.post('http://localhost:11434/api/generate',
                      json={
                          'model': model,
                          'prompt': prompt,
                          'context': context,
                      },
                      stream=True)
    r.raise_for_status()

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        # the response streams one token at a time, print that as we receive it
        print(response_part, end='', flush=True)

        if 'error' in body:
            raise Exception(body['error'])

        if body.get('done', False):
            return body['context']


def main():
    # context = []  # the context stores a conversation history, you can use this to make the model more context aware
    # while True:
    #     user_input = input("Enter a prompt: ")
    #     if not user_input:
    #         exit()
    #     print()
    #     context = generate(user_input, context)
    #     print()
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
    print(JSON_INPUT)


if __name__ == "__main__":
    main()
