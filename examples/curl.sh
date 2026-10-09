#!/bin/sh
# One call, three question types. Same request as the TypeSafe Jev API; only the URL (and no key) changes.
curl -s http://127.0.0.1:18766/v1/systemone -H 'Content-Type: application/json' -d '{
  "state": "Hi, I was charged twice for my last invoice. Can you refund the duplicate? This is a bit urgent.",
  "questions": {
    "intent":   {"type": "choice", "instructions": "What does the customer want?",
                 "criteria": {"refund": "money returned", "technical_help": "a bug or outage", "information": "general information", "cancellation": "wants to cancel"}},
    "urgency":  {"type": "score", "instructions": "How urgent does it sound?", "criteria": ["not urgent", "somewhat urgent", "urgent", "extremely urgent"]},
    "refund":   {"type": "noul",  "instructions": "Is the customer asking for money back?"}
  }}' | python3 -m json.tool
