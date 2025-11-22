import streamlit as st
import google.generativeai as genai

# --- 1. App Config ---
st.set_page_config(page_title="Viral Content Repurposer", page_icon="🚀")
st.title("🚀 YouTube to Viral Post Converter")

# --- 2. Sidebar: API Key & Model Selector ---
with st.sidebar:
    st.header("🔑 Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    # Smart Model Selector
    selected_model = "gemini-2.5-flash" # Default fallback
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Auto-fetch available models
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Filter for 'flash' or 'pro' models which are best for text
            chat_models = [m for m in models if 'flash' in m or 'pro' in m]
            if chat_models:
                selected_model = st.selectbox("Select AI Model:", chat_models, index=0)
            else:
                st.error("No chat models found. Check your API Key permissions.")
        except Exception as e:
            st.warning(f"Could not list models: {e}")
            st.info("Using default model: gemini-2.5-flash")

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

# --- 4. AI Logic ---
def generate_content(text, platform, tone, model_name):
    # Use the selected model from sidebar
    model = genai.GenerativeModel(model_name)
    
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
        with st.spinner("AI is working..."):
            try:
                # Clean model name (remove 'models/' prefix if present)
                clean_model_name = selected_model.replace("models/", "")
                result = generate_content(transcript, platform, tone, clean_model_name)
                st.subheader("Your Content:")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.help("Try selecting a different model in the sidebar.")
