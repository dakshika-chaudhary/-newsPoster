

import requests
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

def post_image_to_facebook(image_path, message):
    url = f"https://graph.facebook.com/{PAGE_ID}/photos"
    payload = {
        "message": message,
        "access_token": PAGE_ACCESS_TOKEN
    }

    files = {
        "source": open(image_path, "rb")
    }

    response = requests.post(url, data=payload, files=files)
    if response.status_code == 200:
        print("✅ Image posted successfully!")
        print("Post ID:", response.json()["post_id"])
    else:
        print("❌ Failed to post image")
        print(response.text)


if __name__ == "__main__":
    post_image_to_facebook("news_cards/news_1.jpg", "📰 Here's today's news update!")
