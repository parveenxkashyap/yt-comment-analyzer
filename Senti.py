import csv
import re
from typing import Dict

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download once (quiet) so first run doesn't break
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