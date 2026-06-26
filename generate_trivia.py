import anthropic
import json
import re
import os
from datetime import date

today = date.today()
target = date(2026, 6, 26)

if today != target:
    print(f"Today is {today} — not the target date. Exiting without making any changes.")
    exit(0)

print(f"Target date confirmed: {today}. Generating questions...")

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

prompt = "Generate 10 expert-level World Cup trivia questions for a soccer coach who follows the sport obsessively. Cover tactics, coaching decisions, obscure records, specific match moments, and player details that casual fans wouldn't know. Return ONLY a JSON array, no preamble, no markdown, no backticks. Each object must have exactly these fields: q (the question string), opts (array of exactly 4 answer strings), answer (integer index 0-3 of the correct answer), category (one of Tactics, Coaching, Goals, Records, Moments, Legends, Goalkeepers, History), fun (a 2-3 sentence follow-up fact). Example format: [{\"q\":\"...\",\"opts\":[\"...\",\"...\",\"...\",\"...\"],\"answer\":0,\"category\":\"Tactics\",\"fun\":\"...\"}]"

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4000,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

raw = message.content[0].text.strip()
questions = json.loads(raw)

with open("index.html", "r") as f:
    html = f.read()

questions_js = json.dumps(questions, indent=2)
new_block = f"const questions = {questions_js};"

html = re.sub(r"const questions = \[.*?\];", new_block, html, flags=re.DOTALL)

with open("index.html", "w") as f:
    f.write(html)

print(f"Done — {len(questions)} questions written on {today}")
