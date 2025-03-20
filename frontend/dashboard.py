import streamlit as st
import requests
import numpy as np


API_URL = "http://127.0.0.1:8000"


st.set_page_config(page_title="ESG Investment Dashboard", layout="wide")

st.markdown(
    """
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #002855, #004d99);
            padding: 25px;
            border-right: 4px solid #00A86B;
            color: #FFFFFF !important;
        }
        [data-testid="stSidebarContent"] {
            background: linear-gradient(180deg, #002855, #004d99);
            color: #FFFFFF !important;
            font-size: 16px;
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
            background: black;
            color: white !important;
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

st.sidebar.title("🌍 ESG Navigation")
st.sidebar.page_link("dashboard.py", label="📢 ESG Predictions & Portfolio")
st.sidebar.page_link("pages/stats.py", label="📈 ESG Statistics & Visualizations")
st.sidebar.page_link("pages/images.py", label="🖼️ ESG Image Gallery")
st.sidebar.page_link("pages/detective.py", label="🔍 ESG Detective Model")


st.sidebar.header("📜 User Input")
company_text = st.sidebar.text_area(
    "Enter Company News for ESG Sentiment Analysis",
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

    st.sidebar.success("✅ Results Updated")


st.title("📊 ESG Investment Dashboard")


st.markdown(
    """
    <style>
        .metric-card {
            background: linear-gradient(135deg, #007BFF 30%, #00A86B 100%);
            padding: 15px;
            border-radius: 10px;
            color: white;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

sentiment_score = round(sentiment_score, 5) if isinstance(sentiment_score, (int, float)) else sentiment_score
st.markdown(f'<div class="metric-card">🌍 ESG Sentiment Score: {sentiment_score}</div>', unsafe_allow_html=True)

st.markdown("---")


st.subheader("🏦 AI-Powered ESG Investment Recommendation")

ACTION_MAP = {0: "Buy", 1: "Hold", 2: "Sell"}
recommended_action_text = ACTION_MAP.get(recommended_action, "Unknown")

if recommended_action == "Error":
    st.error("❌ Could not fetch investment recommendation.")
else:
    st.success(f"✅ **Recommended Investment Action:** {recommended_action_text}")
    st.info(f"💡 **Q-Values:** {q_values}")

st.markdown("---")


st.subheader("💰 ESG Portfolio Simulator")
st.markdown(
    """
    <style>
        .portfolio-card {
            background: linear-gradient(135deg, #007BFF 30%, #00A86B 100%);
            padding: 15px;
            border-radius: 10px;
            color: white;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

investment_amount = st.number_input("💵 Enter Investment Amount ($):", min_value=100, step=100)

if q_values and isinstance(q_values, list) and all(isinstance(q, (int, float, str)) for q in q_values):
    try:
        q_buy, q_hold, q_sell = map(float, q_values)
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


st.subheader("🚨 Greenwashing Alert System")

if greenwashing_alert == 1:
    st.error("🔴 **Greenwashing Found!** ⚠️")
elif greenwashing_alert == 0:
    st.success("✅ **No Greenwashing Detected.**")
else:
    st.warning("⚠️ **Greenwashing Detection Unavailable.**")

st.markdown("---")


st.subheader("🔮 ESG Score Prediction Model")
esg_score = round(esg_score, 5) if isinstance(esg_score, (int, float)) else esg_score
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
