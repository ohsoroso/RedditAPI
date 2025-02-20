import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load the dataset
df = pd.read_csv("reddit_twitter_ban_data.csv")

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(str(text))
    if score["compound"] >= 0.05:
        return "Positive"
    elif score["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment analysis
df["Sentiment"] = df["Title"].apply(get_sentiment)

# Plot sentiment distribution
df["Sentiment"].value_counts().plot(kind="pie", autopct="%1.1f%%", colors=["green", "gray", "red"])
plt.title("Sentiment of Twitter/X Ban Discussions")
plt.show()
