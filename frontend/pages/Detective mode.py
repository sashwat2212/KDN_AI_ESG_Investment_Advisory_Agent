import streamlit as st
import requests
import numpy as np
import pandas as pd
import plotly.express as px
import datetime
import plotly.graph_objects as go
from PIL import Image
import base64

@st.cache_data
def load_data():
    return pd.read_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /data_preprocessing/final_processed_esg_data.csv")  

df = load_data()

#mode section
# Custom CSS for styling
st.markdown(
    """
    <style>
        .esg-header {
            font-size: 32px;
            font-weight: bold;
            color: rgb(30, 73, 226);  /* KPMG Blue */
            text-align: center;
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
        .fraud-alert {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            border-radius: 10px;
        }
        .low-risk {
            background: #aceaff;
            padding: 15px;
            border-radius: 10px;
            color: black;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
        .high-risk {
            background: #aceaff;
            padding: 15px;
            border-radius: 10px;
            color: black;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
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

st.title('🔍 ESG Detective Mode - Fraud Likelihood Meter')

#dropdown 
selected_company = st.selectbox("Select a Company", ["Select..."] + list(df["Company"]))

#ESG details when a company is selected
if selected_company != "Select...":
    company_data = df[df["Company"] == selected_company]

    if not company_data.empty:
        st.markdown(f"<h3 style='color:#007BFF;'>ESG Breakdown for {selected_company}</h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("🌿 Environmental Score", company_data["Env_Score"].values[0])
        col2.metric("🤝 Social Score", company_data["Soc_Score"].values[0])
        col3.metric("🏛️ Governance Score", company_data["Gov_Score"].values[0])

        fraud_risk = company_data["Greenwashing_Risk"].values[0]

        #color and label
        risk_label = "🟢 Low Risk" if fraud_risk == 0 else "🔴 High Risk"
        risk_class = "low-risk" if fraud_risk == 0 else "high-risk"
        st.markdown(f'<div class="fraud-alert {risk_class}">{risk_label}</div>', unsafe_allow_html=True)
    else:
        st.error("⚠️ No data available for this company.")
else:
    st.info("🔍 Please select a company to view ESG details.")