import openai
import pandas as pd
import time
import json
from dotenv import load_dotenv
import os
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key



def gpt_extract_companies(text):
    if not isinstance(text, str) or text.strip() == "":
        return []  

    prompt = (
        "Extract all company names from the following text. "
        "ONLY return a JSON list (e.g., [\"Apple\", \"Microsoft\"]). No extra text.\n\n"
        f"Text:\n{text}"
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        extracted_companies = response.choices[0].message.content.strip()

        
        if extracted_companies.startswith("[") and extracted_companies.endswith("]"):
            return json.loads(extracted_companies)
        else:
            print("⚠️ GPT Response Formatting Error:", extracted_companies)
            return [] 

    except json.JSONDecodeError:
        print("JSON Parsing Error: Could not decode response.")
        return []
    except Exception as e:
        print("Error:", e)
        return []



df_news = pd.read_csv("esg_news_sentiment.csv")  


df_twitter = pd.read_csv("twitter_esg_data_with_sentiment.csv") 


print("Extracting company names from news articles... This may take time.")
df_news["extracted_companies"] = df_news["Headline"].apply(gpt_extract_companies)


print("Extracting company names from tweets... This may take time.")
df_twitter["extracted_companies"] = df_twitter["text"].apply(gpt_extract_companies)


df_news.to_csv("esg_news_with_companies.csv", index=False)
df_twitter.to_csv("twitter_esg_with_companies.csv", index=False)

print("Company name extraction complete! Files saved as:")
print("esg_news_with_companies.csv")
print("twitter_esg_with_companies.csv")


# --------------------------------------------------------------------------------------


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df_esg = pd.read_csv("feature_engineered_esg_data.csv") 
df_twitter = pd.read_csv("twitter_esg_with_companies.csv") 
df_news = pd.read_csv("esg_news_with_companies.csv")  


industries = df_esg["Industry"].unique().tolist()


vectorizer = TfidfVectorizer()
industry_vectors = vectorizer.fit_transform(industries)

def assign_industry(text):
    if pd.isna(text) or text.strip() == "":
        return None
    text_vector = vectorizer.transform([text])
    similarity_scores = cosine_similarity(text_vector, industry_vectors)
    best_match = industries[similarity_scores.argmax()]
    return best_match


df_twitter["industry"] = df_twitter["text"].apply(assign_industry)
df_news["industry"] = df_news["Headline"].apply(assign_industry)

#aggregate industry
df_twitter_industry = df_twitter.groupby("industry")["sentiment_score"].mean().reset_index()
df_news_industry = df_news.groupby("industry")["Sentiment Score"].mean().reset_index()


df_twitter_industry.rename(columns={"sentiment_score": "twitter_esg_sentiment"}, inplace=True)
df_news_industry.rename(columns={"sentiment_score": "news_esg_sentiment"}, inplace=True)


df_twitter_industry.to_csv("industry_twitter_esg.csv", index=False)
df_news_industry.to_csv("industry_news_esg.csv", index=False)


# --------------------------------------------------------------------------------------


from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


vectorizer = CountVectorizer(stop_words='english')
news_vectors = vectorizer.fit_transform(df_news["Headline"])

lda_model = LatentDirichletAllocation(n_components=5, random_state=42)
lda_topics = lda_model.fit_transform(news_vectors)

#sssign dominant topic to each article
df_news["dominant_topic"] = lda_topics.argmax(axis=1)
df_news["lda_score"] = lda_topics.max(axis=1)

#aggregate sentiment by topic
df_topic_scores = df_news.groupby("dominant_topic")["lda_score"].mean().reset_index()
df_topic_scores.rename(columns={"lda_score": "topic_esg_impact"}, inplace=True)

#save ESG impact scores
df_topic_scores.to_csv("topic_esg_impact.csv", index=False)


# --------------------------------------------------------------------------------------


from geopy.geocoders import Nominatim
import geopandas as gpd


df_satellite = pd.read_csv("Satellite_Complete_Data.csv")  


df_satellite["Date"] = pd.to_datetime(df_satellite["Date"])


df_satellite_avg = df_satellite

#rename columns
df_satellite_avg.rename(columns={
    "Deforestation (Percent_Tree_Cover)": "avg_deforestation",
    "Air Pollution (NO2) (tropospheric_NO2_column_number_density)": "avg_air_pollution",
    "Water Quality (SR_B3)": "avg_water_quality_B3",
    "Water Quality (SR_B4)": "avg_water_quality_B4",
    "Water Quality (SR_B5)": "avg_water_quality_B5"
}, inplace=True)

#save
df_satellite_avg.to_csv("satellite_aggregated.csv", index=False)



# --------------------------------------------------------------------------------------


import pandas as pd


df_satellite_avg = pd.read_csv("satellite_environmental_scores.csv")

#columns to normalize
columns_to_normalize = [
    "avg_deforestation", "avg_air_pollution", 
    "avg_water_quality_B3", "avg_water_quality_B4", "avg_water_quality_B5"
]

#convert columns to numeric
df_satellite_avg[columns_to_normalize] = df_satellite_avg[columns_to_normalize].apply(pd.to_numeric, errors="coerce")

#min-max normalization
for col in columns_to_normalize:
    min_val = df_satellite_avg[col].min()
    max_val = df_satellite_avg[col].max()
    df_satellite_avg[col + "_normalized"] = (df_satellite_avg[col] - min_val) / (max_val - min_val)

#compute environmental deviation score 
df_satellite_avg["Env_Score_Norm"] = df_satellite_avg[[col + "_normalized" for col in columns_to_normalize]].mean(axis=1)

#save
df_satellite_avg.to_csv("satellite_normalized_scores.csv", index=False)

print("Normalization complete! The new dataset is saved as 'satellite_normalized_scores.csv'.")




df_base = pd.read_csv("feature_engineered_esg_data.csv")
df_twitter_industry = pd.read_csv("industry_twitter_esg.csv")
df_news_industry = pd.read_csv("industry_news_esg.csv")
df_topic_scores = pd.read_csv("topic_esg_impact.csv")
df_satellite = pd.read_csv("satellite_normalized_scores.csv")

df_base.rename(columns={"Industry": "industry"}, inplace=True)

#merge Twitter & News
df_merged = df_base.merge(df_twitter_industry, on="industry", how="left")
df_merged = df_merged.merge(df_news_industry, on="industry", how="left")

df_merged["industry"] = df_merged["industry"].astype(str)
df_topic_scores["dominant_topic"] = df_topic_scores["dominant_topic"].astype(str)


#merge topic ESG Impact(News-based)
df_merged = df_merged.merge(df_topic_scores, left_on="industry", right_on="dominant_topic", how="left")

print("df_merged columns:", df_merged.columns)
print("df_satellite columns:", df_satellite.columns)


#merge Satellite(environmental deviation score)
df_merged = df_merged.merge(df_satellite, on="Env_Score_Norm", how="left")


df_merged.to_csv("final_esg_dataset.csv", index=False)
print("ESG dataset successfully merged and saved!")


