# 🚀 PostForge AI - Social Media Post Generator

**AI-Powered Post Creator for Instagram, Facebook & X (Twitter)**  
Powered by Grok (xAI) for maximum virality and platform optimization.

Created for content creators, marketers, and viral strategists like you.

## ✨ Features (MVP v1)

- **Platform-Optimized Generation**: Tailored prompts for Instagram (carousels, Reels captions), Facebook (community engagement), and X (hook-driven, concise).
- **Multiple Variations**: Generate 3-5 caption options per prompt with different hooks/styles.
- **Smart Inputs**: Niche presets (Hollywood edits, Beauty products, Gaming/PUBG, Football, Product Promo, Custom), tone, audience, language (English / Roman Urdu / Hinglish).
- **Full Output Package**:
  - Ready-to-post captions (copy-paste)
  - Platform-specific hashtag sets
  - Strong CTAs and engagement boosters
  - Detailed AI Image Generation Prompts (ready for Grok Imagine, Flux, Midjourney, etc.)
- **Niche Presets**: Quick-start buttons for your frequent content types (Hollywood Remix, Hair/Beauty Promo, Gaming, Football Transfers, Viral News).
- **Refine Mode**: Paste any existing caption and improve it for better hooks/engagement.
- **Educational**: Each variation includes "Why this works" insights to level up your skills.
- **Zero Lock-in**: Uses your own xAI API key (pay only for what you use — very cheap for text).

## 🛠 Tech Stack & Why

- **Streamlit**: Beautiful, fast Python web UI (no frontend coding needed).
- **xAI Grok API** (OpenAI-compatible): Best-in-class reasoning + creativity for viral content. Supports future image/video gen.
- Easy local run or deploy to Streamlit Cloud / Hugging Face / Render (free tiers available).

## 📋 Quick Start (Local)

### 1. Get xAI API Key (Free to start, pay-per-use)
1. Go to [https://console.x.ai/](https://console.x.ai/)
2. Sign up / Log in (use your X account preferably)
3. Create API Key → Copy it

### 2. Setup
```bash
cd social-ai-post-generator
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 4. First Use
- Paste your xAI API Key in the sidebar (or set `XAI_API_KEY` env var)
- Select platform + niche or custom topic
- Hit **Generate Viral Posts** 🚀
- Copy captions, hashtags, and image prompts

## 🔮 Roadmap / Future Versions

- v2: One-click Image Generation with Grok Imagine (text-to-image + image-to-video)
- v3: Carousel post series generator (5-10 slides with consistent story)
- v4: Auto-scheduling integration (Buffer/Meta Business API) or direct X posting
- v5: Analytics — predict engagement score, A/B test suggestions
- v6: Team workspace + content calendar
- Mobile-friendly PWA or native app idea

## 💡 Pro Tips for Best Results

- Be specific in "Topic/Key Message": "New God of War trailer reaction with epic Kratos edit" > "gaming post"
- Use **Refine Mode** on your old high-performing posts to 10x them.
- For product promos (beauty/hair): Always include "problem → solution → transformation + social proof hook"
- Test 2-3 variations and see what gets saves/shares on IG/X.
- Combine with X Radar (Premium+) for trending angles.

## 📁 Project Structure

```
social-ai-post-generator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .env.example           # Template for environment variables
└── prompts/               # (Future) Custom system prompts per platform/niche
```

## ⚠️ Notes

- **Costs**: Text generation is extremely cheap (~$0.001–0.01 per post batch). Image gen in future will cost more (you control usage).
- **Privacy**: Your API key stays local (never sent to me). Posts you generate are yours.
- **Rate Limits**: xAI has generous free tier to start; monitor usage in console.x.ai
- This is a production-ready starter you can customize, brand (add your logo), and even sell as SaaS later.

## 🤝 Need Help?

- Want me to add image generation now?
- Add specific niches or your brand voice (e.g., HollywoodMix9 style)?
- Convert to full FastAPI + React?
- Deploy it online for you?
- Integrate with your existing workflow / Google Sheets content calendar?

Just tell me — I'm here to iterate with you until it's perfect for your content creation business.

**Let's make your posts go viral on autopilot.** 🔥

---

*Built with ❤️ for creators by Grok — June 2026*