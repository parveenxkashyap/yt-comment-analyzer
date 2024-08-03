import os
import streamlit as st

from Senti import extract_video_id, analyze_sentiment, bar_chart, plot_sentiment
from YoutubeCommentScrapper import (
    get_youtube_client,
    save_video_comments_to_csv,
    get_channel_id,
    get_channel_info,
    get_video_stats,
)

st.set_page_config(page_title="YouTube Comment Sentiment", layout="centered")
st.title("YouTube Comment Sentiment Analyzer")


def delete_non_matching_csv_files(directory_path: str, video_id: str) -> None:
    for name in os.listdir(directory_path):
        if not name.endswith(".csv"):
            continue
        if name == f"{video_id}.csv":
            continue
        try:
            os.remove(os.path.join(directory_path, name))
        except OSError:
            pass


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

    delete_non_matching_csv_files(os.getcwd(), video_id)

    with open(csv_file, "rb") as f:
        st.download_button(
            label="Download Comments CSV",
            data=f.read(),
            file_name=os.path.basename(csv_file),
            mime="text/csv",
        )

    st.divider()
    st.subheader("Video Preview")
    st.video(youtube_link)

    # Channel info
    channel_id = get_channel_id(youtube, video_id)
    if channel_id:
        info = get_channel_info(youtube, channel_id)
        if info:
            st.divider()
            st.subheader("Channel Info")
            c1, c2 = st.columns([1, 2])
            with c1:
                if info["channel_logo_url"]:
                    st.image(info["channel_logo_url"], width=200)
            with c2:
                st.write(info["channel_title"])
                st.caption((info["channel_created_date"] or "")[:10])

            m1, m2, m3 = st.columns(3)
            m1.metric("Subscribers", info["subscriber_count"])
            m2.metric("Total Videos", info["video_count"])
            m3.metric("Channel Created", (info["channel_created_date"] or "")[:10])

            st.subheader("Description")
            st.write(info["channel_description"])

    # Video stats
    stats = get_video_stats(youtube, video_id)
    if stats:
        st.divider()
        st.subheader("Video Stats")
        v1, v2, v3 = st.columns(3)
        v1.metric("Views", stats.get("viewCount", ""))
        v2.metric("Likes", stats.get("likeCount", ""))
        v3.metric("Comments", stats.get("commentCount", ""))

    # Sentiment
    st.divider()
    st.subheader("Sentiment Results")
    results = analyze_sentiment(csv_file)

    s1, s2, s3 = st.columns(3)
    s1.metric("Positive", results["num_positive"])
    s2.metric("Negative", results["num_negative"])
    s3.metric("Neutral", results["num_neutral"])

    bar_chart(csv_file)
    plot_sentiment(csv_file)
