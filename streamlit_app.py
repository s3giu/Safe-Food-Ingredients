import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURATION ---
# This looks for the key in Streamlit's internal secrets manager
api_key = st.secrets["AIzaSyBvCpvGYZ3070TXSWLb49YJJUiwWvT9JXk"]
app_password = st.secrets["pizza"]

genai.configure(api_key=api_key)

# --- PAGE SETUP ---
st.set_page_config(page_title="SafeEats Cloud", page_icon="☁️")

# --- CSS FOR "APP LIKE" FEEL ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div.stButton > button {
        width: 100%;
        background-color: #00CC96;
        color: white;
        font-weight: bold;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- PASSWORD LOGIN ---
# Keeps your app private for friends only
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Login")
    pwd = st.text_input("Enter Access Code", type="password")
    if st.button("Unlock"):
        if pwd == app_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong password.")
    st.stop()

# --- MAIN APP LOGIC ---
st.title("☁️ SafeEats Scanner")
st.caption("Powered by Google Gemini Flash")

img_file = st.file_uploader("Scan Label", type=["jpg", "png", "jpeg"])
camera_file = st.camera_input("Take Photo")

image_data = img_file if img_file else camera_file

if image_data:
    image = Image.open(image_data)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Analyze Ingredients"):
        with st.spinner("Consulting the Toxicology Database..."):
            try:
                # Use Gemini 1.5 Flash (Fast & Free)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = """
                You are a toxicology expert.
                1. Read the ingredients from this image.
                2. Identify ingredients that are: Carcinogenic, Endocrine Disruptors, or Banned in EU.
                3. Return a markdown table with columns: 'Ingredient', 'Risk', 'Reason'.
                4. If clean, say "✅ Safe".
                """
                
                response = model.generate_content([prompt, image])
                st.markdown("### 🔍 Verdict")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
