import json

with open("data/emails.json", "r", encoding="utf-8") as file:
    emails = json.load(file)

for email in emails:
    print(email["subject"], "->", email["correct_category"])