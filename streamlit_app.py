import streamlit as st
import google.generativeai as genai

# --- 1. App Config ---
st.set_page_config(page_title="Viral Content Repurposer", page_icon="🚀")

# --- 🔒 LOGIN SYSTEM (The Money Maker) ---
# Change "money2025" to whatever password you want to sell
ACCESS_PASSWORD = "money2025" 

with st.sidebar:
    st.header("🔒 Login")
    user_pass = st.text_input("Enter Access Password", type="password")
    
    if user_pass != ACCESS_PASSWORD:
        st.warning("Incorrect or missing password.")
        st.stop()  # 🛑 THIS STOPS THE APP HERE IF PASSWORD IS WRONG
    
    st.success("Access Granted! ✅")
    st.divider()
    
    # --- Settings (Only visible after login) ---
    st.header("🔑 Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Using Model: gemini-2.5-flash")

# --- 2. Main Interface (Hidden until logged in) ---
st.title("🚀 YouTube to Viral Post Converter")
st.caption("Powered by Gemini 2.5 Flash")

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

# --- 3. AI Logic ---
def generate_content(text, platform, tone, key):
    genai.configure(api_key=key)
    # FORCE GEMINI 2.5
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    prompt = f"""
    Act as an expert copywriter.
    Task: Rewrite this transcript into a {platform}.
    Tone: {tone}.
    Transcript: {text}
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- 4. Generate Button ---
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
