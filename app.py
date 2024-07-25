import streamlit as st

st.set_page_config(page_title="YouTube Comment Sentiment", layout="centered")

st.title("YouTube Comment Sentiment Analyzer")

st.sidebar.header("Enter YouTube Link")
youtube_link = st.sidebar.text_input("Link", key="yt_link")
analyze_btn = st.sidebar.button("Analyze")

if analyze_btn:
    st.info("In the next commit, we will add video_id extraction.")
