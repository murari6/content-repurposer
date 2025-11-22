import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Viral Content Converter", page_icon="🚀", layout="wide")

# --- 2. FORCE DARK MODE CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #000000, #1e1e1e, #0f2027, #203a43);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #333333; }
    .stApp, h1, h2, h3, label, p, div, span { color: #FFFFFF !important; }
    .stTextArea textarea, .stTextInput input {
        background-color: #1E1E1E !important; color: #FFFFFF !important; border: 1px solid #444444 !important;
    }
    div[data-baseweb="select"] > div { background-color: #1E1E1E !important; color: white !important; border: 1px solid #444444 !important; }
    div[data-baseweb="popover"] div { background-color: #1E1E1E !important; color: white !important; }
    div[data-baseweb="menu"] div { color: white !important; }
    .stButton > button {
        background: linear-gradient(90deg, #00C9FF, #92FE9D);
        color: black !important; font-weight: bold; border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIN LOGIC ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><h1 style='text-align: center;'>🔐 Creator Portal</h1>", unsafe_allow_html=True)
        password_attempt = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter VIP Password")
        
        if st.button("ENTER ACCESS"):
            if "ACCESS_PASSWORD" not in st.secrets:
                st.error("⚠️ Setup Error: Password not in Secrets.")
            elif password_attempt == st.secrets["ACCESS_PASSWORD"]:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect Password")
    st.stop()

# --- 4. SMART GENERATION LOGIC (The Fix) ---
def smart_generate(prompt, api_key):
    genai.configure(api_key=api_key)
    
    # List of models to try in order (Newest -> Oldest/Stable)
    models_to_try = [
        'gemini-1.5-flash',
        'gemini-1.5-flash-latest',
        'gemini-1.5-pro',
        'gemini-pro' # The "Old Reliable" backup
    ]
    
    last_error = ""
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text # If successful, return immediately
        except Exception as e:
            last_error = str(e)
            continue # If fail, try the next one in the list
            
    return f"Error: All models failed. Last error: {last_error}"

# --- 5. MAIN DASHBOARD ---
with st.sidebar:
    st.write("Logged in as VIP")
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
            with st.spinner("Thinking..."):
                prompt = f"Rewrite as {platform} in {tone} tone: {transcript}"
                # Use the new Smart Generator
                result = smart_generate(prompt, st.secrets["GOOGLE_API_KEY"])
                
                st.markdown("---")
                st.subheader("Result:")
                st.code(result)
                st.balloons()
