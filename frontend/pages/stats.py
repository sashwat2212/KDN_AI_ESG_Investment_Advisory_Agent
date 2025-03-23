import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np
import datetime
import base64
from PIL import Image



st.set_page_config(page_title="ESG Statistics", page_icon="📊", layout="wide")
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /frontend/logo.png")


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

st.title("📊 ESG Statistics")



@st.cache_data
def load_data():
    try:

        data = pd.read_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /data_preprocessing/final_processed_esg_data.csv")  


        required_columns = ["Company", "Weighted_ESG_Score", "Env_Score", "Soc_Score", "Gov_Score"]
        data = data[required_columns]
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"Missing column: {col}")


        data["Average ESG Component"] = data[["Env_Score", "Soc_Score", "Gov_Score"]].mean(axis=1)
        data["Greenwashing Risk"] = abs(data["Weighted_ESG_Score"] - data["Average ESG Component"])


        data["Greenwashing Flag"] = data["Greenwashing Risk"] > 5
        
        return data

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  


df = load_data()


st.subheader("📌 ESG Data Overview")

if df.empty:
    st.warning("⚠️ No data available. Please check your dataset file.")
else:
    st.dataframe(df)


st.markdown("---")  

st.subheader("🚨 Greenwashing Risk Analysis")
st.write(
    "Companies with a high discrepancy between self-reported ESG Score and actual ESG component performance "
    "may be engaging in greenwashing. A higher Greenwashing Risk Score indicates a greater likelihood of misleading claims."
)

#top 20 companies
top_n = 20
df_sorted = df.sort_values("Greenwashing Risk", ascending=False).head(top_n)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=df_sorted["Company"], y=df_sorted["Greenwashing Risk"], palette="Reds_r", ax=ax)
plt.xticks(rotation=45, ha="right")
plt.xlabel("Company")
plt.ylabel("Greenwashing Risk Score")
plt.title(f"Top {top_n} Companies with Highest Greenwashing Risk")
st.pyplot(fig)

st.markdown("---")  

#companies with high greenwashing risk
high_risk_companies = df[df["Greenwashing Flag"]][["Company", "Greenwashing Risk"]]

if not high_risk_companies.empty:
    st.error(f"🚨 {len(high_risk_companies)} Companies Detected with High Greenwashing Risk!")
    
    #filteration
    risk_threshold = st.slider(
        "Select Greenwashing Risk Score Threshold",
        min_value=int(df["Greenwashing Risk"].min()),
        max_value=int(df["Greenwashing Risk"].max()),
        value=30,  #threshold
    )
    
    filtered_high_risk = high_risk_companies[high_risk_companies["Greenwashing Risk"] >= risk_threshold]
    
    if not filtered_high_risk.empty:
        st.dataframe(filtered_high_risk)
    else:
        st.success("✅ No Companies Above Selected Risk Threshold.")
else:
    st.success("✅ No Companies Detected with High Greenwashing Risk.")


st.success("✅ ESG Statistics & Greenwashing Analysis Loaded Successfully!")

st.markdown("---") 

stocks_data = pd.read_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /data_preprocessing/final_processed_esg_data.csv")


required_columns = ["Company", "ESG_Impact_Score"]
if not all(col in stocks_data.columns for col in required_columns):
    st.error("⚠️ Missing required columns in dataset. Please check the file format.")
else:

    stocks_data = stocks_data[required_columns]
    threshold = stocks_data["ESG_Impact_Score"].mean()


    styled_df = stocks_data.style.map(
        lambda x: "background-color: lightgreen" if x > threshold else "", subset=["ESG_Impact_Score"]
    )


    st.subheader("📈 Live ESG Stock Market Data")
    st.dataframe(styled_df)


st.markdown("---")  


df_news = pd.read_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /data_preprocessing/news_sentiment_forecasting.csv")

required_columns = ["Headline", "sentiment"]
if not all(col in df_news.columns for col in required_columns):
    st.error("⚠️ Missing required columns in dataset. Please check the file format.")
else:

    df_news = df_news[required_columns]
    def highlight_sentiment(val):
        if val.lower() == "negative":
            return "background-color: red; color: white"
        elif val.lower() == "neutral":
            return "background-color: yellow; color: black"
        elif val.lower() == "positive":
            return "background-color: lightgreen; color: black"
        return ""


    styled_df = df_news.style.map(highlight_sentiment, subset=["sentiment"])


    st.subheader("⚠️ ESG Controversy Detection")
    st.dataframe(styled_df)


    negative_news = df_news[df_news["sentiment"].str.lower() == "negative"]
    if not negative_news.empty:
        st.warning("🚨 Some companies have negative ESG-related news! Review them carefully.")

