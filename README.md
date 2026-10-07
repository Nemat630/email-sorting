# Customer Email Sorting with AI and Human Review

An automated workflow that reads incoming customer emails for a mobile operator,
classifies them by topic, extracts key information, and drafts a reply.
A human always reviews and approves before anything is sent.

## The problem

Customer service teams receive a large number of emails every day about invoices,
cancellations, plan changes and technical issues. Sorting them by hand and sending
them to the right team takes time, and emails that end up in the wrong place lead to
slower answers and frustrated customers. Many emails also lack the information needed
to handle them, which means extra back-and-forth with the customer.

This project automates the repetitive parts of that work, while keeping a person in
control of every reply that goes out.

## How it works

1. **Read** – Emails are loaded from a file (in a real setup, from an inbox).
2. **Classify** – A language model (Claude) assigns each email exactly one category.
   The answer is checked against the list of allowed categories, and anything
   unexpected is sent to manual review instead of being guessed.
3. **Extract** – The model pulls out key information such as customer number,
   phone number and what the customer wants, returned as structured JSON.
4. **Validate** – Rule-based checks make sure the extracted data is in the right
   format (e.g. a valid Swedish mobile number). Missing information is flagged.
5. **Draft a reply** – The model writes a reply suggestion. If information is missing,
   the draft asks the customer for it.
6. **Human review** – In a simple web interface, a reviewer sees the original email
   next to the category, extracted data and draft reply. They can edit, approve or
   reject. Every decision is logged.

## Categories

| Category | Description |
|---|---|
| Invoice | Questions or complaints about invoices and payments |
| Cancellation | The customer wants to end their subscription |
| Plan change | The customer wants to upgrade, downgrade or switch plans |
| Technical issue | Problems with coverage, data, calls or the SIM card |
| Number transfer | Moving a phone number to or from another operator |
| Other | Anything that doesn't fit the categories above |

## Results

Tested on 18 made-up emails with known correct categories, including vague
emails, emails covering two topics, and emails written in English.

| Metric | Result |
|---|---|
| Correct category | 18 of 18 (100%) |

All test emails were classified correctly. Since I wrote the test emails myself,
they are probably clearer than real customer emails, so this result shows that the
workflow works as intended, not that it would be perfect in production. The next
step is a larger and harder test set with spelling mistakes, very short emails and
more ambiguous cases, to find where the model starts making mistakes.


*All emails in this project are made up. No real customer data is used.*
