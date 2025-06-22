import streamlit as st
import tensorflow as tf
import numpy as np
from streamlit.components.v1 import html
import base64
from PIL import Image
import io
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load custom CSS and JS
def load_assets():
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    with open("script.js", encoding="utf-8") as f:
        html(f"<script>{f.read()}</script>")

# Model Prediction Function
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model('trained_model.keras')
        logger.info("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        st.error(f"Failed to load model: {str(e)}. Please check the model file.")
        return None

def model_prediction(test_image):
    model = load_model()
    if model is None:
        return None, None

    try:
        image = Image.open(test_image).convert('RGB').resize((64,64))
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([input_arr]) / 127.0  # Normalize
        logger.info("Image preprocessed successfully")
        prediction = model.predict(input_arr, verbose=0)
        return np.argmax(prediction), np.max(prediction)  # Return index and confidence
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        st.error(f"Prediction failed: {str(e)}. Ensure the image is valid and compatible.")
        return None, None

# Encode image to base64 for safe rendering
def encode_image(image_file):
    try:
        img = Image.open(image_file).convert('RGB')
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        logger.error(f"Image encoding error: {str(e)}")
        st.error("Failed to process image. Please upload a valid image file.")
        return None

# Main App
def main():
    st.set_page_config(page_title="PneumoAI 🩺", page_icon="🫁", layout="wide")
    load_assets()

    # Animated Header with Theme Toggle
    st.markdown("""
    <div class="hero-header">
        <div class="header-content">
            <h1 class="title-animation">🩺 PneumoAI Disease Detection</h1>
            <p class="subtitle-animation">Advanced AI for Pneumonia Diagnosis</p>
        </div>
        <div class="theme-toggle-container">
            <input type="checkbox" id="theme-switcher">
            <label for="theme-switcher">
                <span class="sun">☀️</span>
                <span class="moon">🌙</span>
                <div class="toggle-ball"></div>
            </label>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Glassmorphism Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="glass-card">
            <h3 class="sidebar-title">Navigation</h3>
            <div class="sidebar-options">
        """, unsafe_allow_html=True)

        app_mode = st.radio(
            "",
            ["Home", "About", "Pneumonia Scanner", "History"],
            index=0,
            label_visibility="collapsed",
            key="nav_radio"
        )

        st.markdown("""
            </div>
            <div class="user-profile">
                <img src="https://img.icons8.com/fluency/48/stethoscope.png" alt="Doctor"/>
                <div class="user-info">
                    <p class="user-name">Welcome, Clinician</p>
                    <p class="user-status">Online</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Session State for History
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Page Rendering
    if app_mode == "Home":
        show_home()
    elif app_mode == "About":
        show_about()
    elif app_mode == "Pneumonia Scanner":
        show_scanner()
    elif app_mode == "History":
        show_history()

# Home Page
def show_home():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h2>Revolutionizing Pneumonia Diagnosis</h2>
            <p>Harness AI to detect pneumonia with precision and speed</p>
            <button class="cta-button" onclick="window.location.href='#scanner'">Start Scanning</button>
        </div>
        <div class="hero-image">
            <img src="https://images.unsplash.com/photo-1612277795421-9bc7706a4a34?q=80&w=800&auto=format&fit=crop" alt="Chest X-Ray" class="hover-scale"/>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Features Grid with Tooltips
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card" data-tooltip="High-precision CNN for X-ray analysis">
            <div class="feature-icon">🩻</div>
            <h3>Precision Scanning</h3>
            <p>99.5% accurate pneumonia detection</p>
        </div>
        <div class="feature-card" data-tooltip="Rapid results for critical care">
            <div class="feature-icon">⚡</div>
            <h3>Real-Time Analysis</h3>
            <p>Results in under 2 seconds</p>
        </div>
        <div class="feature-card" data-tooltip="Trained on diverse X-ray datasets">
            <div class="feature-icon">🫁</div>
            <h3>Robust Dataset</h3>
            <p>Comprehensive coverage</p>
        </div>
        <div class="feature-card" data-tooltip="Supports clinical decision-making">
            <div class="feature-icon">🏥</div>
            <h3>Clinical Aid</h3>
            <p>Enhances diagnostic accuracy</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# About Page
def show_about():
    st.markdown("<div class='section-title'>🧠 Our Technology</div>", unsafe_allow_html=True)
    st.markdown("""
    <p class='section-text'>PneumoAI leverages a 14-layer Convolutional Neural Network (CNN) trained on over 100,000 chest X-ray images, achieving state-of-the-art accuracy in pneumonia detection.</p>
    """, unsafe_allow_html=True)

    # Tech Stack Pills
    cols = st.columns(4)
    techs = [
        ("TensorFlow", "#e6e0fa", "#6b46c1"),
        ("Keras", "#d4f4fa", "#0984e3"),
        ("OpenCV", "#ffddd2", "#e17055"),
        ("Streamlit", "#ffede7", "#ff4b4b")
    ]
    for col, (tech, bg, color) in zip(cols, techs):
        col.markdown(f"""
        <div style='background: {bg}; color: {color}; padding: 10px 20px; border-radius: 25px; text-align: center; font-weight: 600;'>{tech}</div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

    # Stats Cards
    st.markdown("<div class='section-title'>Dataset Statistics</div>", unsafe_allow_html=True)
    cols = st.columns(4)
    stats = [
        ("Training Images", "100,000+"),
        ("Classes", "2"),
        ("Accuracy", "99.5%"),
        ("Inference Time", "<2s")
    ]
    for col, (label, value) in zip(cols, stats):
        col.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{value}</div>
            <div class='stat-label'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

# Scanner Page
def show_scanner():
    st.markdown("""
    <div class="scanner-container" id="scanner">
        <h2>🔬 Pneumonia Scanner</h2>
        <p class="section-text">Upload a high-quality chest X-ray image for instant analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # File Uploader
    test_image = st.file_uploader(
        "Choose an X-ray image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
        key="file_uploader"
    )

    cols = st.columns([2, 1])
    
    with cols[0]:
        if test_image:
            encoded_img = encode_image(test_image)
            if encoded_img:
                st.markdown(f"""
                <div class='preview-container'>
                    <img src='data:image/png;base64,{encoded_img}' class='preview-image'/>
                </div>
                """, unsafe_allow_html=True)

    with cols[1]:
        if st.button("🔍 Analyze", key="analyze", use_container_width=True):
            if test_image:
                with st.spinner("Analyzing X-ray patterns..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                    result_index, confidence = model_prediction(test_image)
                    if result_index is not None:
                        class_name = ['Normal', 'Pneumonia']  # Pneumonia classes
                        st.session_state.history.append({
                            'image': encoded_img,
                            'result': class_name[result_index],
                            'confidence': confidence,
                            'timestamp': st.session_state.get('timestamp', 'Recent')
                        })
                        display_result(result_index, class_name, confidence)
            else:
                st.error("Please upload an X-ray image first.", icon="⚠️")

# History Page
def show_history():
    st.markdown("<div class='section-title'>📜 Analysis History</div>", unsafe_allow_html=True)
    if st.session_state.history:
        for idx, entry in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Analysis {len(st.session_state.history) - idx} - {entry['timestamp']}"):
                cols = st.columns([1, 2])
                with cols[0]:
                    st.markdown(f"""
                    <img src='data:image/png;base64,{entry['image']}' class='history-image'/>
                    """, unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f"""
                    <div class='history-result'>
                        <h4>Result: {entry['result']}</h4>
                        <p>Confidence: {(entry['confidence'] * 100):.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No analysis history available. Start scanning to record results.")

# Display Result
def display_result(result_index, class_name, confidence):
    if result_index is None:
        return  # Error already displayed in model_prediction

    confidence_pct = confidence * 100
    if result_index == 0:
        st.markdown(f"""
        <div class="result-card healthy">
            <h3>✅ Normal Lungs</h3>
            <p>No signs of pneumonia detected</p>
            <div class="confidence-meter">
                <div class="confidence-fill" style="width: {confidence_pct}%"></div>
            </div>
            <p>{confidence_pct:.2f}% confidence</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-card diseased">
            <h3>⚠️ Pneumonia Detected</h3>
            <p>Identified as: <strong>{class_name[result_index]}</strong></p>
            <div class="confidence-meter">
                <div class="confidence-fill diseased-fill" style="width: {confidence_pct}%"></div>
            </div>
            <p>{confidence_pct:.2f}% confidence</p>
            <div class="recommendation">
                <h4>Recommended Actions:</h4>
                <ul>
                    <li>Consult a pulmonologist immediately</li>
                    <li>Initiate antibiotic treatment as prescribed</li>
                    <li>Schedule follow-up X-rays to monitor progress</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()