import os
import streamlit as st

from Senti import extract_video_id
from YoutubeCommentScrapper import get_youtube_client, save_video_comments_to_csv

st.set_page_config(page_title="YouTube Comment Sentiment", layout="centered")
st.title("YouTube Comment Sentiment Analyzer")

st.sidebar.header("Enter YouTube Link")
youtube_link = st.sidebar.text_input("Link", key="yt_link")
analyze_btn = st.sidebar.button("Analyze")

@st.cache_resource
def _yt():
    return get_youtube_client()

if analyze_btn:
    video_id = extract_video_id(youtube_link)

    if not video_id:
        st.error("Invalid YouTube link. Please paste a proper video link.")
        st.stop()

    st.success(f"Video ID: {video_id}")

    try:
        youtube = _yt()
    except Exception as e:
        st.error(f"YouTube API client init failed: {e}")
        st.stop()

    csv_file = save_video_comments_to_csv(youtube, video_id, out_dir=os.getcwd())
    if not csv_file:
        st.error("Failed to fetch comments (API/permissions/disabled comments).")
        st.stop()

    st.success("Comments saved to CSV!")

    with open(csv_file, "rb") as f:
        st.download_button(
            label="Download Comments CSV",
            data=f.read(),
            file_name=os.path.basename(csv_file),
            mime="text/csv",
        )

    st.info("In the next commit, we will show channel and video stats.")
