# YouTube Comment Sentiment Analyzer

This project takes a YouTube video link, scrapes the comments, saves them into a CSV file, and performs sentiment analysis using VADER (Positive/Negative/Neutral) along with interactive charts.

## Features
- Fetches comments from a YouTube video and generates a `<videoId>.csv` file (columns: `Username`, `Comment`).
- Provides a CSV download button in the Streamlit UI.
- Displays channel information (name, logo, total videos, creation date, subscribers, description).
- Shows video statistics (views, likes, comment count).
- Calculates sentiment counts using NLTK VADER (positive/negative/neutral) and renders Plotly charts (bar chart + pie chart).

## Tech Stack
- Python + Streamlit (UI).
- YouTube Data API (googleapiclient) for comments, channel, and video data.
- NLTK VADER + Pandas + Plotly for sentiment analysis and visualization.

## Setup
1. Install dependencies:
   ```bash
   pip install streamlit google-api-python-client python-dotenv nltk pandas plotly colorama

2. Create a .env file in the project root:
    ```bash
    YOUTUBEAPIKEY=YOUR_YOUTUBE_DATA_API_KEY

    Note: On the first run, NLTK will download the vader_lexicon.

3. Run
    ```bash
    streamlit run app.py


Files

1. app.py → Streamlit app (UI and main flow).
2. YoutubeCommentScrapper.py → Fetches comments, channel, and video data using the YouTube API and writes CSV files.
3. Senti.py → Extracts video ID, performs sentiment analysis, and generates Plotly charts.
