from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import torch
import shap
import datetime
import logging
import os
import sys
import pickle
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer


root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from models.rl_agent import ESGAgent  

app = FastAPI()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


embedder = SentenceTransformer('all-MiniLM-L6-v2')

def get_text_embedding(text):    
    embedding = embedder.encode([text])[0] 
    twitter_esg_sentiment = np.mean(embedding)
    return twitter_esg_sentiment



try:
    sentiment_model = joblib.load("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /models/sentiment_rf_model.pkl")
    logging.info("Sentiment model loaded successfully!")
except Exception as e:
    logging.error(f"Error loading sentiment model: {e}")
    raise e


try:
    sample_embeddings = np.random.rand(100, 384)  
    pca = PCA(n_components=32)
    pca.fit(sample_embeddings)
    logging.info("PCA model trained successfully!")
except Exception as e:
    logging.error(f"Error training PCA model: {e}")
    raise e


rl_agent = ESGAgent(4, 3)
try:
    rl_agent.model.load_state_dict(torch.load("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /models/trained_rl_model.pth", map_location=torch.device("cpu")))
    logging.info("RL model loaded successfully!")
except Exception as e:
    logging.error(f"Error loading RL model: {e}")
    raise e


try:
    greenwashing_model = joblib.load("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /models/greenwashing_model.pkl")
    logging.info("Greenwashing model loaded successfully!")
except Exception as e:
    logging.error(f"Error loading greenwashing model: {e}")
    raise e



try:
    esg_model = joblib.load("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /models/esg_score_model.pkl")
    
    logging.info("ESG Score Prediction model loaded successfully!")
except Exception as e:
    logging.error(f"Error loading ESG model: {e}")
    raise e


explainer = shap.TreeExplainer(sentiment_model)


class SentimentInput(BaseModel):
    text: str  

class BulkSentimentInput(BaseModel):
    texts: list[str]

class RLInput(BaseModel):
    state: list[float]

class GreenwashingInput(BaseModel):
    Env_Score: float
    Gov_Score: float
    Soc_Score: float  


class ESGScoreInput(BaseModel):
    Env_Score: float
    Gov_Score: float
    Soc_Score: float


@app.post("/predict/sentiment")
def predict_sentiment(input_data: SentimentInput):
    try:
        text_vector = get_text_embedding(input_data.text).reshape(1, -1)
        #reduced_vector = pca.transform(text_vector)
        prediction = sentiment_model.predict(text_vector)[0]
        return {"sentiment_score": float(prediction)}
    except Exception as e:
        logging.error(f"Error in /predict/sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/rl")
def predict_rl_action(input_data: RLInput):
    try:
        state = np.array(input_data.state, dtype=np.float32)
        state_tensor = torch.tensor(state).unsqueeze(0)
        action_values = rl_agent.model(state_tensor).detach().numpy()[0]
        recommended_action = int(np.argmax(action_values))
        return {"recommended_action": recommended_action, "q_values": action_values.tolist()}
    except Exception as e:
        logging.error(f"Error in /predict/rl: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/greenwashing")
def predict_greenwashing(input_data: GreenwashingInput):
    try:

        min_values = np.array([200, 75, 160])
        max_values = np.array([719, 475, 667])
        esg_features = np.array([[input_data.Env_Score, input_data.Gov_Score, input_data.Soc_Score]])

        def scale_input(input_values):
            return (input_values / 100) * (max_values - min_values) + min_values
        
        scaled_values = scale_input(esg_features).reshape(1, -1)
        prediction = greenwashing_model.predict(scaled_values)

        return {"prediction": float(prediction)}

    except Exception as e:
        return {"error": str(e)}
    
@app.post("/predict/esg_score")
def predict_esg_score(input_data: ESGScoreInput):
    try:
        #combine
        esg_features = np.array([[input_data.Env_Score, input_data.Gov_Score, input_data.Soc_Score]])
    
        esg_score = esg_model.predict(esg_features)

        return {"esg_score": float(esg_score)}

    except Exception as e:
        logging.error(f"Error in /predict/esg_score: {e}")
        raise HTTPException(status_code=500, detail=str(e))

#metadata
@app.get("/metadata")
def get_metadata():
    return {
        "sentiment_model": {
            "name": "RandomForest ESG Sentiment Model",
            "version": "1.0",
            "last_updated": "2025-03-17"
        },
        "rl_model": {
            "name": "DQN ESG Investment Agent",
            "version": "1.0",
            "last_updated": "2025-03-17"
        },
        "greenwashing_model": {
            "name": "Greenwashing Detection Model",
            "version": "1.0",
            "last_updated": "2025-03-17"
        }
    }

#health check
@app.get("/health")
def health_check():
    return {"status": "API is running", "timestamp": str(datetime.datetime.now())}
