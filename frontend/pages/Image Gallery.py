import streamlit as st
import os
from pathlib import Path
import random
import base64
from PIL import Image

#page title and layout
st.set_page_config(page_title="🌿 ESG Image Gallery", page_icon="🖼️", layout="wide")

#custom CSS
# Custom CSS for KPMG Branding
def apply_custom_styles():
    st.markdown(
        """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(to right, #002E6D, #0057B8);
                color: white;
            }
            [data-testid="stSidebar"] {
                background: #aceaff;
                padding: 25px;
                border-right: 4px solid rgb(0, 192, 174);
                color: #FFFFFF !important;
            }
            [data-testid="stSidebarContent"] {
                background: #aceaff;
                color: #FFFFFF !important;
                font-size: 16px;
            }
            .stApp {
                background: white;
            }
            .image-container:hover {
                transform: scale(1.08);
                transition: all 0.3s ease-in-out;
                filter: brightness(1.2);
            }
            .header-text {
                font-size: 52px;
                font-weight: bold;
                
                color: rgb(30, 73, 226);
                text-align: left;
                text-shadow: 2px 2px 10px rgba(255, 255, 255, 0.8);
            }
            .subheader-text {
                font-size: 26px;
                
                color: rgb(30, 73, 226);;
                margin-top: 20px;
                text-align: left;
                text-transform: uppercase;
            }
            .info-text {
                font-size: 20px;
                color: rgb(30, 73, 226);;
                text-align: left;
            }
            .category-header {
                font-size: 24px;
                
                color: rgb(30, 73, 226);;
                margin-top: 30px;
            }
            .separator {
                border-top: 2px solid rgba(255, 255, 255, 0.5);
                margin: 20px 0;
            }
            .stButton > button {
                border-radius: 10px;
                background: linear-gradient(135deg, #0057B8, #002E6D);
                color: white;
                
                padding: 10px 20px;
                transition: 0.3s;
                border: none;
            }
            .stButton > button:hover {
                background: linear-gradient(135deg, #002E6D, #0057B8);
                transform: scale(1.05);
            }
            .metric-card {
                background: linear-gradient(135deg, #0057B8 30%, #002E6D 100%);
                padding: 20px;
                border-radius: 12px;
                color: white;
                text-align: center;
                font-size: 22px;
                
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

# Encode the logo
logo_base64 = get_base64_image("logo.png")

# Insert logo at the top of the sidebar
st.sidebar.markdown(
    f"""
    <style>
        .sidebar-logo {{
            display: flex;
            justify-content: left;
            align-items: left;
            margin-top: -350px;  /* Move logo up */
            margin-bottom: 20px; /* Add some space below */
        }}
        .sidebar-logo img {{
            width: 120px;  /* Adjust logo size */
        }}
    </style>
    <div class="sidebar-logo">
        <img src="data:image/png;base64,{logo_base64}">
    </div>
    """,
    unsafe_allow_html=True
)

apply_custom_styles()

#header
st.title('🖼️ ESG Image Gallery')
st.markdown('<p class="info-text">Explore ESG-related insights through visually engaging data-driven images.</p>', unsafe_allow_html=True)

st.markdown("-------")

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
    st.markdown("-------")
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True) 
