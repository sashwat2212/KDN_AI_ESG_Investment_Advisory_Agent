import shap
import torch
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

from rl_agent import ESGAgent
from rl_env import ESGTradingEnv 


results_folder = "results"
os.makedirs(results_folder, exist_ok=True)


state_dim = 4
action_dim = 3
agent = ESGAgent(state_dim, action_dim)
model = agent.model
model.eval()


feature_names = ["Carbon Emissions", "Water Usage", "Renewable Energy", "Governance Score"]


def get_state(method="default"):
    if method == "default":
        return torch.FloatTensor([[299.20, -0.000024116, 22.425, 1.0]])
    elif method == "random":
        return torch.FloatTensor(np.random.randn(1, state_dim))
    elif method == "csv":
        df = pd.read_csv("esg_data.csv")
        random_state = df.sample(n=1).values
        return torch.FloatTensor(random_state)
    elif method == "env":
        env = ESGTradingEnv()
        state = env.reset()
        return torch.FloatTensor(state).unsqueeze(0)
    else:
        raise ValueError("Invalid state generation method")


generation_method = "default" 
state_tensor = get_state(generation_method)


baseline_states = torch.zeros_like(state_tensor).repeat(10, 1)  


explainer = shap.GradientExplainer(model, baseline_states)
shap_values = explainer.shap_values(state_tensor)


shap_values_np = np.array(shap_values) 


expected_value = model(baseline_states).mean(0).detach().numpy()


action_index = 0  
shap_values_single_action = shap_values_np[0, :, action_index]  
expected_value_single_action = expected_value[action_index]


def save_shap_plot(fig, filename):
    
    filepath = os.path.join(results_folder, filename)
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close(fig)


fig = plt.figure()
shap.waterfall_plot(
    shap.Explanation(
        values=shap_values_single_action, 
        base_values=expected_value_single_action, 
        data=state_tensor.detach().numpy().flatten(), 
        feature_names=feature_names
    )
)
save_shap_plot(fig, "shap_waterfall.png")


fig = plt.figure()
shap.summary_plot(
    shap_values_np[:, :, action_index], 
    state_tensor.numpy(), 
    feature_names=feature_names, 
    show=False  #prevents immediate display
)
save_shap_plot(fig, "shap_summary.png")



fig = plt.figure()
shap.decision_plot(
    expected_value_single_action,
    shap_values_single_action,
    feature_names=feature_names,
    show=False
)
save_shap_plot(fig, "shap_decision.png")


fig = plt.figure()
shap.bar_plot(shap_values_single_action, feature_names=feature_names, show=False)
save_shap_plot(fig, "shap_bar.png")

print(f"SHAP plots saved in '{results_folder}'")
