import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Viral Content Converter", page_icon="🚀", layout="wide")

# --- 2. SESSION STATE (Keeps you logged in) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 3. CUSTOM CSS (Background & Centering) ---
st.markdown("""
    <style>
    /* 1. The Background - Fusion of X, LinkedIn, TikTok Colors */
    .stApp {
        background: linear-gradient(120deg, #000000 30%, #0077B5 50%, #ff0050 80%);
        background-size: 200% 200%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. General Text Color */
    .stApp, h1, h2, h3, label, p { color: white !important; }
    
    /* 3. Input Fields (Dark Glass Look) */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px;
        text-align: center; 
    }
    
    /* 4. The Login Button */
    div.stButton > button {
        background: #00C9FF;
        color: black !important;
        border-radius: 25px;
        padding: 10px 30px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. THE LOGIN PAGE LOGIC ---
def check_password():
    # Get password from Secrets
    if "ACCESS_PASSWORD" not in st.secrets:
        st.error("⚠️ Admin: Please set ACCESS_PASSWORD in Secrets.")
        return False
    
    correct_password = st.secrets["ACCESS_PASSWORD"]
    
    if st.session_state.password_input == correct_password:
        st.session_state.authenticated = True
    else:
        st.error("❌ Wrong Password")

# IF NOT LOGGED IN -> SHOW CENTERED LOGIN PAGE
if not st.session_state.authenticated:
    # Use 3 columns to center the middle one
    col1, col2, col3 = st.columns([1, 1, 1]) # Middle column is the "Login Card"
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True) # Push it down
        st.image("https://cdn-icons-png.flaticon.com/512/12595/12595888.png", width=80) # Rocket Icon
        st.markdown("<h1 style='text-align: center;'>Creator Portal</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Login to access the Viral Converter</p>", unsafe_allow_html=True)
        
        st.text_input("Password", type="password", key="password_input", label_visibility="collapsed")
        st.button("ENTER", on_click=check_password)
        
    st.stop() # 🛑 STOP here so the app doesn't load behind the login screen

# --- 5. MAIN APP (Only loads after login) ---

# (Optional: Sidebar Logout Button)
with st.sidebar:
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

# HEADER
st.markdown("<h1>🚀 YouTube to Viral Post</h1>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown("### 📹 Input")
    transcript = st.text_area("Transcript", height=350, label_visibility="collapsed", placeholder="Paste transcript here...")

with col2:
    st.markdown("### ⚙️ Settings")
    platform = st.selectbox("Format", ["Twitter Thread", "LinkedIn Post", "TikTok Script", "Blog Article"])
    tone = st.select_slider("Tone", options=["Funny", "Casual", "Professional"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("✨ GENERATE"):
        if not transcript:
            st.warning("Please paste text first.")
        else:
            try:
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                with st.spinner("Writing..."):
                    prompt = f"Rewrite as {platform} in {tone} tone: {transcript}"
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.subheader("Result:")
                    st.code(response.text)
                    st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")
