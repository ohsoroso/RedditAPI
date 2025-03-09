import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load the dataset
df = pd.read_csv("reddit_twitter_ban_data.csv")

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to classify sentiment based on VADER score
def get_sentiment(text):
    score = analyzer.polarity_scores(str(text))  # Convert NaN values to string
    if score["compound"] >= 0.05:
        return "Positive"
    elif score["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment analysis to post titles
df["Sentiment"] = df["Title"].apply(get_sentiment)

# Count occurrences of each sentiment
sentiment_counts = df["Sentiment"].value_counts()

# Define custom function for pie chart labels (show percentage + actual count)
def pie_label(pct, all_vals):
    absolute = int(pct / 100. * sum(all_vals))  # Convert percentage to count
    return f"{pct:.1f}% ({absolute})"

# Plot sentiment distribution with improved labels
plt.figure(figsize=(7, 7))
plt.pie(
    sentiment_counts, 
    labels=sentiment_counts.index, 
    autopct=lambda pct: pie_label(pct, sentiment_counts),  # Show % and count
    colors=["green", "gray", "red"], 
    startangle=140
)
plt.title("Sentiment of Twitter/X Ban Discussions")
plt.show()
