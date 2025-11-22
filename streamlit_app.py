import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Viral Content Converter", page_icon="🚀", layout="wide")

# --- 2. CUSTOM CSS (The "X/LinkedIn/TikTok" Theme) ---
st.markdown("""
    <style>
    /* Animated Background - Black/Blue/Pink Fusion */
    .stApp {
        background: linear-gradient(-45deg, #000000, #1e1e1e, #0077B5, #ff0050);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* White Text Everywhere */
    .stApp, h1, h2, h3, label, p, div { color: white !important; }
    
    /* Login Input Styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 10px;
        text-align: center;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00C9FF, #92FE9D);
        color: black !important;
        border-radius: 20px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. ROBUST LOGIN SYSTEM (Centered) ---
# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Login Logic
if not st.session_state.authenticated:
    # Create 3 columns to center the middle one
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>🔐 Creator Portal</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Enter your VIP Password to continue</p>", unsafe_allow_html=True)
        
        # Password Input
        password_attempt = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter Password Here")
        
        if st.button("ENTER ACCESS"):
            # Check if secrets exist first to prevent crash
            if "ACCESS_PASSWORD" not in st.secrets:
                st.error("⚠️ System Error: Password not set in Secrets.")
            elif password_attempt == st.secrets["ACCESS_PASSWORD"]:
                st.session_state.authenticated = True
                st.rerun() # Refresh to show the app
            else:
                st.error("❌ Incorrect Password")
    
    # Stop the app here if not logged in
    st.stop()

# --- 4. MAIN APP (Only visible after login) ---

# Logout button in sidebar
with st.sidebar:
    st.write(f"Logged in as VIP")
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

st.markdown("<h1 style='text-align: center;'>🚀 YouTube to Viral Post</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2], gap="medium")

with col1:
    st.markdown("### 📹 Video Transcript")
    transcript = st.text_area("Transcript", height=350, label_visibility="collapsed", placeholder="Paste transcript here...")

with col2:
    st.markdown("### ⚙️ Settings")
    platform = st.selectbox("Format", ["Twitter Thread", "LinkedIn Post", "TikTok Script", "Blog Article"])
    tone = st.select_slider("Tone", options=["Funny", "Casual", "Professional"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("✨ GENERATE MAGIC"):
        if not transcript:
            st.warning("Please paste text first.")
        else:
            try:
                # Check API Key existence
                if "GOOGLE_API_KEY" not in st.secrets:
                    st.error("⚠️ API Key missing in Secrets.")
                else:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    with st.spinner("Generating..."):
                        prompt = f"Rewrite as {platform} in {tone} tone: {transcript}"
                        response = model.generate_content(prompt)
                        st.markdown("---")
                        st.subheader("Result:")
                        st.code(response.text)
                        st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")
