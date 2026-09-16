"""
generate_voice.py
يحوّل نص القصة لصوت بشري طبيعي باستخدام edge-tts (مجاني تمامًا، بدون API key).

يدعم أصوات مصرية أصلية: ar-EG-ShakirNeural (رجالي) / ar-EG-SalmaNeural (نسائي)
"""
import json
import asyncio
import sys
from pathlib import Path
import edge_tts  # pip install edge-tts

SCRIPT_DIR = Path(__file__).parent
EPISODE_PATH = SCRIPT_DIR.parent / "state" / "current_episode.json"
OUTPUT_AUDIO = SCRIPT_DIR.parent / "downloaded_clips" / "narration.mp3"

# غيّر ده لو عايز صوت مختلف بين الحلقات لتنويع أكبر
VOICE = "ar-EG-ShakirNeural"
RATE = "-4%"     # سرعة أبطأ شوية = إيقاع رعب أكتر
PITCH = "-2Hz"   # نبرة أعمق شوية


async def synthesize(text: str, output_path: Path):
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(str(output_path))


def main():
    if not EPISODE_PATH.exists():
        sys.exit("خطأ: مفيش current_episode.json — شغّل generate_script.py الأول")

    episode = json.loads(EPISODE_PATH.read_text(encoding="utf-8"))
    narration_text = episode["narration"]

    OUTPUT_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(synthesize(narration_text, OUTPUT_AUDIO))

    print(f"✅ اتولّد الصوت في: {OUTPUT_AUDIO}")


if __name__ == "__main__":
    main()
