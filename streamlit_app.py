import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="Viral Content Converter", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom right, #0e1117, #131720, #0e1117); }
    h1 { color: white; text-align: center; text-shadow: 0 0 10px rgba(0, 255, 255, 0.3); }
    .stButton>button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: black; font-weight: bold; border-radius: 12px; height: 50px; width: 100%; border: none;
    }
    .stButton>button:hover { transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

# --- 🔒 SECURITY SYSTEM (UNCRACKABLE) ---
def check_login():
    # 1. Look for password in the Secure Vault (Secrets)
    if "ACCESS_PASSWORD" not in st.secrets:
        st.error("⚠️ Security Error: Password not set in Secrets.")
        st.stop()
    
    correct_password = st.secrets["ACCESS_PASSWORD"]
    
    # 2. Sidebar Login
    with st.sidebar:
        st.header("🔒 Login")
        input_pass = st.text_input("Enter Access Password", type="password")
        
        if input_pass != correct_password:
            st.warning("🔒 Please log in to use the tool.")
            st.stop() # 🛑 BLOCKS EVERYTHING BELOW THIS LINE
        
        st.success("✅ Access Granted")

# Run the security check before loading ANYTHING else
check_login()

# --- ⬇️ EVERYTHING BELOW IS INVISIBLE UNTIL LOGGED IN ⬇️ ---

# --- 2. MAIN APP LOGIC ---
st.markdown("<h1>🚀 YouTube to Viral Post Converter</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    transcript = st.text_area("Input Transcript", height=300)

with col2:
    platform = st.selectbox("Output Format", ["Twitter Thread", "LinkedIn Post", "TikTok Script"])
    tone = st.select_slider("Tone", options=["Funny", "Casual", "Professional"])
    if st.button("✨ Generate Content"):
        if not transcript:
            st.error("Please paste text first.")
        else:
            try:
                # Securely fetch API Key
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                with st.spinner("Generating..."):
                    prompt = f"Rewrite as {platform} in {tone} tone: {transcript}"
                    response = model.generate_content(prompt)
                    
                    st.markdown("---")
                    st.balloons()
                    st.subheader("Result:")
                    st.code(response.text, language="markdown")
            except Exception as e:
                st.error(f"Error: {str(e)}")
