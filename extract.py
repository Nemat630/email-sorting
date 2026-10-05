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

category_correct = 0
customer_number_correct = 0
phone_number_correct = 0

for email in emails:
    result = analyze_email(email)

    predicted_category = result.get("category")
    predicted_customer_number = result.get("customer_number")
    predicted_phone_number = result.get("phone_number")

    category_match = predicted_category == email["correct_category"]

    customer_match = (
        predicted_customer_number
        == email["correct_customer_number"]
    )

    phone_match = (
        predicted_phone_number
        == email["correct_phone_number"]
    )

    if category_match:
        category_correct += 1

    if customer_match:
        customer_number_correct += 1

    if phone_match:
        phone_number_correct += 1

    output = {
        "id": email["id"],
        "subject": email["subject"],

        "predicted_category": predicted_category,
        "correct_category": email["correct_category"],
        "category_correct": category_match,

        "predicted_customer_number": predicted_customer_number,
        "correct_customer_number": email["correct_customer_number"],
        "customer_number_correct": customer_match,

        "predicted_phone_number": predicted_phone_number,
        "correct_phone_number": email["correct_phone_number"],
        "phone_number_correct": phone_match
    }

    results.append(output)

    print("-" * 60)
    print("ID:", email["id"])
    print("Subject:", email["subject"])

    print(
        "Category:",
        predicted_category,
        "| Correct:",
        email["correct_category"],
        "|",
        "CORRECT" if category_match else "WRONG"
    )

    print(
        "Customer number:",
        predicted_customer_number,
        "| Correct:",
        email["correct_customer_number"],
        "|",
        "CORRECT" if customer_match else "WRONG"
    )

    print(
        "Phone number:",
        predicted_phone_number,
        "| Correct:",
        email["correct_phone_number"],
        "|",
        "CORRECT" if phone_match else "WRONG"
    )


total = len(emails)

category_accuracy = category_correct / total * 100
customer_accuracy = customer_number_correct / total * 100
phone_accuracy = phone_number_correct / total * 100

print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)

print(
    f"Category accuracy: "
    f"{category_correct}/{total} = {category_accuracy:.2f}%"
)

print(
    f"Customer number accuracy: "
    f"{customer_number_correct}/{total} = {customer_accuracy:.2f}%"
)

print(
    f"Phone number accuracy: "
    f"{phone_number_correct}/{total} = {phone_accuracy:.2f}%"
)


with open("data/results.json", "w", encoding="utf-8") as file:
    json.dump(
        results,
        file,
        ensure_ascii=False,
        indent=2
    )

print("\nResults saved to data/results.json")