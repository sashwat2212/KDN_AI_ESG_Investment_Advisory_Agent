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
st.markdown(
    """
    <style>
        .esg-header {
            font-size: 32px;
            font-weight: bold;
            color: #00A86B;
            text-align: center;
        }
        .fraud-alert {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            border-radius: 10px;
        }
        .low-risk {
            background: linear-gradient(135deg, #007BFF 30%, #00A86B 100%);
            padding: 15px;
            border-radius: 10px;
            color: green;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
        .high-risk {
            background: linear-gradient(135deg, #007BFF 30%, #00A86B 100%);
            padding: 15px;
            border-radius: 10px;
            color: #721C24;
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

st.markdown('<div class="esg-header">🔍 ESG Detective Mode - Fraud Likelihood Meter</div>', unsafe_allow_html=True)

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