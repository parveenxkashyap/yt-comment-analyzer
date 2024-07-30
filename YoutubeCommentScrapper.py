import csv
import os
from typing import Optional

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_youtube_client():
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing YOUTUBE_API_KEY in .env")

    return build("youtube", "v3", developerKey=api_key)


def get_channel_id(youtube, video_id: str) -> Optional[str]:
    try:
        resp = youtube.videos().list(part="snippet", id=video_id).execute()
        items = resp.get("items", [])
        if not items:
            return None
        return items[0]["snippet"]["channelId"]
    except HttpError:
        return None


def save_video_comments_to_csv(youtube, video_id: str, out_dir: str = ".") -> Optional[str]:
    comments: list[list[str]] = []

    try:
        req = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100,
        )
        resp = req.execute()

        while resp:
            for item in resp.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                username = snippet.get("authorDisplayName", "")
                comment = snippet.get("textDisplay", "")
                comments.append([username, comment])

            token = resp.get("nextPageToken")
            if not token:
                break

            resp = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=token,
            ).execute()

    except HttpError:
        return None

    if not comments:
        return None

    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, f"{video_id}.csv")

    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Username", "Comment"])
        writer.writerows(comments)

    return filepath
