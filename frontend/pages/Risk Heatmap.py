import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import base64
from PIL import Image


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
                font-size: 40px;
                font-weight: bold;
                color: rgb(30, 73, 226);
                text-align: center;
                text-shadow: 2px 2px 10px rgba(255, 255, 255, 0.8);
            }
            .subheader-text {
                font-size: 26px;
                font-weight: bold;
                color: black;
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
                color: #E6E6E6;
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
                font-weight: bold;
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

# Load dataset
df = pd.read_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /corporate_financing_esg_dataset.csv")

# Hardcoded Latitude & Longitude for specific countries
country_coords = {
    "India": [20.5937, 78.9629],
    "USA": [37.0902, -95.7129],
    "UK": [55.3781, -3.4360],
    "Germany": [51.1657, 10.4515],
    "China": [35.8617, 104.1954],
    "Japan": [36.2048, 138.2529],
    "Brazil": [-14.2350, -51.9253],
    "South Africa": [-30.5595, 22.9375],
    "Australia": [-25.2744, 133.7751],
    "Canada": [56.1304, -106.3468],
    "France": [46.2276, 2.2137],
    "Italy": [41.8719, 12.5674],
}

# Filter dataset to include only these countries
df_filtered = df[df["Country"].isin(country_coords.keys())]

# Aggregate ESG scores by country
country_esg = df_filtered.groupby("Country")["ESG_Score_Post"].mean().reset_index()

# Function to classify risk levels
def classify_risk(score):
    if score >= 75:
        return "Low Risk"
    elif score >= 70:
        return "Medium Risk"
    else:
        return "High Risk"

country_esg["Risk_Level"] = country_esg["ESG_Score_Post"].apply(classify_risk)

# Function to assign colors based on ESG Risk Level
def get_color(risk):
    return {"Low Risk": "green", "Medium Risk": "orange", "High Risk": "red"}[risk]

# Streamlit UI
st.title("🌍 ESG Risk Heatmap")
st.write("Interactive map displaying ESG compliance risk across countries.")

# Feature: Filter for Risk Level
risk_filter = st.selectbox("Select Risk Level to Display:", ["All", "Low Risk", "Medium Risk", "High Risk"])
if risk_filter != "All":
    country_esg = country_esg[country_esg["Risk_Level"] == risk_filter]

# Create Folium Map
m = folium.Map(location=[20, 0], zoom_start=2)

# Add markers for each country with Tooltip on Hover
for _, row in country_esg.iterrows():
    country = row["Country"]
    lat, lon = country_coords[country]  # Use hardcoded lat/lon
    
    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        color=get_color(row["Risk_Level"]),
        fill=True,
        fill_color=get_color(row["Risk_Level"]),
        fill_opacity=0.7,
        popup=f"<b>{country}</b><br>Risk Level: <b>{row['Risk_Level']}</b><br>ESG Score: <b>{row['ESG_Score_Post']:.2f}</b>",
        tooltip=folium.Tooltip(f"{country} - {row['Risk_Level']} ({row['ESG_Score_Post']:.2f})")  # 🔥 Added Hover Tooltip!
    ).add_to(m)

# Display Folium map in Streamlit
folium_static(m)

# Feature: Show ESG Score Summary Table
st.write("### ESG Score Summary Table")
st.dataframe(country_esg)

