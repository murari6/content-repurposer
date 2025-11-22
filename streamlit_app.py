import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Viral Content Converter",
    page_icon="🚀",
    layout="wide"  # ⬅️ This makes the app full-width!
)

# Inject Custom CSS for that "SaaS" Look
st.markdown("""
    <style>
    /* 1. Background - Dark Modern Gradient */
    .stApp {
        background: linear-gradient(to bottom right, #0e1117, #131720, #0e1117);
    }
    
    /* 2. The Main Title */
    h1 {
        color: #FFFFFF;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        padding-bottom: 20px;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    
    /* 3. The "Generate" Button - Glowing Gradient */
    .stButton>button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000000;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-size: 18px;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.4);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 201, 255, 0.6);
    }
    
    /* 4. Text Areas & Inputs */
    .stTextArea>div>div>textarea {
        background-color: #1E232F;
        color: white;
        border-radius: 10px;
        border: 1px solid #30363D;
    }
    .stSelectbox>div>div>div {
        background-color: #1E232F;
        color: white;
        border-radius: 10px;
    }
    
    /* 5. Success/Info Boxes */
    .stAlert {
        background-color: #1E232F;
        border: 1px solid #30363D;
        color: #E6EDF3;
    }
    </style>
""", unsafe_allow_html=True)

# --- 🔒 LOGIN SYSTEM ---
ACCESS_PASSWORD = "money2025" 

with st.sidebar:
    st.markdown("### 🔐 VIP Access")
    user_pass = st.text_input("Enter Password", type="password", help="Ask the admin for access.")
    
    if user_pass != ACCESS_PASSWORD:
        st.warning("🔒 Please log in to unlock the tool.")
        st.info("Don't have a password? Contact the owner.")
        st.stop()
    
    st.success("Welcome back, Creator! 🚀")
    st.markdown("---")
    st.caption("Professional Plan Active")

# --- 2. MAIN APP LAYOUT ---
# Centered Header
st.markdown("<h1>🚀 YouTube to Viral Post Converter</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e; margin-bottom: 40px;'>Turn raw video transcripts into polished social media gold in seconds.</p>", unsafe_allow_html=True)

# Create two main columns for better layout
col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    st.subheader("1️⃣ Input")
    transcript = st.text_area(
        "Paste Video Transcript", 
        height=400, 
        placeholder="Paste your video text here... (We'll handle the rest)"
    )

with col2:
    st.subheader("2️⃣ Settings")
    
    platform = st.selectbox(
        "Output Platform",
        ["Twitter/X Thread (Viral)", "LinkedIn Post (Professional)", "TikTok Script (Engaging)", "Blog Post (SEO Optimized)"],
        index=0
    )
    
    tone = st.select_slider(
        "Content Tone", 
        options=["😂 Funny", "🙂 Casual", "🧐 Professional", "🤯 Controversial"],
        value="🙂 Casual"
    )
    
    st.markdown("###") # Spacer
    
    # The Big Magic Button
    generate_btn = st.button("✨ Generate Magic Content")

# --- 3. AI LOGIC (Secure) ---
def generate_content(text, platform, tone):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a world-class social media copywriter.
        Task: Rewrite the following transcript into a {platform}.
        Tone: {tone}.
        
        formatting_rules:
        - Use short, punchy sentences.
        - Use relevant emojis.
        - If Twitter: Create a numbered thread.
        - If LinkedIn: Use a strong "Hook" sentence at the start.
        
        Transcript:
        {text}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- 4. OUTPUT DISPLAY ---
if generate_btn:
    if not transcript:
        st.error("⚠️ Please paste a transcript first!")
    else:
        with st.spinner("🤖 Analyzing video structure... Writing viral copy..."):
            result = generate_content(transcript, platform, tone)
            
            st.markdown("---")
            st.subheader("🎉 Your Viral Content")
            st.balloons() # Fun animation
            
            # Output container with copy button
            st.code(result, language="markdown")
            st.caption("Tip: Click the copy icon in the top right of the box above!")
