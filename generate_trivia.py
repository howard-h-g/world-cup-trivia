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

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4000,
    messages=[
        {
            "role": "user",
            "content": """Generate 25 expert-level World Cup trivia questions for a soccer coach who follows the sport obsessively. Cover tactics, coaching decisions, obscure records, specific match moments, and player details that casual fans wouldn't know.

Return ONLY a JSON array, no preamble, no markdown, no backticks. Each object must have exactly these fields:
- q: the question string
- opts: array of exactly 4 answer strings
- answer: integer index (0-3) of the correct answer
- category: one of Tactics, Coaching, Goals, Records, Moments, Legends, Goalkeepers, History
- fun: a 2-3 sentence follow-up fact that adds color beyond just confirming the answer

Example
