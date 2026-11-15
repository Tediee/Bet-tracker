import os
import requests

from dotenv import load_dotenv


ENV_PATH = os.path.join(
        os.path.dirname(__file__),
        ".env"
    )
print("Loading:", ENV_PATH)
load_dotenv(ENV_PATH)

WEBHOOK_URL = os.getenv(
    "DISCORD_WEBHOOK_URL"
)
print("WEBHOOK:", WEBHOOK_URL)

def send_discord_alert(message):

    response = requests.post(
        WEBHOOK_URL,
        json={
            "content": message
        }
    )

    print(
        f"Discord Status: {response.status_code}"
    )
    