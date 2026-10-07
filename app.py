import os
import json
import streamlit as st
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


st.set_page_config(
    page_title="AI Email Sorting",
    page_icon="📧",
    layout="centered"
)

st.title("📧 AI Email Sorting")

st.write(
    "Enter a customer email below. "
    "The AI will classify the email and extract customer information."
)

subject = st.text_input(
    "Email subject",
    placeholder="Example: Kan inte ringa"
)

email_text = st.text_area(
    "Customer email",
    placeholder="Write or paste the customer email here...",
    height=180
)

if st.button("Analyze email"):

    if not subject.strip() and not email_text.strip():
        st.warning("Please enter an email subject or email text.")

    else:
        with st.spinner("Analyzing email..."):
            try:
                result = analyze_email(subject, email_text)

                st.success("Email analyzed successfully")

                st.subheader("Result")

                st.write("**Category:**", result["category"])

                customer_number = result["customer_number"]
                phone_number = result["phone_number"]

                st.write(
                    "**Customer number:**",
                    customer_number if customer_number else "Not found"
                )

                st.write(
                    "**Phone number:**",
                    phone_number if phone_number else "Not found"
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")