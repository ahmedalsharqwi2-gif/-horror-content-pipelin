# قناة الرعب — Pipeline مجاني بالكامل

مبني على: Groq (سيناريو) + Pexels (كليبات حقيقية) + edge-tts (صوت بشري) +
ffmpeg (مونتاج) + GitHub Actions (تنسيق) + مراجعة بشرية إلزامية + Buffer (نشر)

## خطوات التجهيز (مرة واحدة بس)

### 1. اعمل ريبو جديد على GitHub وارفعله المشروع ده
```bash
git init
git add .
git commit -m "initial setup"
git remote add origin https://github.com/USERNAME/horror-content-pipeline.git
git push -u origin main
```

### 2. جيب الـ API Keys المجانية (كلها مجانية 100%)
| المفتاح | من فين | مجاني؟ |
|---|---|---|
| `GROQ_API_KEY` | https://console.groq.com/keys | ✅ مجاني بالكامل |
| `PEXELS_API_KEY` | https://www.pexels.com/api/ | ✅ مجاني بالكامل |
| `BUFFER_ACCESS_TOKEN` | https://buffer.com → Settings → Apps | ✅ مجاني (Free plan) |
| `BUFFER_CHANNEL_ID` | من نفس صفحة Buffer، بعد ربط قناة اليوتيوب | ✅ |

### 3. ضيف المفاتيح في GitHub Secrets
Settings → Secrets and variables → Actions → New repository secret
ضيف كل مفتاح من الجدول فوق (ملحوظة: GITHUB_TOKEN بييجي تلقائي، مش محتاج تضيفه).

### 4. حل نقطة استضافة الفيديو قبل Buffer (مهم)
Buffer محتاج رابط عام للفيديو مش ملف مرفوع مباشر. أسهل حل مجاني:
- استخدم **GitHub Releases** كـ "استضافة": ارفع الفيديو كـ asset في release وخد الرابط المباشر
- أو استخدم **Cloudflare R2** (مجاني لحد 10GB شهريًا)

لسه محتاج تكمّل دالة `upload_media()` في `scripts/publish_buffer.py` بأي
الطريقتين دول — سيبتها placeholder عشان تختار الأنسب ليك.

### 5. جرّبه يدويًا الأول
Actions tab → Create Horror Episode Draft → Run workflow

## إزاي الدورة بتشتغل يوميًا

```
كل يوم 10 مساءً (cron)
   │
   ▼
generate_script.py  → يكتب قصة رعب جديدة + كلمات بحث بصرية
   │
   ▼
fetch_clips.py       → يجيب كليبات حقيقية من Pexels (بدون تكرار)
   │
   ▼
generate_voice.py    → يحوّل القصة لصوت بشري طبيعي (عربي مصري)
   │
   ▼
assemble_video.py    → يجمع كل حاجة في فيديو 9:16 نهائي
   │
   ▼
open_review_issue.py → يفتح GitHub Issue وينتظرك
   │
   ▼
  [إنت تراجع وتكتب /approve]
   │
   ▼
publish_buffer.py    → ينشر تلقائيًا عبر Buffer
```

## التعديل على قناتين تانيين

لما تتأكد إن قناة الرعب شغالة كويس، كرر نفس الهيكل لقناة القطط والتذكير
الإسلامي، بس غيّر:
- `prompts/*.md` (نص الـ system prompt)
- كلمات البحث الافتراضية في Pexels
- الصوت المستخدم في `generate_voice.py`

كل قناة تبقى في ريبو منفصل (أو مجلد منفصل في نفس الريبو مع workflows منفصلة).
