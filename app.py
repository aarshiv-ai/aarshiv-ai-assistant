import streamlit as st
import requests

st.set_page_config(page_title="AarShiv.ai Assistant", page_icon="🤖")
st.title("🤖 AarShiv.ai Content Assistant")
st.caption("Generate brand-aligned content or get IG strategy ideas.")

# ---------------------
# Mode Selection
# ---------------------
mode = st.radio("Choose Assistant Mode", ["📢 Content Generator", "📸 Instagram Strategy Helper"])

# ---------------------
# Shared Config
# ---------------------
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": "Bearer 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",  # Replace with your actual Groq API Key
    "Content-Type": "application/json"
}

# ---------------------
# Mode 1: Content Generator
# ---------------------
if mode == "📢 Content Generator":
    content_type = st.selectbox("Platform", ["LinkedIn", "Instagram", "Email"])
    user_input = st.text_area("📝 What's the topic?", height=150)

    if st.button("Generate Content"):
        if not user_input.strip():
            st.warning("⚠️ Please enter a topic.")
        else:
            with st.spinner("Generating content..."):

                brand_style = """
You are a content assistant for AarShiv.ai — a company that builds AI tools, chatbots, dashboards, and automation systems for creators and startups.
Write professional and engaging content in the tone of AarShiv.ai: friendly, clear, tech-savvy, and results-oriented. Use a confident, helpful tone suitable for the selected platform. Do not include taglines or meta instructions. Just give the final content ready to post or send.
"""

                examples = {
                    "LinkedIn": """
Write a LinkedIn post that starts with a hook or insight, uses 1-2 emojis max, and ends with a CTA or reflection. Keep it professional, startup-focused, and concise.
""",
                    "Instagram": """
Write a short, engaging Instagram caption that is visual, emoji-friendly, and bold. Focus on creators, tools, and innovation. Use relevant hashtags.
""",
                    "Email": """
Write a concise, friendly, and persuasive professional email. Skip greetings/closings if not asked. Get straight to the point.
"""
                }

                system_prompt = brand_style + examples[content_type]
                payload = {
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Write a {content_type} post about: {user_input}"}
                    ]
                }

                try:
                    response = requests.post(url, headers=headers, json=payload)
                    content = response.json()["choices"][0]["message"]["content"]

                    # Clean meta lines
                    lines = content.split('\n')
                    filtered = [l for l in lines if not any(x in l.lower() for x in ["feel free", "proofread", "tagline", "aims to"])]
                    st.success(f"✅ {content_type} Content:")
                    st.markdown(f"```text\n{chr(10).join(filtered).strip()}\n```")

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ---------------------
# Mode 2: IG Strategy Helper
# ---------------------
else:
    ig_format = st.selectbox("Choose Instagram Format", ["Carousel", "Post", "Reel"])
    ig_topic = st.text_area("🎯 Enter your topic", placeholder="e.g. How our chatbot works", height=100)

    if st.button("Suggest IG Ideas"):
        if not ig_topic.strip():
            st.warning("⚠️ Please enter a topic.")
        else:
            with st.spinner("Generating Instagram strategy..."):

                prompt = f"""
You are a creative assistant at AarShiv.ai, helping generate Instagram {ig_format.lower()} ideas for tech startups, automation tools, and AI services.

The tone is clear, exciting, and startup-friendly. Give 3 creative suggestions for {ig_format.lower()}s about:
'{ig_topic}'.
Each suggestion should be short and actionable.
"""

                payload = {
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": "system", "content": "You are a tech-savvy Instagram content strategist for a SaaS/AI brand."},
                        {"role": "user", "content": prompt}
                    ]
                }

                try:
                    response = requests.post(url, headers=headers, json=payload)
                    ideas = response.json()["choices"][0]["message"]["content"]
                    st.success(f"✅ {ig_format} Suggestions:")
                    st.markdown(ideas.strip())
                except Exception as e:
                    st.error(f"❌ Error: {e}")
