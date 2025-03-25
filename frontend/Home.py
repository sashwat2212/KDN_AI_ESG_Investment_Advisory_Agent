import streamlit as st
import requests
import numpy as np
from PIL import Image
import base64

API_URL = "http://127.0.0.1:8000"


st.set_page_config(page_title="ESG Investment Dashboard", layout="wide")

st.markdown(
    """
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        [data-testid="stSidebar"] {
            background: #aceaff;
            padding: 25px;
            border-right: 4px solid rgb(0, 192, 174);
            color: #000000 !important;
        }
        [data-testid="stSidebarContent"] {
            background: #aceaff;
            color: #000000 !important;
            font-size: 16px;
        }
        .stButton > button {
            border-radius: 10px;
            background: rgb(118, 210, 255);

            color: black;
            font-weight: bold;
            padding: 10px 20px;
            transition: 0.3s;
            border: none;
        }
        .stButton > button:hover {
            background: rgb(118, 210, 255)
            transform: scale(1.05);
        }
        .stTextArea textarea {
            background: #aceaff;
            color: black !important;
            border-radius: 8px;
        }
        .metric-card {
            background: #aceaff;
            padding: 20px;
            border-radius: 12px;
            color: black;
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
        .sidebar-logo-container {{
            background: white; 
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 10px;
            margin-bottom: 20px; /* Space between logo and sidebar content */
        }}
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


st.sidebar.header("📜 User Input")
company_text = st.sidebar.text_area(
    "",
    "Tesla commits to sustainable energy."
)


sentiment_score = "N/A"
recommended_action = "N/A"
greenwashing_alert = "N/A"
greenwashing_score = "N/A"
q_values = "N/A"
Total_Score = "N/A"
esg_score = "N/A"
market_state = np.random.rand(4).tolist() 


if st.sidebar.button("🔍 Analyze ESG Score & Recommend Investment"):
    with st.spinner("Fetching results..."):
        try:
            sentiment_response = requests.post(f"{API_URL}/predict/sentiment", json={"text": company_text})
            sentiment_score = sentiment_response.json().get("sentiment_score", "Error")

            rl_response = requests.post(f"{API_URL}/predict/rl", json={"state": market_state})
            recommended_action = rl_response.json().get("recommended_action", "Error")
            q_values = rl_response.json().get("q_values", "Error")

        except Exception as e:
            st.sidebar.error(f"API Request Failed: {e}")

    st.sidebar.success("Results Updated")


st.title("ESG Investment Dashboard")


st.markdown(
    """
    <style>
        .metric-card {
            background: #aceaff;
            padding: 15px;
            border-radius: 12px;
            color: black;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True
)


sentiment_score = round(sentiment_score, 5) if isinstance(sentiment_score, (int, float)) else sentiment_score
st.markdown(f'<div class="metric-card">🌍 ESG Sentiment Score: {sentiment_score}</div>', unsafe_allow_html=True)

st.markdown("---")


st.subheader("AI-Powered ESG Investment Recommendation")

ACTION_MAP = {0: "Buy", 1: "Hold", 2: "Sell"}
recommended_action_text = ACTION_MAP.get(recommended_action, "Unknown")

if recommended_action == "Error":
    st.error("❌ Could not fetch investment recommendation.")
else:
    st.success(f"**Recommended Investment Action:** {recommended_action_text}")
    st.info(f"💡 **Q-Values:** {q_values}")

st.markdown("---")


st.subheader("💰 ESG Portfolio Simulator")
st.markdown(
    """
    <style>
        .portfolio-card {
            background: #aceaff;
            padding: 15px;
            border-radius: 12px;
            color: black;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True
)


investment_amount = st.number_input("Enter Investment Amount ($):", min_value=100, step=100)

if q_values and isinstance(q_values, list) and all(isinstance(q, (int, float, str)) for q in q_values):
    try:
        q_buy, q_hold, q_sell = map(float, q_values)

        if q_buy == max(q_buy, q_hold, q_sell):
            q_buy = -1 * q_buy
            projected_growth = investment_amount * ((q_buy-1)/10)
        projected_growth = investment_amount * (1 + max(q_buy, q_hold, q_sell) / 10)
        
        st.markdown(f'<div class="portfolio-card">📈 Projected Portfolio Value (1 Year): ${round(projected_growth, 2)}</div>', unsafe_allow_html=True)
        
        st.write(f"🟢 **Buy:** {q_buy}, 🟡 **Hold:** {q_hold}, 🔴 **Sell:** {q_sell}")

    except ValueError:
        st.error("⚠️ Invalid Q-values detected! Please run the analysis first.")
else:
    st.warning("⚠️ Q-values are missing! Click 'Analyze' first.")

st.markdown("---")


st.subheader("🔢 ESG Score Inputs")

col1, col2, col3 = st.columns(3)
with col1:
    env_score = st.slider("🌱 Environmental Score", 0.0, 100.0, 50.0, step=1.0)
with col2:
    gov_score = st.slider("🏛️ Governance Score", 0.0, 100.0, 50.0, step=1.0)
with col3:
    soc_score = st.slider("🤝 Social Score", 0.0, 100.0, 50.0, step=1.0)

if st.button("🚦 Analyze Greenwashing"):
    with st.spinner("Analyzing Greenwashing..."):
        try:
            greenwashing_response = requests.post(f"{API_URL}/predict/greenwashing", json={
                "Env_Score": env_score, "Gov_Score": gov_score, "Soc_Score": soc_score
            })
            greenwashing_alert = greenwashing_response.json().get("prediction", "Error")

            esg_response = requests.post(f"{API_URL}/predict/esg_score", json={
                "Env_Score": env_score, "Gov_Score": gov_score, "Soc_Score": soc_score
            })
            esg_score = esg_response.json().get("esg_score", "Error")

        except Exception as e:
            st.error(f"API Request Failed: {e}")

st.markdown("---")


st.subheader("Greenwashing Alert System")

if greenwashing_alert == 1:
    st.error("🔴 **Greenwashing Found!**")
elif greenwashing_alert == 0:
    st.success("✅ **No Greenwashing Detected.**")
else:
    st.warning("⚠️ **Greenwashing Detection Unavailable.**")

st.markdown("---")

# 🔮 **ESG Score Prediction**
st.subheader("ESG Score Prediction Model")

if esg_score != "N/A":
    st.metric("📊 Predicted ESG Score", esg_score)
else:
    st.warning("⚠️ ESG Score not available. Run analysis first.")

st.markdown("---")


st.sidebar.subheader("⚙️ API Status")
try:
    health_response = requests.get(f"{API_URL}/health").json()
    st.sidebar.write(f"🟢 {health_response['status']} at {health_response['timestamp']}")
except Exception:
    st.sidebar.error("🔴 API Unreachable")
