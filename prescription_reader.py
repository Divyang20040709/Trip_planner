import io
from PIL import Image
import streamlit as st
from google import genai
from google.genai import types

# Page configuration
st.set_page_config(
    page_title="MediScan AI | Prescription Assistant",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .prescription-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .sidebar-content {
        padding: 10px;
    }
    h1 {
        color: #1e3a8a;
    }
    </style>
""", unsafe_allow_html=True)

# API Key check
try:
    api_key = st.secrets.get("GEMINI_API_KEY")
except KeyError:
    st.error("❌ Gemini API Key not found. Please add it to your Streamlit Secrets.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# System Prompt
system_prompt = """
You are an intelligent medical assistant chatbot.
Your role is to help users understand doctor prescriptions by analyzing uploaded images and extracting relevant medical information.

Core Responsibilities:
1. Extract medicine names from the prescription.
2. Provide clear and simple explanations of each medicine:
   - Uses (what it's for)
   - Common side effects
   - Recommended dosage (if mentioned)
   - Important warnings
3. Tone: Helpful, calm, and informative.
4. Always include this disclaimer: "This information is for educational purposes only. Please consult a doctor or pharmacist before taking any medication."
"""

def generate_response(image_bytes):
    """Generates response using Gemini 3 Flash Preview as requested."""
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            system_prompt,
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            "Analyze this prescription image and provide a structured summary of each medicine found."
        ]
    )
    return response.text

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3022/3022137.png", width=100)
    st.title("MediScan AI")
    st.markdown("---")
    st.markdown("### 📋 How to Use")
    st.write("1. Upload a clear photo of your prescription.")
    st.write("2. Click 'Analyze Prescriptions'.")
    st.write("3. Review the AI-generated details.")
    
    st.markdown("---")
    st.warning("### ⚠️ Safety Disclaimer")
    st.info("This tool is AI-powered and for educational use only. Never change your medication without consulting a professional.")
    st.markdown("---")
    st.caption("Powered by Gemini 3 Flash Preview")

# Main Content
st.title("💊 Prescription Analysis Assistant")
st.markdown("Upload your prescription images below to get a clear, easy-to-understand breakdown of your medications.")

uploaded_files = st.file_uploader(
    "Choose prescription images", 
    accept_multiple_files=True, 
    type=["jpg", "jpeg", "png"],
    help="Upload clear images for better results"
)

if uploaded_files:
    st.markdown("### 📸 Uploaded Images")
    cols = st.columns(len(uploaded_files))
    for idx, uploaded_file in enumerate(uploaded_files):
        with cols[idx]:
            # Pre-load image to avoid MediaFileHandler issues
            img = Image.open(uploaded_file)
            st.image(img, width="stretch", caption=uploaded_file.name)

    if st.button("🚀 Analyze Prescriptions"):
        for uploaded_file in uploaded_files:
            with st.status(f"Analyzing {uploaded_file.name}...", expanded=True) as status:
                try:
                    # Read bytes for API call
                    uploaded_file.seek(0)
                    image_bytes = uploaded_file.read()
                    
                    response = generate_response(image_bytes)
                    
                    with st.expander(f"📄 Analysis for {uploaded_file.name}", expanded=True):
                        st.markdown(response)
                    
                    status.update(label=f"✅ Analysis for {uploaded_file.name} complete!", state="complete")
                    
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                    status.update(label=f"❌ Error in {uploaded_file.name}", state="error")
else:
    st.info("👋 Welcome! Please upload one or more prescription images to get started.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>© 2024 MediScan AI Assistant | Empowering health literacy</div>", unsafe_allow_html=True)