import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Viral Content Converter", page_icon="🚀", layout="wide")

# --- 2. HIGH-END CSS STYLING ---
st.markdown("""
    <style>
    /* Global Text Color Fix */
    .stApp, .stMarkdown, p, h1, h2, h3, label {
        color: #FFFFFF !important;
    }

    /* Background - Deep Space Gradient */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    
    /* Title Styling */
    h1 {
        font-size: 3rem !important;
        background: -webkit-linear-gradient(#00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 10px;
    }
    
    /* Input Fields - Dark Mode Style */
    .stTextArea textarea {
        background-color: #1E293B !important;
        color: #E2E8F0 !important;
        border: 1px solid #334155 !important;
        border-radius: 12px;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1E293B !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 12px;
    }
    
    /* The 'Generate' Button - Neon Glow */
    .stButton > button {
        background: linear-gradient(45deg, #3B82F6, #8B5CF6);
        color: white !important;
        border: none;
        border-radius: 12px;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.5);
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px 0 rgba(59, 130, 246, 0.7);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

# --- 🔒 SECURITY CHECK (Do not remove) ---
def check_login():
    # If no password set in Secrets, allow access (for testing) 
    # OR block it. Safer to require it.
    if "ACCESS_PASSWORD" not in st.secrets:
        st.warning("⚠️ Password not configured in Secrets.")
        return # Allow pass for testing if secrets missing
        
    correct_password = st.secrets["ACCESS_PASSWORD"]
    
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/622/622669.png", width=50)
        st.markdown("### 🔐 Member Login")
        input_pass = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter Password")
        
        if input_pass != correct_password:
            st.info("Enter password to unlock.")
            st.stop()
        
        st.success("✅ Access Granted")

check_login()

# --- 3. MAIN APP LAYOUT ---

# Header
st.markdown("<h1>YouTube to Viral Post</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 1.2rem;'>The Secret Weapon for Content Creators</p>", unsafe_allow_html=True)
st.divider()

# Layout
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown("### 📹 Input Video Text")
    transcript = st.text_area(
        "Transcript", 
        height=350, 
        label_visibility="collapsed",
        placeholder="Paste the full video transcript here... (Ctrl+V)"
    )

with col2:
    st.markdown("### ⚙️ Configuration")
    
    # Card Container
    with st.container():
        platform = st.selectbox(
            "Output Format",
            ["Twitter Thread (Viral)", "LinkedIn Post (Story)", "TikTok Script (Visual)", "Blog Article (SEO)"]
        )
        
        st.markdown("<br>", unsafe_allow_html=True) # Spacer
        
        tone = st.select_slider(
            "Writing Tone", 
            options=["🤪 Funny", "😎 Casual", "🧐 Professional", "🔥 Controversial"],
            value="😎 Casual"
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True) # Spacer
        
        if st.button("✨ GENERATE CONTENT"):
            if not transcript:
                st.toast("⚠️ Please paste a transcript first!", icon="⚠️")
            else:
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    with st.spinner("🦄 Writing viral magic..."):
                        prompt = f"Rewrite this video transcript as a {platform}. Tone: {tone}. Text: {transcript}"
                        response = model.generate_content(prompt)
                        
                        # Result Area
                        st.markdown("---")
                        st.subheader("🎉 Here is your content:")
                        st.code(response.text, language="markdown")
                        st.balloons()
                except Exception as e:
                    st.error(f"System Error: {e}")
