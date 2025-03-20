import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import joblib
import numpy as np
import torch
from models.rl_agent import ESGAgent  
import logging



logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


SENTIMENT_MODEL_PATH = "models/sentiment_rf_model.pkl"
RL_MODEL_PATH = "models/trained_rl_model.pth"


try:
    sentiment_model = joblib.load(SENTIMENT_MODEL_PATH)
    logging.info("Sentiment model loaded successfully!")
except Exception as e:
    logging.error(f"Error loading sentiment model: {e}")
    sentiment_model = None

def predict_sentiment(features):
   
    try:
        features = np.array(features).reshape(1, -1)  
        return sentiment_model.predict(features)[0] if sentiment_model else None
    except Exception as e:
        logging.error(f"Error predicting sentiment: {e}")
        return None


STATE_DIM = 4
ACTION_DIM = 3

try:
    rl_agent = ESGAgent(STATE_DIM, ACTION_DIM)
    rl_agent.model.load_state_dict(torch.load(RL_MODEL_PATH, map_location=torch.device("cpu")))
    rl_agent.model.eval()
    logging.info("RL model loaded successfully!")
except Exception as e:
    logging.error(f"Error loading RL model: {e}")
    rl_agent = None

logging.info("All models initialized successfully!")
