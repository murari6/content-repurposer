import streamlit as st
import google.generativeai as genai

# --- 1. App Config ---
st.set_page_config(page_title="Viral Content Repurposer", page_icon="🚀")

# --- 🔒 LOGIN SYSTEM ---
# The password to sell access
ACCESS_PASSWORD = "money2025" 

with st.sidebar:
    st.header("🔒 Login")
    user_pass = st.text_input("Enter Access Password", type="password")
    
    if user_pass != ACCESS_PASSWORD:
        st.warning("Please log in to use the tool.")
        st.stop()  # 🛑 Stops here if wrong password
    
    st.success("Access Granted! ✅")

# --- 2. Main Interface ---
st.title("🚀 YouTube to Viral Post Converter")
st.caption("Professional Edition")

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

# --- 3. AI Logic (Hidden Key) ---
def generate_content(text, platform, tone):
    # GRAB KEY FROM SECRETS (Hidden from user)
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Using the stable model
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
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
    if not transcript:
        st.warning("Please paste a transcript first.")
    else:
        with st.spinner("Generating content..."):
            try:
                result = generate_content(transcript, platform, tone)
                st.subheader("Your Content:")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
