import streamlit as st
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("reddit_twitter_ban_filtered.csv")

df = load_data()

# Sentiment Analysis Function
def get_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(str(text))

    if score["compound"] >= 0.1:
        return "Positive"
    elif score["compound"] <= -0.1:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment analysis if not already done
if "Sentiment" not in df.columns:
    df["Sentiment"] = df["Title"].apply(get_sentiment)

# --- Sidebar Navigation (Fixed Persistence) ---
st.sidebar.title("📌 Navigation")

# Use session_state to persist selected page
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"

if st.sidebar.button("🏠 Home"):
    st.session_state["selected_page"] = "Home"
if st.sidebar.button("📈 Subreddit Insights"):
    st.session_state["selected_page"] = "Subreddit Insights"
if st.sidebar.button("💬 Sentiment Analysis"):
    st.session_state["selected_page"] = "Sentiment Analysis"

page = st.session_state["selected_page"]

# --- Persistent Subreddit Selection ---
if "selected_subreddit" not in st.session_state:
    st.session_state["selected_subreddit"] = df["Subreddit"].unique()[0]

# --- HOME PAGE ---
if page == "Home":
    st.title("📊 Reddit Analysis Dashboard")

    # Mission Statement
    st.write("""
    Welcome! This project explores how Reddit communities discuss the banning of Twitter/X links. 
    We analyze posts, comments, and sentiment to see how different subreddits react.
    """)

    # Data Summary
    st.info(f"📝 Total posts collected: {len(df)} across {df['Subreddit'].nunique()} subreddits.")

    # Expanded Data Preview
    st.subheader("📄 Data Preview")
    st.dataframe(df)

    # General Sentiment Pie Chart
    st.subheader("📊 Overall Sentiment Across All Subreddits")
    sentiment_counts = df["Sentiment"].value_counts()
    
    fig = px.pie(
        names=sentiment_counts.index, 
        values=sentiment_counts.values,
        title="Overall Sentiment of Twitter/X Ban Discussions",
        hole=0.3
    )
    st.plotly_chart(fig)

# --- SUBREDDIT INSIGHTS (Persistent Selection) ---
elif page == "Subreddit Insights":
    st.title("📈 Subreddit Activity Analysis")

    # Top N Subreddits Selection (Up to 50)
    top_n = st.slider("Select Number of Top Subreddits:", 5, 50, 10)
    subreddit_counts = df["Subreddit"].value_counts().head(top_n)

    # Interactive Bar Chart
    fig = px.bar(
        subreddit_counts, 
        x=subreddit_counts.index, 
        y=subreddit_counts.values, 
        labels={'x': 'Subreddit', 'y': 'Number of Posts'},
        title=f"🔥 Top {top_n} Subreddits Discussing Twitter/X Bans",
        color=subreddit_counts.values, 
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig)

    # Persistent Subreddit Selection
    st.session_state["selected_subreddit"] = st.selectbox("Select a Subreddit:", df["Subreddit"].unique(), 
                                                          index=list(df["Subreddit"].unique()).index(st.session_state["selected_subreddit"]))

    # Display Posts Discussing X/Twitter Ban for the Selected Subreddit
    st.subheader(f"📝 Posts from r/{st.session_state['selected_subreddit']} Discussing Twitter/X Ban")
    subreddit_posts = df[df["Subreddit"] == st.session_state["selected_subreddit"]][["Title", "Score", "Sentiment"]]
    st.dataframe(subreddit_posts)

# --- SENTIMENT ANALYSIS (Fixed Persistence) ---
elif page == "Sentiment Analysis":
    st.title("💬 Subreddit-Specific Sentiment Analysis")

    # Persistent Subreddit Selection
    st.session_state["selected_subreddit"] = st.selectbox("Select a subreddit for sentiment breakdown:", df["Subreddit"].unique(), 
                                                          index=list(df["Subreddit"].unique()).index(st.session_state["selected_subreddit"]))

    # Filter posts for the selected subreddit
    subreddit_data = df[df["Subreddit"] == st.session_state["selected_subreddit"]]

    # Ensure at least 2 posts are needed instead of 10
    st.subheader(f"📊 Sentiment Breakdown for r/{st.session_state['selected_subreddit']}")
    subreddit_sentiment_counts = subreddit_data["Sentiment"].value_counts()

    fig = px.pie(
        names=subreddit_sentiment_counts.index, 
        values=subreddit_sentiment_counts.values,
        title=f"Sentiment of Posts in r/{st.session_state['selected_subreddit']}",
        hole=0.3
    )
    st.plotly_chart(fig)

    # Generate Word Cloud (Based on Post Titles)
    st.subheader(f"🗨️ Word Cloud for r/{st.session_state['selected_subreddit']}")
    all_titles = " ".join(subreddit_data["Title"].dropna())  # Drop NaN values to avoid errors
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_titles)

    # Display Word Cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)
