import streamlit as st
import google.generativeai as genai

# --- 1. App Config ---
st.set_page_config(page_title="Viral Content Repurposer", page_icon="🚀")
st.title("🚀 YouTube to Viral Post Converter")
st.caption("Powered by Gemini 2.5 Flash")

# --- 2. Sidebar: API Key Only ---
with st.sidebar:
    st.header("🔑 Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Using Model: gemini-2.5-flash")

# --- 3. Main Interface ---
col1, col2 = st.columns(2)

with col1:
    transcript = st.text_area(
        "Paste Video Transcript Here:", 
        height=300, 
        placeholder="Paste your text here..."
    )

with col2:
    platform = st.selectbox(
        "Choose Output Format:",
        ["Twitter/X Thread", "LinkedIn Post", "TikTok Script", "Blog Article"]
    )
    tone = st.select_slider("Select Tone:", options=["Funny", "Casual", "Professional"])

# --- 4. AI Logic (Hardcoded to 2.5) ---
def generate_content(text, platform, tone, key):
    genai.configure(api_key=key)
    
    # FORCE GEMINI 2.5 FLASH
    # If this fails, check if your API key has access to 2.5 yet.
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    prompt = f"""
    Act as an expert copywriter.
    Task: Rewrite this transcript into a {platform}.
    Tone: {tone}.
    Transcript: {text}
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- 5. Generate Button ---
if st.button("✨ Generate Magic Content", type="primary"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    elif not transcript:
        st.warning("Please paste a transcript.")
    else:
        with st.spinner("Gemini 2.5 is thinking..."):
            try:
                result = generate_content(transcript, platform, tone, api_key)
                st.subheader("Your Content:")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.error("Note: If you get a 404, 'gemini-2.5-flash' might not be enabled for your key yet. Try changing the code to 'gemini-1.5-flash' as a backup.")
