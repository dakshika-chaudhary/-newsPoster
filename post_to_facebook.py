
import requests
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")
IMAGE_PATHS = [
    "news_cards/news_1.jpg",
    "news_cards/news_2.jpg",
    "news_cards/news_3.jpg",
    "news_cards/news_4.jpg",
    "news_cards/news_5.jpg"
]

def upload_image_unpublished(image_path):
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"
    payload = {
        "published": "false",
        "access_token": PAGE_ACCESS_TOKEN
    }
    files = {
        "source": open(image_path, "rb")
    }

    response = requests.post(url, data=payload, files=files)
    response.raise_for_status()
    media_fbid = response.json()["id"]
    return media_fbid

def create_post_with_multiple_images(media_fbids, message):
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": PAGE_ACCESS_TOKEN
    }

    for i, fbid in enumerate(media_fbids):
        payload[f"attached_media[{i}]"] = f'{{"media_fbid":"{fbid}"}}'

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Multi-image post created successfully!")
        print("Post ID:", response.json()["id"])
    else:
        print("❌ Failed to create post")
        print(response.text)

if __name__ == "__main__":
    try:
        print("Uploading images as unpublished...")
        media_fbids = [upload_image_unpublished(path) for path in IMAGE_PATHS]
        print("Creating a post with uploaded images...")
        create_post_with_multiple_images(media_fbids, "📰 Today's News Updates!")
    except Exception as e:
        print("❌ Error:", e)
