'''# spam_ui.py
import streamlit as st
import pickle

# ✅ Use st.cache_resource for models or other reusable resources
@st.cache_resource
def load_model():
    with open('spam_classifier_model.pkl', 'rb') as f:
        return pickle.load(f)

st.set_page_config(page_title="Spam Detector", layout="centered")

clf = load_model()

st.title("📧 Spam Message Classifier")
st.write("Type or paste an SMS/email/message below to check if it's spam.")

text = st.text_area("Message", height=180)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Check"):
        if not text.strip():
            st.warning("Please enter a message.")
        else:
            pred = clf.predict([text])[0]
            try:
                prob = clf.predict_proba([text])[0][1]
                prob_pct = f"{prob * 100:.1f}%"
            except Exception:
                prob_pct = "N/A"

            if pred == 1:
                st.error(f"🚨 Spam detected (probability: {prob_pct})")
            else:
                st.success(f"✅ Not spam (probability: {prob_pct})")

with col2:
    if st.button("Clear"):
        st.rerun()  # ✅ Already correct in modern Streamlit

st.markdown("---")
st.write("**Example inputs:**")
st.write("- Free tickets for IPL")
st.write("- Hey, are we meeting today?")'''






# spam_ui_ocr.py
import streamlit as st
import pickle
import time
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- Load Model ---
@st.cache_resource
def load_model():
    with open('spam_classifier_model.pkl', 'rb') as f:
        return pickle.load(f)

clf = load_model()

# --- Page Setup ---
st.set_page_config(page_title="Smart Spam Detector", layout="centered")

# --- Custom CSS (Gradient + Chat UI) ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(-45deg, #cfe9ff, #a3c9f9, #b5dcff, #d7f0ff);
        background-size: 400% 400%;
        animation: gradientMove 10s ease infinite;
        color: #00264d;
        font-family: "Poppins", sans-serif;
    }

    @keyframes gradientMove {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .main-title {
        font-size: 2.6em;
        font-weight: 700;
        color: #004a99;
        text-align: center;
        text-shadow: 1px 1px 10px rgba(255,255,255,0.6);
    }

    .subtitle {
        text-align: center;
        color: #003366;
        font-size: 1.2em;
        margin-bottom: 25px;
    }

    .stTextArea textarea {
        border-radius: 20px;
        border: 2px solid #66a3ff;
        background-color: rgba(255,255,255,0.9);
        font-size: 16px;
        padding: 12px;
    }

    .stButton button {
        background: linear-gradient(45deg, #66a3ff, #99ccff);
        color: white;
        border-radius: 30px;
        font-weight: 600;
        padding: 10px 35px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 3px 8px rgba(0,0,0,0.2);
    }

    .stButton button:hover {
        background: linear-gradient(45deg, #4d94ff, #80b3ff);
        transform: scale(1.05);
    }

    .chat-box {
        background-color: rgba(255,255,255,0.85);
        border-radius: 20px;
        padding: 25px;
        margin-top: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }

    .bubble {
        padding: 12px 18px;
        border-radius: 20px;
        max-width: 75%;
        margin: 10px auto;
        font-size: 16px;
        line-height: 1.4em;
    }

    .user-bubble {
        background-color: #d7efff;
        border: 1px solid #99ccff;
        color: #003366;
        text-align: right;
    }

    .bot-bubble {
        background-color: #e6f0ff;
        border: 1px solid #a3c2f2;
        color: #00264d;
        text-align: left;
    }

    </style>
""", unsafe_allow_html=True)

# --- Animated Title ---
placeholder = st.empty()
title_text = "💬 Smart Spam Detector"
display_text = ""
for char in title_text:
    display_text += char
    placeholder.markdown(f"<h1 class='main-title'>{display_text}</h1>", unsafe_allow_html=True)
    time.sleep(0.03)

st.markdown("<p class='subtitle'>Extract text from images and detect spam automatically ✨</p>", unsafe_allow_html=True)

# --- Image Upload for OCR ---
uploaded_image = st.file_uploader("📷 Upload an image containing text (JPEG/PNG)", type=["jpg", "jpeg", "png"])

extracted_text = ""
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="🖼️ Uploaded Image", use_container_width=True)
    with st.spinner("Extracting text from image... 🔍"):
        extracted_text = pytesseract.image_to_string(image)
        time.sleep(1)
    st.success("✅ Text extracted successfully!")

# --- Input Area (Pre-filled with OCR text if available) ---
# st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
text = st.text_area("✉️ Type or edit the message here", value=extracted_text, height=180)

col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Analyze"):
        if not text.strip():
            st.warning("⚠️ Please enter or extract a message.")
        else:
            with st.spinner("Analyzing message... 🤖"):
                time.sleep(1)
                pred = clf.predict([text])[0]
                try:
                    prob = clf.predict_proba([text])[0][1]
                    prob_pct = f"{prob * 100:.1f}%"
                except Exception:
                    prob_pct = "N/A"

                st.markdown(f"<div class='bubble user-bubble'>💬 {text}</div>", unsafe_allow_html=True)
                if pred == 1:
                    st.markdown(f"<div class='bubble bot-bubble'>🚨 <b>Spam Detected!</b><br>Confidence: {prob_pct}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='bubble bot-bubble'>✅ <b>Not Spam!</b><br>Confidence: {prob_pct}</div>", unsafe_allow_html=True)

with col2:
    if st.button("🧹 Clear"):
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<h3 style='color:#003366;'>💡 Try sample messages:</h3>
<ul style='color:#00264d; font-size:16px;'>
<li>🎁 You’ve won a free vacation! Click to claim.</li>
<li>📅 Are you joining the meeting today?</li>
<li>🏆 Get 90% off on your next purchase!</li>
</ul>
""", unsafe_allow_html=True)




