"""
open_review_issue.py
بيفتح GitHub Issue فيه كل تفاصيل الحلقة المسودة، وبيستنى منك تعليق "/approve"
قبل ما يكمل للنشر. ده بوابة المراجعة البشرية الحقيقية.

يحتاج: GITHUB_TOKEN (متوفر تلقائيًا جوه GitHub Actions، مش محتاج تضيفه بنفسك)
"""
import os
import json
import sys
import requests
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
EPISODE_PATH = SCRIPT_DIR.parent / "state" / "current_episode.json"

GITHUB_API = "https://api.github.com"


def main():
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")  # مثلا "username/horror-content-pipeline"
    run_id = os.environ.get("GITHUB_RUN_ID", "")

    if not token or not repo:
        sys.exit("خطأ: لازم تشتغل جوه GitHub Actions (GITHUB_TOKEN و GITHUB_REPOSITORY)")

    episode = json.loads(EPISODE_PATH.read_text(encoding="utf-8"))

    artifact_note = (
        f"🎬 الفيديو المُجمَّع موجود كـ **Artifact** في نفس الـ workflow run:\n"
        f"https://github.com/{repo}/actions/runs/{run_id}\n\n"
        f"نزّله وشوفه الأول قبل ما توافق."
    )

    body = f"""## 📝 مسودة حلقة جديدة — جاهزة للمراجعة

**العنوان:** {episode['title']}

**السيناريو:**
{episode['narration']}

**الكابشن المقترح:**
{episode['caption']}

**كلمات البحث البصرية المستخدمة:** {', '.join(episode['visual_keywords'])}

---
{artifact_note}

---
### ✅ للموافقة والنشر
اكتب تعليق فيه بالظبط: `/approve`

### ✏️ لو عايز تعدّل حاجة
عدّل النص هنا في وصف الـ Issue نفسه قبل ما توافق (السكريبت هياخد النسخة المعدّلة).

### ❌ لرفض الحلقة دي
اكتب تعليق فيه: `/reject` — والنظام هيولّد حلقة تانية بدلها.
"""

    resp = requests.post(
        f"{GITHUB_API}/repos/{repo}/issues",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        json={
            "title": f"مراجعة: {episode['title']}",
            "body": body,
            "labels": ["horror-draft", "needs-review"],
        },
        timeout=20,
    )
    resp.raise_for_status()
    issue_url = resp.json()["html_url"]
    print(f"✅ اتفتح Issue للمراجعة: {issue_url}")


if __name__ == "__main__":
    main()
