import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

with open("data/emails.json", "r", encoding="utf-8") as file:
    emails = json.load(file)


def analyze_email(email):
    prompt = f"""
You are an email analysis system for a Swedish mobile operator.

Analyze the email and return ONLY valid JSON.

The JSON must contain exactly these fields:

category
customer_number
phone_number

Allowed categories:

invoice
cancellation
plan_change
technical_issue
number_transfer
other

Rules:
- customer_number should contain the customer number if it appears in the email.
- phone_number should contain the phone number if it appears in the email.
- If a value is missing, use null.
- Do not invent any numbers.
- Return only JSON.
- Do not add explanations.

Email subject:
{email["subject"]}

Email text:
{email["text"]}
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
        max_tokens=100,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        }
    )

    raw_response = response.choices[0].message.content.strip()

    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        return {
            "category": "invalid",
            "customer_number": None,
            "phone_number": None
        }


results = []

for email in emails:
    result = analyze_email(email)

    output = {
        "id": email["id"],
        "subject": email["subject"],
        "category": result["category"],
        "customer_number": result["customer_number"],
        "phone_number": result["phone_number"]
    }

    results.append(output)

    print("-" * 60)
    print("ID:", output["id"])
    print("Subject:", output["subject"])
    print("Category:", output["category"])
    print("Customer number:", output["customer_number"])
    print("Phone number:", output["phone_number"])


with open("data/results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False, indent=2)

print("\nResults saved to data/results.json")