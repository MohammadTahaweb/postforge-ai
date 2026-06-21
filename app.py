#!/usr/bin/env python3
"""
PostForge AI - Professional Social Media Post Generator
Powered by Grok (xAI API)
Built for creators who want platform-optimized, viral-ready content fast.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="PostForge AI | Viral Posts for IG • FB • X",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://x.com/MohammedTa92",
        "Report a bug": "https://x.com/MohammedTa92",
        "About": "PostForge AI — Built with Grok to 10x your content output"
    }
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    .platform-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 0.5rem;
    }
    .ig-badge { background: #E1306C; color: white; }
    .fb-badge { background: #1877F2; color: white; }
    .x-badge { background: #000000; color: white; }
    
    .variation-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border-left: 5px solid #FF4B2B;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0.8rem 0 0.4rem 0;
    }
    .copy-hint {
        font-size: 0.75rem;
        color: #888;
        font-style: italic;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    .stTextArea textarea {
        font-family: 'Inter', system-ui, sans-serif;
    }
    .metric-small {
        font-size: 0.85rem;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if "history" not in st.session_state:
    st.session_state.history = []
if "last_generation" not in st.session_state:
    st.session_state.last_generation = None
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("XAI_API_KEY", "")

# ==================== HELPER FUNCTIONS ====================

def get_xai_client(api_key: str) -> OpenAI:
    """Create OpenAI-compatible client for xAI API"""
    return OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

def get_platform_badge(platform: str) -> str:
    badges = {
        "Instagram": '<span class="platform-badge ig-badge">📷 INSTAGRAM</span>',
        "Facebook": '<span class="platform-badge fb-badge">📘 FACEBOOK</span>',
        "X (Twitter)": '<span class="platform-badge x-badge">𝕏 X / TWITTER</span>'
    }
    return badges.get(platform, platform)

def get_niche_presets() -> Dict[str, str]:
    return {
        "🎬 Hollywood Remix / Epic Edit": 
            "Create a high-engagement post about a Hollywood movie clip, fan edit, 'what if these two characters met in real life', or epic remix. Focus on cinematic moments, star power, and emotional hooks.",
        "💇 Beauty & Hair Product Promo": 
            "Write a promotional caption for a hair tool (straightener, laser hair remover, brush, etc.). Use problem → solution → transformation structure. Include social proof, before/after feel, and strong but natural CTA with affiliate link placeholder.",
        "🎮 Gaming (PUBG, God of War, etc.)": 
            "High-energy gaming post: new limited-time mode (e.g. PUBG x PAYDAY), character reveal (Kratos, Atreus), funny fail/win moment, or challenge. Use gamer slang, urgency, and calls to action like 'comment your main' or 'tag your squad'.",
        "⚽ Football / Transfer News": 
            "React to or rephrase a football transfer rumor, big bid (e.g. €150m Olise to Real Madrid), club statement, or fan reaction. Make it sound insider or passionate fan perspective with viral potential.",
        "🔥 Viral Hook / Trend Jacking": 
            "Take any trending global or Pakistan news/topic and turn it into a scroll-stopping hook post that relates to your audience. Strong opinion + question format works best.",
        "✍️ Custom / Your Own Idea": 
            "Write about whatever topic the user describes in detail. Make it platform-native and highly engaging."
    }

def get_tone_options() -> List[str]:
    return [
        "Viral & Punchy (strong hooks, scroll-stopping)",
        "Engaging Storyteller (emotional, narrative)",
        "Professional & Authority (expert, credible)",
        "Casual & Relatable (friendly, conversational)",
        "Promotional & Salesy (benefit-driven, offer-focused)",
        "Controversial / Hot Take (sparks comments & shares)"
    ]

def get_language_options() -> List[str]:
    return [
        "English (Global / Professional)",
        "Roman Urdu (Pakistani audience friendly)",
        "Hinglish / Roman Urdu Mix (most natural for desi creators)",
        "Bilingual (English + Roman Urdu version)"
    ]

def build_system_prompt(platform: str, niche: str, tone: str, language: str, num_variations: int) -> str:
    """Craft a powerful, platform-specific system prompt"""
    
    platform_rules = {
        "Instagram": """
