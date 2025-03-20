import pandas as pd


df = pd.read_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor/esg_data/data.csv")

df.info(), df.head()

#dropping irrelevant columns
df_cleaned = df.drop(columns=["logo", "weburl", "cik", "last_processing_date"])

#rename columns
df_cleaned.columns = [
    "Ticker", "Company", "Currency", "Exchange", "Industry", 
    "Env_Grade", "Env_Level", "Soc_Grade", "Soc_Level", "Gov_Grade", "Gov_Level",
    "Env_Score", "Soc_Score", "Gov_Score", "Total_Score", "Total_Grade", "Total_Level"
]

#handle missing values
df_cleaned["Industry"] = df_cleaned["Industry"].fillna("Unknown")


#convert scores
df_cleaned[["Env_Score", "Soc_Score", "Gov_Score", "Total_Score"]] = df_cleaned[["Env_Score", "Soc_Score", "Gov_Score", "Total_Score"]].astype(float)


df_cleaned.head()


df_cleaned.to_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor/esg_data/cleaned_esg_data.csv", index=False)



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


visualization_dir = "visualizations"
os.makedirs(visualization_dir, exist_ok=True)


df_cleaned = pd.read_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /esg_data/cleaned_esg_data.csv")


sns.set(style="whitegrid")

#distribution
plt.figure(figsize=(12, 5))
sns.histplot(df_cleaned["Total_Score"], bins=30, kde=True, color="blue")
plt.title("Distribution of Total ESG Scores", fontsize=14)
plt.xlabel("Total ESG Score")
plt.ylabel("Frequency")
plt.savefig(f"{visualization_dir}/esg_score_distribution.png")  
plt.close()

#by Industry 
plt.figure(figsize=(14, 6))
top_industries = df_cleaned["Industry"].value_counts().head(10).index
df_subset = df_cleaned[df_cleaned["Industry"].isin(top_industries)]

sns.boxplot(x="Industry", y="Total_Score", data=df_subset, palette="coolwarm")
plt.xticks(rotation=45)
plt.title("Total ESG Score Distribution by Industry")
plt.savefig(f"{visualization_dir}/esg_scores_by_industry.png") 
plt.close()

#correlation heatmap
plt.figure(figsize=(8, 6))
correlation_matrix = df_cleaned[["Env_Score", "Soc_Score", "Gov_Score", "Total_Score"]].corr()
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Between ESG Factors")
plt.savefig(f"{visualization_dir}/esg_correlation_heatmap.png") 
plt.close()


#top 10 companies
top_10 = df_cleaned.nlargest(10, "Total_Score")[["Company", "Total_Score"]]
bottom_10 = df_cleaned.nsmallest(10, "Total_Score")[["Company", "Total_Score"]]

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.barplot(y=top_10["Company"], x=top_10["Total_Score"], palette="Greens", ax=axes[0])
axes[0].set_title("Top 10 Companies by ESG Score")
axes[0].set_xlabel("Total ESG Score")

sns.barplot(y=bottom_10["Company"], x=bottom_10["Total_Score"], palette="Reds", ax=axes[1])
axes[1].set_title("Bottom 10 Companies by ESG Score")
axes[1].set_xlabel("Total ESG Score")

plt.tight_layout()
plt.savefig(f"{visualization_dir}/top_bottom_esg_companies.png")  
plt.close()

print("EDA visualizations saved in 'visualizations/' directory.")


import pandas as pd
from sklearn.preprocessing import MinMaxScaler


df_cleaned = pd.read_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /esg_data/cleaned_esg_data.csv")


df_cleaned["ESG_Impact_Score"] = (df_cleaned["Env_Score"] + df_cleaned["Soc_Score"] + df_cleaned["Gov_Score"]) / 3


df_cleaned["ESG_Risk_Level"] = pd.qcut(df_cleaned["Total_Score"], q=3, labels=["High Risk", "Medium Risk", "Low Risk"])


scaler = MinMaxScaler()
df_cleaned[["Env_Score_Norm", "Soc_Score_Norm", "Gov_Score_Norm", "Total_Score_Norm"]] = scaler.fit_transform(
    df_cleaned[["Env_Score", "Soc_Score", "Gov_Score", "Total_Score"]]
)


industry_avg_esg = df_cleaned.groupby("Industry")["Total_Score"].mean().to_dict()
df_cleaned["Industry_Avg_Score"] = df_cleaned["Industry"].map(industry_avg_esg)


df_cleaned["ESG_Score_Deviation"] = df_cleaned["Total_Score"] - df_cleaned["Industry_Avg_Score"]


df_cleaned.to_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /esg_data/feature_engineered_esg_data.csv", index=False)

print("Feature engineering complete! Data saved as 'feature_engineered_esg_data.csv'")

print(df_cleaned.describe())
print(df_cleaned.groupby("ESG_Risk_Level")["Total_Score"].mean())
