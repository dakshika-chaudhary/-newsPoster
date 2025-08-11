from dotenv import load_dotenv
import tweepy
import os

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_TOKEN_SECRET")

client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_secret
)


# Post a tweet
tweet = "Hello Twitterr! #news"
response = client.create_tweet(text=tweet)

if response and response.data and 'id' in response.data:
    tweet_id = response.data['id']
    print(f"Tweet posted successfully! Tweet ID: {tweet_id}")
else:
    print("Failed to post tweet.")
print("Tweet posted successfully!")
