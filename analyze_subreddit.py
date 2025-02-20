import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("reddit_twitter_ban_data.csv")

# Count posts by subreddit
subreddit_counts = df["Subreddit"].value_counts().head(10)

# Plot subreddit post count
plt.figure(figsize=(10, 5))
subreddit_counts.plot(kind="bar", color="blue")
plt.title("Top 10 Subreddits Discussing Twitter/X Bans")
plt.xlabel("Subreddit")
plt.ylabel("Number of Posts")
plt.xticks(rotation=45)
plt.show()
