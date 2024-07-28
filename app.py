import streamlit as st

from Senti import extract_video_id

st.set_page_config(page_title="YouTube Comment Sentiment", layout="centered")

st.title("YouTube Comment Sentiment Analyzer")

st.sidebar.header("Enter YouTube Link")
youtube_link = st.sidebar.text_input("Link", key="yt_link")
analyze_btn = st.sidebar.button("Analyze")

if analyze_btn:
    video_id = extract_video_id(youtube_link)

    if not video_id:
        st.error("Invalid YouTube link. Please paste a proper video link.")
    else:
        st.success(f"Video ID: {video_id}")
        st.info("In the next commit, we will add fetching comments from the YouTube API and saving them to a CSV file.")