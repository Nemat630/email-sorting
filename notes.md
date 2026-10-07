# Step 3 – Preparation

## 1. What does the AI need to know in the prompt?

The AI needs to know the allowed categories and what each category means.

The categories are:

- invoice
- cancellation
- plan_change
- technical_issue
- number_transfer
- other

The AI should also receive the email subject and email text.

It should be told to choose the category that best represents the customer's main reason for contacting the company.

For emails that contain more than one issue, the AI should choose the main or most important issue.

## 2. How do we make sure the AI answers with exactly one category?

The prompt should clearly tell the AI:

- Return only one category.
- Use only one of the allowed category names.
- Do not add explanations.
- Do not create new categories.

For example:

Return exactly one of these values:

invoice, cancellation, plan_change, technical_issue, number_transfer, other

## 3. What should happen if the AI returns something unexpected?

The Python program should check the AI response against the list of allowed categories.

If the response is not one of the allowed categories, the program should treat it as invalid.

Possible handling could be:

- classify it as "other", or
- return "invalid" and log the response for review.

For this project, using "invalid" during testing is better because it makes errors easier to find.