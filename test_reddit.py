import praw
import pandas as pd
from datetime import datetime
import sys

# Fix Unicode encoding issues on Windows
sys.stdout.reconfigure(encoding="utf-8")

# Reddit API authentication (Make sure to replace with your actual credentials)
reddit = praw.Reddit(
    client_id="Veek5kFIB5UJBZi5PP1dhQ",
    client_secret="n6c9fkHSt2p-RbJj-g5rTnasu1Hyzw",
    user_agent="banXornah/0.1 by YourRedditUsername",
    check_for_async=False
)

# Expanded keyword list for searching
keywords = [
    "ban Twitter", "ban X", "no Twitter links", "block Twitter",
    "remove Twitter links", "Twitter not allowed", "Twitter/X ban",
    "Twitter banned", "Twitter links removed", "X links not allowed",
    "no Twitter allowed", "no X allowed", "banning Twitter links"
]

# Date range for filtering (from January 19, 2025, to March 8, 2025)
start_date = datetime(2025, 1, 19).timestamp()  # Convert to Unix timestamp
end_date = datetime(2025, 3, 8).timestamp()  # Convert to Unix timestamp

# Store results
data = []

# Search Reddit for each keyword with an increased limit
for keyword in keywords:
    print(f"\n🔍 Searching for posts mentioning: '{keyword}'...")

    # Increase post limit per search to capture more data
    for post in reddit.subreddit("all").search(keyword, limit=150):
        post_timestamp = post.created_utc  # Get post timestamp

        # Only keep posts within the defined date range
        if start_date <= post_timestamp <= end_date:
            data.append({
                "Subreddit": post.subreddit.display_name,
                "Title": post.title,
                "Score": post.score,
                "Comments": post.num_comments,
                "Timestamp": post_timestamp
            })

    print(f"✅ Collected {len(data)} posts so far.")

# Convert to DataFrame and save filtered dataset
df = pd.DataFrame(data)
df.to_csv("reddit_twitter_ban_filtered.csv", index=False)

print("\n📁 Data saved to 'reddit_twitter_ban_filtered.csv'!")
