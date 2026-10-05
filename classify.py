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

with open("data/emails_test.json", "r", encoding="utf-8") as file:
    emails = json.load(file)


def classify_email(email):
    prompt = f"""
You are a customer email classifier for a Swedish mobile operator.

Choose exactly ONE category:

invoice
cancellation
plan_change
technical_issue
number_transfer
other

Definitions:
- invoice: billing, charges, payments, incorrect invoice amounts
- cancellation: ending or cancelling a subscription
- plan_change: changing subscription, data amount, or plan
- technical_issue: an existing problem with calls, SMS, mobile data, coverage, or service not working correctly
- number_transfer: keeping or transferring an existing phone number
- other: general service questions that do not involve an active technical problem,
  including eSIM, SIM card options, opening hours, and general information
Rules:
- Return ONLY the category name.
- Return exactly one category.
- Do not explain your reasoning.
- If the email contains multiple issues, choose the main reason for contact.

Subject: {email["subject"]}
Text: {email["text"]}

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
    max_tokens=30,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    }
)

    prediction = response.choices[0].message.content.strip().lower()

    if prediction not in allowed_categories:
        for category in allowed_categories:
            if category in prediction:
                prediction = category
                break

    if prediction not in allowed_categories:
        prediction = "invalid"

    return prediction


correct_count = 0

for email in emails:
    prediction = classify_email(email)
    correct_category = email["correct_category"]

    is_correct = prediction == correct_category

    if is_correct:
        correct_count += 1

    print("-" * 60)
    print("ID:", email["id"])
    print("Subject:", email["subject"])
    print("Correct:", correct_category)
    print("Predicted:", prediction)
    print("Result:", "CORRECT" if is_correct else "WRONG")


total = len(emails)
accuracy = correct_count / total * 100

print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)
print("Correct predictions:", correct_count)
print("Total emails:", total)
print(f"Accuracy: {accuracy:.2f}%")