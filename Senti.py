import csv
import re
from typing import Dict

import nltk
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon", quiet=True)


def extract_video_id(youtube_link: str) -> str | None:
    pattern = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, youtube_link or "")
    return match.group(1) if match else None


def analyze_sentiment(csv_file: str) -> Dict[str, int]:
    sid = SentimentIntensityAnalyzer()

    comments: list[str] = []
    with open(csv_file, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            comments.append((row.get("Comment") or "").strip())

    num_neutral = 0
    num_positive = 0
    num_negative = 0

    for comment in comments:
        score = sid.polarity_scores(comment)
        compound = score.get("compound", 0.0)

        if compound == 0.0:
            num_neutral += 1
        elif compound > 0.0:
            num_positive += 1
        else:
            num_negative += 1

    return {
        "num_neutral": num_neutral,
        "num_positive": num_positive,
        "num_negative": num_negative,
    }


def bar_chart(csv_file: str) -> None:
    r = analyze_sentiment(csv_file)

    df = pd.DataFrame(
        {
            "Sentiment": ["Positive", "Negative", "Neutral"],
            "Number of Comments": [r["num_positive"], r["num_negative"], r["num_neutral"]],
        }
    )

    fig = px.bar(
        df,
        x="Sentiment",
        y="Number of Comments",
        color="Sentiment",
        title="Sentiment Analysis (Bar)",
        color_discrete_sequence=["#2ecc71", "#e74c3c", "#95a5a6"],
    )
    fig.update_layout(title_font=dict(size=18))
    st.plotly_chart(fig, use_container_width=True)


def plot_sentiment(csv_file: str) -> None:
    r = analyze_sentiment(csv_file)

    labels = ["Neutral", "Positive", "Negative"]
    values = [r["num_neutral"], r["num_positive"], r["num_negative"]]
    colors = ["#95a5a6", "#2ecc71", "#e74c3c"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textinfo="label+percent",
                marker=dict(colors=colors),
            )
        ]
    )
    fig.update_layout(title_text="Sentiment Analysis (Pie)")
    st.plotly_chart(fig, use_container_width=True)
