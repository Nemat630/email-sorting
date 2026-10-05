import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)


def analyze_email(subject, text):
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

Definitions:
- invoice: billing, charges, payments, incorrect invoice amounts
- cancellation: ending or cancelling a subscription
- plan_change: changing subscription, data amount, or plan
- technical_issue: an existing problem with calls, SMS, mobile data, coverage, or service not working correctly
- number_transfer: keeping or transferring an existing phone number
- other: general service questions, eSIM, SIM cards, opening hours, or anything that does not fit the categories above

Rules:
- Return only valid JSON.
- Do not add explanations.
- Do not invent information.
- customer_number must contain the customer number if one appears.
- phone_number must contain the phone number if one appears.
- If a value is missing, use null.
- If there are multiple issues, choose the main reason for contact.

Email subject:
{subject}

Email text:
{text}
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


print("=== Email Sorting Demo ===")

subject = input("Enter email subject: ")

print("\nEnter email text:")
text = input()

result = analyze_email(subject, text)

print("\n=== Result ===")
print(json.dumps(result, ensure_ascii=False, indent=2))