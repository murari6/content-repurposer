import streamlit as st
import google.generativeai as genai

# --- 1. App Config & Layout ---
st.set_page_config(page_title="Viral Content Repurposer", page_icon="🚀")

st.title("🚀 YouTube to Viral Post Converter")
st.markdown("""
**Turn raw video transcripts into polished social media gold.** *Built with Gemini AI*
""")

# --- 2. Sidebar: API Key Input ---
with st.sidebar:
    st.header("🔑 Settings")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    st.markdown("[Get a Free Gemini API Key](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.info("Security Note: Your key is not saved permanently.")

# --- 3. Main Interface ---
col1, col2 = st.columns(2)

with col1:
    transcript = st.text_area(
        "Paste Video Transcript Here:", 
        height=300, 
        placeholder="So today I want to talk about how AI is changing the world..."
    )

with col2:
    platform = st.selectbox(
        "Choose Output Format:",
        ["Twitter/X Thread (Viral Style)", "LinkedIn Post (Professional)", "TikTok Script (Engaging)", "Blog Article (SEO Optimized)"]
    )
    
    tone = st.select_slider(
        "Select Tone:",
        options=["Funny", "Casual", "Professional", "Controversial"]
    )

# --- 4. The AI Logic ---
def generate_content(text, platform, tone, key):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash-002') # Fast & Free model
        
        prompt = f"""
        Act as an expert social media copywriter. 
        Task: Rewrite the following video transcript into a {platform}.
        Tone: {tone}.
        
        Rules:
        - If Twitter: Create a thread of 5-7 tweets. Number them. Use hooks.
        - If LinkedIn: Use short paragraphs, professional emojis, and a strong call to action.
        - If Blog: Use H2 headings and bullet points.
        
        Transcript:
        {text}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- 5. The 'Generate' Action ---
if st.button("✨ Generate Magic Content", type="primary"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar to proceed.")
    elif not transcript:
        st.warning("Please paste a transcript first.")
    else:
        with st.spinner("AI is writing your content..."):
            result = generate_content(transcript, platform, tone, api_key)
            st.subheader("Your Content:")
            st.markdown(result)
            st.download_button("Download Text", result)
