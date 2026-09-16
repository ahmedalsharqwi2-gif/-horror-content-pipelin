"""
publish_buffer.py
بينشر الفيديو النهائي عبر Buffer API بعد ما توافق على الحلقة بـ /approve.

يحتاج: BUFFER_ACCESS_TOKEN و BUFFER_CHANNEL_ID (من إعدادات Buffer)
"""
import os
import json
import sys
import requests
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
EPISODE_PATH = SCRIPT_DIR.parent / "state" / "current_episode.json"
FINAL_VIDEO = SCRIPT_DIR.parent / "output" / "final_video.mp4"

BUFFER_API = "https://api.bufferapp.com/1"


def upload_media(video_path: Path, access_token: str) -> str:
    """Buffer محتاج رابط عام للفيديو مش رفع مباشر أحيانًا —
    البديل العملي: ارفع الفيديو على مكان مؤقت عام (مثلا GitHub Release
    أو أي storage عندك رابط مباشر ليه) وحط الرابط هنا.
    الدالة دي placeholder لحد ما تحدد طريقة الاستضافة المؤقتة بتاعتك."""
    raise NotImplementedError(
        "لازم تحدد إزاي هترفع الفيديو لرابط عام قبل إرساله لـ Buffer "
        "(اقتراح: GitHub Release asset أو Cloudflare R2 المجاني)"
    )


def create_buffer_post(video_url: str, caption: str, channel_id: str, access_token: str):
    resp = requests.post(
        f"{BUFFER_API}/updates/create.json",
        data={
            "access_token": access_token,
            "profile_ids[]": channel_id,
            "text": caption,
            "media[video]": video_url,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    access_token = os.environ.get("BUFFER_ACCESS_TOKEN")
    channel_id = os.environ.get("BUFFER_CHANNEL_ID")

    if not access_token or not channel_id:
        sys.exit("خطأ: لازم BUFFER_ACCESS_TOKEN و BUFFER_CHANNEL_ID في GitHub Secrets")

    if not FINAL_VIDEO.exists():
        sys.exit("خطأ: مفيش final_video.mp4 — شغّل assemble_video.py الأول")

    episode = json.loads(EPISODE_PATH.read_text(encoding="utf-8"))

    video_url = upload_media(FINAL_VIDEO, access_token)
    result = create_buffer_post(video_url, episode["caption"], channel_id, access_token)

    print(f"✅ اتنشر البوست عبر Buffer: {result}")


if __name__ == "__main__":
    main()
