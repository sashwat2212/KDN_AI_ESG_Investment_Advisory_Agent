import tweepy
import pandas as pd


BEARER_TOKEN = "8Ge5ZBX1NzHMNWaK5JEfPmXsn"


client = tweepy.Client(bearer_token=BEARER_TOKEN)


ESG_KEYWORDS = ["sustainability", "greenwashing", "carbon neutral", "ESG policies"]


def fetch_tweets(query, max_results=100):
    tweets = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["created_at", "text"])
    data = [{"created_at": tweet.created_at, "text": tweet.text} for tweet in tweets.data]
    return pd.DataFrame(data)


df = fetch_tweets("sustainability")
print(df.head())
df.to_csv("twitter_esg_data.csv", index=False)



import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


nltk.download("vader_lexicon") #sentiment analysis
sia = SentimentIntensityAnalyzer()


file_path = "/Users/kdn_aisashwat/Desktop/esg-investment-advisor /twitter_esg_data.csv"  
df = pd.read_csv(file_path)

def analyze_sentiment(text):
    sentiment_score = sia.polarity_scores(text)["compound"]
    sentiment_label = "Positive" if sentiment_score > 0.05 else "Negative" if sentiment_score < -0.05 else "Neutral"
    return sentiment_score, sentiment_label


df["sentiment_score"], df["sentiment_label"] = zip(*df["text"].map(analyze_sentiment))


output_file = "/Users/kdn_aisashwat/Desktop/esg-investment-advisor /twitter_esg_data_with_sentiment.csv"
df.to_csv(output_file, index=False)

print(f"Sentiment analysis completed! Data saved to {output_file}")

