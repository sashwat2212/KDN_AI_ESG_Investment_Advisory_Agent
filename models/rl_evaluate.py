from rl_env import ESGTradingEnv
from rl_agent import ESGAgent
import torch

print("Initializing Environment")
env = ESGTradingEnv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /data_preprocessing/final_processed_esg_data.csv")

print("Initializing Agent")
agent = ESGAgent(state_dim=4, action_dim=3)

print("Loading Model")
try:
    agent.model.load_state_dict(torch.load("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /models/trained_rl_model.pth", weights_only=False))
    print(f"Model loaded. Weights: {agent.model.state_dict().keys()}")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Model loading failed: {e}")

state = env.reset()
done = False

print("Starting Evaluation")
while not done:
    print(f"State: {state}") 
    action = agent.get_action(state)
    print(f"→ Chosen Action: {action}")
    
    state, reward, done, _ = env.step(action)
    print(f"→ New State: {state}, Reward: {reward}")

print("Evaluation Complete!")
