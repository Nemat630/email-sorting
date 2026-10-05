import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

allowed_categories = [
    "invoice",
    "cancellation",
    "plan_change",
    "technical_issue",
    "number_transfer",
    "other"
]

with open("data/emails.json", "r", encoding="utf-8") as file:
    emails = json.load(file)

email = emails[0]

prompt = f"""
You are an email classification system.

Choose exactly ONE category from this list:

invoice
cancellation
plan_change
technical_issue
number_transfer
other

Rules:
- Reply with only the category name.
- Do not explain.
- Do not write a sentence.
- Do not add punctuation.
- Do not use any category outside the list.

Email subject:
{email["subject"]}

Email text:
{email["text"]}

Category:
"""

response = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0,
    max_tokens=20
)

prediction = response.choices[0].message.content.strip().lower()

if prediction not in allowed_categories:
    for category in allowed_categories:
        if category in prediction:
            prediction = category
            break
print("Subject:", email["subject"])
print("Correct:", email["correct_category"])
print("Predicted:", prediction)

if prediction in allowed_categories:
    print("Valid category: yes")
else:
    print("Valid category: no")