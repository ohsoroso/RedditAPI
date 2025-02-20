import praw
import pandas as pd

# Reddit API authentication (Make sure to replace with your actual credentials)
reddit = praw.Reddit(
    client_id="Veek5kFIB5UJBZi5PP1dhQ",
    client_secret="n6c9fkHSt2p-RbJj-g5rTnasu1Hyzw",
    user_agent="banXornah/0.1 by YourRedditUsername",
    check_for_async=False
)

# Keywords to search for
keywords = ["ban Twitter", "ban X", "no Twitter links", "block Twitter"]

# Store results
data = []

# Search Reddit for each keyword
for keyword in keywords:
    print(f"\nSearching for posts mentioning: '{keyword}'...")  # Removed emoji for compatibility

    # Make sure `reddit` is being called properly inside the loop
    for post in reddit.subreddit("all").search(keyword, limit=50):
        data.append({
            "Subreddit": post.subreddit.display_name,
            "Title": post.title,
            "Score": post.score,
            "Comments": post.num_comments,
            "Timestamp": post.created_utc
        })

    print(f"Collected {len(data)} posts so far.")  # Optional emoji check

# Convert to DataFrame and save
df = pd.DataFrame(data)
df.to_csv("reddit_twitter_ban_data.csv", index=False)

print("\nData saved to 'reddit_twitter_ban_data.csv'!")
