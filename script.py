import requests
from datetime import datetime, timedelta
import os

GITHUB_USERNAME = "Tirvy"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def had_commit_today_or_yesterday():
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events"
    response = requests.get(url)
    events = response.json()

    for event in events:
        if event.get("type") == "PushEvent":
            try:
                event_date = datetime.strptime(
                    event["created_at"], "%Y-%m-%dT%H:%M:%SZ"
                ).date()
            except (KeyError, ValueError):
                continue
            if event_date == today or event_date == yesterday:
                return True

    return False


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    requests.post(url, data=payload)


if __name__ == "__main__":
    if not had_commit_today_or_yesterday():
        send_telegram_message("🚨 No commits today or yesterday. Go build something!")