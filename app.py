import os
import streamlit as st

from Senti import extract_video_id
from YoutubeCommentScrapper import (
    get_youtube_client,
    save_video_comments_to_csv,
    get_channel_id,
    get_channel_info,
    get_video_stats,
)

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

    channel_id = get_channel_id(youtube, video_id)
    if channel_id:
        info = get_channel_info(youtube, channel_id)
        if info:
            col1, col2 = st.columns(2)
            with col1:
                if info["channel_logo_url"]:
                    st.image(info["channel_logo_url"], width=220)
            with col2:
                st.subheader("YouTube Channel")
                st.write(info["channel_title"])

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Subscribers", info["subscriber_count"])
            with c2:
                st.metric("Total Videos", info["video_count"])
            with c3:
                st.metric("Created", (info["channel_created_date"] or "")[:10])

            st.subheader("Channel Description")
            st.write(info["channel_description"])

    stats = get_video_stats(youtube, video_id)
    if stats:
        st.subheader("Video Stats")
        v1, v2, v3 = st.columns(3)
        with v1:
            st.metric("Views", stats.get("viewCount", ""))
        with v2:
            st.metric("Likes", stats.get("likeCount", ""))
        with v3:
            st.metric("Comments", stats.get("commentCount", ""))

    st.info("In the next commit, we will add sentiment charts and UI polish.")