st.markdown("---")  



df_investment = pd.read_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /data_preprocessing/final_processed_esg_data.csv")


required_columns = ["Company", "Weighted_ESG_Score", "Exchange", "industry", "Greenwashing_Risk"]
if not all(col in df_investment.columns for col in required_columns):
    st.error("⚠️ Missing required columns in dataset. Please check the file format.")
else:

    st.subheader("🏆 ESG Investment Leaderboard")
    df_investment = df_investment[required_columns]

    leaderboard = df_investment.sort_values(by="Weighted_ESG_Score", ascending=False)
    

    st.dataframe(leaderboard)

st.markdown("---") 



numeric_df = df.drop(columns=["Company", "Greenwashing Flag"])


col1, col2 = st.columns(2)


with col1:
    st.subheader("📊 ESG Score Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(numeric_df["Weighted_ESG_Score"], bins=10, kde=True, ax=ax)
    plt.xlabel("Weighted_ESG_Score")
    st.pyplot(fig)


with col2:
    st.subheader("📊 ESG Component Correlations")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)


st.markdown("---")  


st.subheader("📊 ESG Score Comparison")


mode = st.selectbox(
    "How do you want to filter companies?",
    ["Top Companies", "Select Companies", "Random Sample"]
)

if mode == "Top Companies":
    num_top = st.slider("Select Number of Top Companies:", min_value=5, max_value=50, value=20)
    top_companies = df.nlargest(num_top, "Weighted_ESG_Score")  #get top N companies

    fig, ax = plt.subplots(figsize=(12, 6))
    top_companies.set_index("Company")[["Env_Score", "Soc_Score", "Gov_Score"]].plot(
        kind="bar", stacked=True, ax=ax
    )
    plt.xticks(rotation=45)
    plt.xlabel("Company")
    plt.ylabel("Weighted ESG Score")
    plt.title(f"Top {num_top} Companies: ESG Component Breakdown")
    st.pyplot(fig)

elif mode == "Select Companies":
    selected_companies = st.multiselect(
        "Select Companies to Compare", df["Company"].unique(), default=df["Company"].unique()[:5]
    )

    if selected_companies:
        filtered_df = df[df["Company"].isin(selected_companies)]

        fig, ax = plt.subplots(figsize=(12, 6))
        filtered_df.set_index("Company")[["Env_Score", "Soc_Score", "Gov_Score"]].plot(
            kind="bar", stacked=True, ax=ax
        )
        plt.xticks(rotation=45)
        plt.xlabel("Company")
        plt.ylabel("Weighted ESG Score")
        plt.title("Selected Companies: ESG Component Breakdown")
        st.pyplot(fig)
    else:
        st.warning("⚠️ Please select at least one company to display the chart.")

elif mode == "Random Sample":
    num_sample = st.slider("Select Number of Random Companies:", min_value=5, max_value=50, value=30)
    sampled_df = df.sample(num_sample, random_state=42)

    fig, ax = plt.subplots(figsize=(12, 6))
    sampled_df.set_index("Company")[["Env_Score", "Soc_Score", "Gov_Score"]].plot(
        kind="bar", stacked=True, ax=ax
    )
    plt.xticks(rotation=45)
    plt.xlabel("Company")
    plt.ylabel("Weighted ESG Score")
    plt.title(f"Random Sample of {num_sample} Companies: ESG Component Breakdown")
    st.pyplot(fig)



st.markdown("---")  


#by industry
st.subheader("🏢 Industry-wise ESG Performance Comparison")
df = pd.read_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /data_preprocessing/final_processed_esg_data.csv")  


if "industry" in df.columns and "Industry_Avg_Score" in df.columns:

    industry_performance = df.groupby("industry")["Industry_Avg_Score"].agg(["mean", "std"]).reset_index()
    industry_performance.columns = ["industry", "Avg ESG Score", "Volatility"]


    industry_performance["Volatility"].fillna(0, inplace=True)


    fig_industry = px.bar(
        industry_performance,
        x="industry",
        y="Avg ESG Score",
        color="Volatility",
        title="Average ESG Scores by Industry",
        labels={"Volatility": "Market Volatility"},
        text="Avg ESG Score",
        color_continuous_scale="viridis",
    )

    st.plotly_chart(fig_industry)
else:
    st.error("⚠️ Missing 'Industry' or 'Industry_Avg_Score' columns in the dataset.")


st.markdown("---")  

