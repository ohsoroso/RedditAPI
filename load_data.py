import pandas as pd

# Load the dataset
df = pd.read_csv("reddit_twitter_ban_data.csv")

# Preview data
print(df.head())

# Save cleaned version (if needed)
df.to_csv("cleaned_reddit_data.csv", index=False)
