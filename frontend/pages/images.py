import streamlit as st
import os
from pathlib import Path
import random
import base64
from PIL import Image

#page title and layout
st.set_page_config(page_title="🌿 ESG Image Gallery", page_icon="🖼️", layout="wide")

#custom CSS
def apply_custom_styles():
    st.markdown(
        """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(to right, #002855, #004d99);
                color: white;
            }
            .stApp {
                background: black;
            }
            .image-container:hover {
                transform: scale(1.08);
                transition: all 0.3s ease-in-out;
                filter: brightness(1.2);
            }
            .header-text {
                font-size: 40px;
                font-weight: bold;
                color: #FFD700;
                text-align: center;
                text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.8);
            }
            .subheader-text {
                font-size: 26px;
                font-weight: bold;
                color: #00A86B;
                margin-top: 20px;
                text-align: center;
                text-transform: uppercase;
            }
            .info-text {
                font-size: 20px;
                color: white;
                text-align: center;
            }
            .category-header {
                font-size: 24px;
                font-weight: bold;
                color: #FFA500;
                margin-top: 30px;
            }
            .separator {
                border-top: 2px solid rgba(255, 255, 255, 0.5);
                margin: 20px 0;
            }
            .stButton > button {
                border-radius: 10px;
                background: linear-gradient(135deg, #007BFF, #00A86B);
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                transition: 0.3s;
                border: none;
            }
            .stButton > button:hover {
                background: linear-gradient(135deg, #00A86B, #007BFF);
                transform: scale(1.05);
            }
            .stTextArea textarea {
                background: linear-gradient(135deg, #00A86B, #007BFF);
                color: #000000 !important;
                border-radius: 8px;
            }
            .metric-card {
                background: linear-gradient(135deg, #007BFF 30%, #00A86B 100%);
                padding: 20px;
                border-radius: 12px;
                color: white;
                text-align: center;
                font-size: 22px;
                font-weight: bold;
                margin: 10px 0;
                box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.2);
            }
        </style>
        """,
        unsafe_allow_html=True
    )



def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("logo.png")

st.markdown(
    f"""
    <style>
        .logo-container {{
            
            top: 1;
            left: 1;
            z-index: 9999;
            padding: 0;
            margin: 0;
        }}
        .logo-container img {{
            width: 70px;  /* Adjust the size as needed */
            padding: 0;
            margin: 0;
        }}
    </style>
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}">
    </div>
    """,
    unsafe_allow_html=True
)

apply_custom_styles()

#header
st.markdown('<p class="header-text">🖼️ ESG Image Gallery</p>', unsafe_allow_html=True)
st.markdown('<p class="info-text">Explore ESG-related insights through visually engaging data-driven images.</p>', unsafe_allow_html=True)

#image categories
categories = {
    "📊 Results for Agent Training": "/Users/kdn_aisashwat/Desktop/esg-investment-advisor /results/agent_results",
    "📈 SHAP Plots for Agent": "/Users/kdn_aisashwat/Desktop/esg-investment-advisor /results/agent_shap",
    "🔍 SHAP Plots for Sentiment Analysis Model": "/Users/kdn_aisashwat/Desktop/esg-investment-advisor /results/sentiment_shap",
    "🚨 SHAP Plots for Greenwashing Detection Model": "/Users/kdn_aisashwat/Desktop/esg-investment-advisor /results/greenwashing_shap",
}

def display_images(folder_path):
    folder = Path(folder_path)
    if not folder.exists():
        st.warning(f"⚠️ Folder '{folder_path}' not found. Please check the path.")
        return
    
    images = [f for f in folder.iterdir() if f.suffix.lower() in ['.png', '.jpg', '.jpeg']]
    random.shuffle(images) 

    if images:
        num_cols = min(4, len(images))  #adjust columns dynamically
        cols = st.columns(num_cols)
        
        for index, image in enumerate(images):
            with cols[index % num_cols]:
                st.image(str(image), caption=image.name, use_container_width=True)
                st.markdown("<div class='image-container'></div>", unsafe_allow_html=True)
    else:
        st.info("🚫 No images found in this category.")

#loop through categories and display images under each header
for category, folder in categories.items():
    st.markdown(f'<p class="subheader-text">{category}</p>', unsafe_allow_html=True)
    display_images(folder)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True) 
