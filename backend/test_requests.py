import os
import requests


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

def make_request(endpoint, payload=None, method="POST"):

    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=payload)
        else:
            response = requests.get(url)
        
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


sentiment_payload = {"text": "Renewable energy is the best investment"}
print("Sentiment Prediction:", make_request("/predict/sentiment", sentiment_payload))


bulk_payload = {"texts": ["Green bonds are gaining traction", "Oil stocks are volatile"]}
print("Bulk Sentiment Predictions:", make_request("/predict/sentiment_bulk", bulk_payload))


explain_payload = {"text": "Companies investing in sustainability perform better"}
print("Feature Importance:", make_request("/explain/sentiment", explain_payload))


rl_payload = {"state": [0.1] * 4} 
print("RL Model Prediction:", make_request("/predict/rl", rl_payload))


print("Health Check:", make_request("/health", method="GET"))


print("Model Metadata:", make_request("/metadata", method="GET"))
