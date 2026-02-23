import requests
from datetime import datetime, timedelta
import os

GITHUB_USERNAME = "Tirvy"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def had_commit_yesterday():
    yesterday = (datetime.utcnow() - timedelta(days=1)).date()
    
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events"
    response = requests.get(url)
    events = response.json()

    for event in events:
        if event["type"] == "PushEvent":
            event_date = datetime.strptime(
                event["created_at"], "%Y-%m-%dT%H:%M:%SZ"
            ).date()
            if event_date == yesterday:
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
    if not had_commit_yesterday():
        send_telegram_message("🚨 No commits yesterday. Go build something!")