- Instagram loves longer, story-driven captions with line breaks, emojis, and personality.
- Structure: Hook (first 1-2 lines must stop the scroll) → Story / Value → CTA (like, comment, save, share, follow).
- Use 8-15 relevant hashtags (mix popular + niche). Best placed at the end or in first comment.
- Emojis: Generous but not spammy. Use them to break text and highlight key points.
- Carousel / Multi-slide posts: Suggest how to break content into 5-10 slides if relevant.
- Goal: Maximize Saves + Shares (algorithm loves these more than likes).
""",
        "Facebook": """
- Facebook favors community feel, questions that spark real discussion, and longer thoughtful posts.
- Strong emotional hooks + relatability work great.
- Encourage comments heavily ("Tag someone who needs to see this", "What's your experience?").
- Hashtags: 3-6 max, or none if very personal/community post.
- Emojis: Moderate. Facebook audience responds well to warmth and authenticity.
- Goal: High comment velocity in first 30-60 mins.
""",
        "X (Twitter)": """
- X is brutal: You have ~1.5 seconds. First line = HOOK. Make it bold, surprising, or curiosity-driven.
- Keep total under 280 characters when possible (or thread if complex).
- Short paragraphs (1-2 lines max). Use line breaks.
- Emojis: 1-4 max, used strategically for visual pop.
- Hashtags: 2-5 max. Only use if they add discoverability (e.g. #GodOfWar, #PUBGMobile).
- Questions, polls, and controversial but respectful takes drive replies.
- Goal: Replies + Reposts + Bookmarks.
"""
    }

    language_rules = {
        "English (Global / Professional)": "Write all captions in clear, natural, high-quality English suitable for international audiences.",
        "Roman Urdu (Pakistani audience friendly)": "Write captions primarily in Roman Urdu using natural Pakistani informal style. Use English words where they feel natural (common in desi social media). Make it feel local and relatable.",
        "Hinglish / Roman Urdu Mix (most natural for desi creators)": "Use a natural mix of Roman Urdu + English (Hinglish). This is the most common and engaging style for Pakistani/Indian creators on Instagram, Facebook and X.",
        "Bilingual (English + Roman Urdu version)": "Provide TWO versions for each variation: (1) English version, (2) Roman Urdu / Hinglish version right below it. Label them clearly."
    }

    prompt = f"""You are PostForge AI — a world-class viral social media strategist and copywriter who has generated billions of impressions.

You specialize in creating platform-native, algorithm-optimized posts that stop the scroll and drive massive engagement (likes, comments, saves, shares, reposts).

CURRENT TASK:
- Platform: {platform}
- Niche / Content Type: {niche}
- Desired Tone: {tone}
- Language Style: {language}
- Generate exactly {num_variations} distinct variations.

{platform_rules.get(platform, "")}

{language_rules.get(language, "")}

GENERAL RULES FOR ALL PLATFORMS:
1. Every caption must have a **powerful hook in the first 1-2 lines**. No boring starts.
2. Use storytelling, emotion, curiosity, controversy, or relatable pain points.
3. Include a clear, natural Call-to-Action (CTA) that matches the goal (comment, save, share, click link, tag friend).
4. Optimize for the specific platform's algorithm (mentioned above).
5. Make it feel human and authentic — never robotic or overly salesy unless the tone demands it.
6. For product promos: Problem → Agitation → Solution → Transformation + Proof.
7. For entertainment/gaming/Hollywood: High energy, FOMO, "you need to see this", insider feel.

OUTPUT FORMAT (strictly follow this structure for each variation):

**Variation 1: [Catchy short name for this version, e.g. "Bold Hook" or "Emotional Story"]**

**Caption:**
[Full ready-to-post caption here with line breaks and emojis]

**Why this works:**
[1-2 sentences explaining the psychological hook, algorithm fit, or why it will perform well]

**Hashtags:**
[#tag1 #tag2 #tag3 ...]  (platform-appropriate number)

**Image / Visual Prompt:**
[Detailed, cinematic prompt ready to paste into Grok Imagine, Flux, Midjourney or Leonardo. Include style, mood, composition, lighting, aspect ratio suggestion if relevant. Make it visually stunning and on-brand.]

---
(Repeat the exact same structure for Variation 2, 3, etc.)

After all variations, add one final section:

**💡 Pro Tips for Maximum Reach on {platform}:**
- 3-4 bullet points with specific, actionable advice (posting time, first comment strategy, A/B test ideas, etc.)

Do not add any extra intro or closing text outside this structure. Be creative, bold, and data-driven in your suggestions."""

    return prompt

def generate_posts(
    client: OpenAI,
    platform: str,
    niche: str,
    topic: str,
    tone: str,
    language: str,
    num_variations: int,
    model: str = "grok-4.3"
) -> str:
    """Call xAI API and return the raw response text"""
    
    system_prompt = build_system_prompt(platform, niche, tone, language, num_variations)
    
    user_prompt = f"""Topic / Key Message / Idea:
{topic}

Please generate {num_variations} high-quality variations now following the exact output format."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.82,   # Creative but consistent
            max_tokens=2800,
            top_p=0.95
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

def parse_and_display_variations(raw_output: str, platform: str):
    """Display the LLM output beautifully with copy-friendly sections"""
    if raw_output.startswith("ERROR:"):
        st.error(raw_output)
        return
    
    st.markdown("---")
    st.subheader(f"✨ Generated Variations for {platform}")
    
    # Split by Variation
    parts = raw_output.split("**Variation ")
    
    for i, part in enumerate(parts[1:], 1):  # Skip first empty
        if not part.strip():
            continue
            
        # Extract title
        title_end = part.find("**")
        var_title = part[:title_end].strip() if title_end > 0 else f"Variation {i}"
        
        with st.container():
            st.markdown(f'<div class="variation-card">', unsafe_allow_html=True)
            st.markdown(f"### Variation {i}: {var_title}")
            
            # Try to extract sections (simple parsing)
            lines = part.split("\n")
            current_section = None
            section_content = []
            
            for line in lines:
                line = line.strip()
                if line.startswith("**Caption:**"):
                    current_section = "caption"
                    section_content = []
                elif line.startswith("**Why this works:**"):
                    if section_content and current_section == "caption":
                        st.markdown("**📝 Caption**")
                        caption_text = "\n".join(section_content).strip()
                        st.text_area(
                            label="Caption (select & copy)",
                            value=caption_text,
                            height=180,
                            key=f"cap_{i}_{hash(caption_text[:50])}",
                            label_visibility="collapsed"
                        )
                    current_section = "why"
                    section_content = []
                elif line.startswith("**Hashtags:**"):
                    if section_content and current_section == "why":
                        st.markdown("**💡 Why it works**")
                        st.info("\n".join(section_content).strip())
                    current_section = "hashtags"
                    section_content = []
                elif line.startswith("**Image / Visual Prompt:**"):
                    if section_content and current_section == "hashtags":
                        st.markdown("**🏷️ Hashtags**")
                        hashtags = "\n".join(section_content).strip()
                        st.code(hashtags, language="text")
                    current_section = "image"
                    section_content = []
                elif line.startswith("---") or line.startswith("**💡 Pro Tips"):
                    if section_content and current_section == "image":
                        st.markdown("**🖼️ Image Prompt (copy to Grok Imagine / Flux)**")
                        st.code("\n".join(section_content).strip(), language="text")
                    current_section = None
                    section_content = []
                elif current_section:
                    section_content.append(line)
            
            # Handle last section if any
            if section_content and current_section == "image":
                st.markdown("**🖼️ Image Prompt (copy to Grok Imagine / Flux)**")
                st.code("\n".join(section_content).strip(), language="text")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Pro Tips at the end
    if "**💡 Pro Tips" in raw_output:
        tips_start = raw_output.find("**💡 Pro Tips")
        tips_text = raw_output[tips_start:].replace("**💡 Pro Tips for Maximum Reach on", "**💡 Pro Tips**").strip()
        st.markdown("---")
        st.markdown(tips_text)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://picsum.photos/id/1015/300/80", width=300)  # Placeholder banner
    st.markdown("## ⚙️ Settings")
    
    api_key = st.text_input(
        "xAI API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="xai-...",
        help="Get your free API key at console.x.ai"
    )
    st.session_state.api_key = api_key
    
    if not api_key:
        st.warning("⚠️ Please enter your xAI API Key to generate posts.")
        st.markdown("[→ Get API Key](https://console.x.ai/)", unsafe_allow_html=True)
    
    model = st.selectbox(
        "Model",
        ["grok-4.3", "grok-3"],
        index=0,
        help="grok-4.3 is the most capable for creative writing"
    )
    
    st.divider()
    
    st.markdown("### 📜 Generation History")
    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"{item['platform'][:3]} • {item['topic'][:40]}..."):
                st.caption(f"{item['timestamp']}")
                if st.button("Load this generation", key=f"load_{idx}"):
                    st.session_state.last_generation = item['output']
                    st.rerun()
    else:
        st.caption("Your generated posts will appear here after first use.")
    
    st.divider()
    st.markdown("**Made for creators • Powered by Grok**")
    st.caption("Mohammed Taha Khan • June 2026")

# ==================== MAIN UI ====================
st.markdown('<h1 class="main-header">🚀 PostForge AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Generate scroll-stopping posts for Instagram • Facebook • X in seconds</p>', unsafe_allow_html=True)

# Quick stats / trust
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Platforms", "3", "IG • FB • X optimized")
with col2:
    st.metric("Avg. Time", "< 15s", "per 5 variations")
with col3:
    st.metric("Cost per batch", "~$0.002-0.01", "using Grok")

st.divider()

# ==================== TABS ====================
tab1, tab2 = st.tabs(["🆕 Generate New Post", "✍️ Refine Existing Caption"])

with tab1:
    # Platform Selection
    st.markdown("### 1. Choose Platform")
    platform = st.radio(
        "Target Platform",
        options=["Instagram", "Facebook", "X (Twitter)"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown(get_platform_badge(platform), unsafe_allow_html=True)
    
    # Niche / Preset
    st.markdown("### 2. Content Type / Niche")
    niche_presets = get_niche_presets()
    niche_choice = st.selectbox(
        "Quick Presets (or choose Custom)",
        options=list(niche_presets.keys()),
        index=5  # Custom by default
    )
    
    if niche_choice == "✍️ Custom / Your Own Idea":
        niche_desc = ""
        topic = st.text_area(
            "Describe your topic, key message, or idea in detail",
            placeholder="e.g. New PUBG x PAYDAY mode just dropped — 50k+ followers needed for creator campaign. Make a hype post encouraging people to play and tag squad.",
            height=100,
            key="custom_topic"
        )
    else:
        niche_desc = niche_presets[niche_choice]
        st.info(f"**Preset loaded:** {niche_desc[:120]}...")
        topic = st.text_area(
            "Add specific details or angle (optional but recommended)",
            placeholder="e.g. Focus on the new limited-time mode rewards or the collab with PAYDAY. Make it feel urgent and fun.",
            height=80,
            key="preset_topic"
        )
    
    # Tone & Language
    col_tone, col_lang = st.columns(2)
    with col_tone:
        tone = st.selectbox("Tone / Voice", get_tone_options(), index=0)
    with col_lang:
        language = st.selectbox("Language Style", get_language_options(), index=2)  # Hinglish default for user
    
    # Advanced Options
    with st.expander("⚙️ Advanced Options"):
        num_variations = st.slider("Number of variations", 2, 5, 3)
        st.caption("More variations = slightly higher cost & time")
        
        include_image_gen = st.checkbox("Include image generation prompts (always on in v1)", value=True, disabled=True)
        st.caption("Future: One-click generate actual images with Grok Imagine")
    
    # Generate Button
    generate_btn = st.button(
        "🚀 Generate Viral Posts",
        type="primary",
        use_container_width=True,
        disabled=not (api_key and topic.strip())
    )
    
    if generate_btn:
        if not api_key:
            st.error("Please enter your xAI API Key in the sidebar first.")
        elif not topic.strip():
            st.error("Please describe your topic or idea.")
        else:
            with st.spinner("🧠 Grok is crafting scroll-stopping posts for you..."):
                client = get_xai_client(api_key)
                raw_output = generate_posts(
                    client=client,
                    platform=platform,
                    niche=niche_desc or niche_choice,
                    topic=topic,
                    tone=tone,
                    language=language,
                    num_variations=num_variations,
                    model=model
                )
            
            # Save to history
            history_item = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "platform": platform,
                "topic": topic[:80],
                "output": raw_output
            }
            st.session_state.history.append(history_item)
            st.session_state.last_generation = raw_output
            
            # Display
            parse_and_display_variations(raw_output, platform)

with tab2:
    st.markdown("### Refine or Improve an Existing Caption")
    st.caption("Paste any caption you've written (or one generated before) and let Grok make it 2-5x better for engagement.")
    
    existing_caption = st.text_area(
        "Paste your current caption here",
        height=150,
        placeholder="e.g. New hair straightener just arrived 🔥 Gets your hair silky smooth in minutes. Link in bio!"
    )
    
    refine_platform = st.selectbox("Optimize for which platform?", ["Instagram", "Facebook", "X (Twitter)"], key="refine_platform")
    refine_goal = st.text_input("What do you want to improve?", placeholder="Stronger hook, more comments, better CTA, shorter version, more emotional...")
    
    if st.button("✨ Refine This Caption", type="primary", disabled=not (api_key and existing_caption.strip())):
        with st.spinner("Improving your caption..."):
            client = get_xai_client(api_key)
            refine_prompt = f"""You are an expert social media copywriter. 
Refine and dramatically improve the following caption for {refine_platform}.

Original Caption:
{existing_caption}

User's goal for improvement: {refine_goal or "Make it more engaging, higher converting, and algorithm-friendly while keeping the core message."}

Provide:
1. 2-3 improved versions with different angles/hooks
2. For each: Explain the key improvements
3. Suggested hashtags
4. Image prompt if visual content makes sense

Output in clean, copy-ready format."""

            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are PostForge AI, a master at turning good captions into viral ones."},
                        {"role": "user", "content": refine_prompt}
                    ],
                    temperature=0.75,
                    max_tokens=1500
                )
                refined = response.choices[0].message.content
                st.markdown("### Improved Versions")
                st.markdown(refined)
            except Exception as e:
                st.error(f"Error: {e}")

# ==================== FOOTER / TIPS ====================
st.divider()

with st.expander("💡 Pro Tips from a Creator (Mohammed Taha Khan style)"):
    st.markdown("""
    - **Hook test**: Read only the first line. If it doesn't make you curious or emotional in 1 second → rewrite.
    - **For IG Reels / Stories**: Use the caption to drive people to watch the full video ( "Wait till the end 👀" ).
    - **Product posts**: Always show transformation + social proof. "I used this for 14 days and..." performs insanely well.
    - **X growth hack**: Post 3-5 times/day with different hooks on same topic. One will hit.
    - **Save this app**: Add to home screen on your phone for daily use while creating content.
    """)

st.caption("PostForge AI v1.0 • Built with Grok • Tailored for high-output creators • Your data & API key stay private")

# Auto-load last generation if exists
if st.session_state.last_generation and "last_generation" in st.session_state:
    if st.button("🔄 Show last generated posts again"):
        parse_and_display_variations(st.session_state.last_generation, "Last Platform")