"""Minimal client (standard library only). Works against Dex and, with a key and the JEV URL, against the Jev API: the request and answers are the same."""
import json
import urllib.request

URL = "http://127.0.0.1:18766/v1/systemone"


def decide(state, questions, url=URL, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=json.dumps({"state": state, "questions": questions}).encode(), headers=headers)
    return json.load(urllib.request.urlopen(req, timeout=60))["answers"]


if __name__ == "__main__":
    a = decide("Our nightly backup failed again and the last good copy is three days old.",
               {"needs_action": {"type": "noul", "instructions": "Does this describe a real problem a person needs to act on?"},
                "severity": {"type": "score", "instructions": "How severe is it?", "criteria": ["low", "medium", "high", "critical"]}})
    print(json.dumps(a, indent=2))
