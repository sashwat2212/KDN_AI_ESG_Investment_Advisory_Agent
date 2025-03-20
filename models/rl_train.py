import os
import matplotlib.pyplot as plt
from rl_env import ESGTradingEnv
from rl_agent import ESGAgent
import numpy as np
import torch


os.makedirs("results", exist_ok=True)


env = ESGTradingEnv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /data_preprocessing/final_processed_esg_data.csv")


agent = ESGAgent(state_dim=4, action_dim=3, lr=0.0005, gamma=0.99, epsilon_decay=0.990)


episodes = 500
replay_buffer = []
reward_log = []
loss_log = []
portfolio_rl = []  #portfolio value
portfolio_baseline = []  #baseline strategy portfolio
initial_balance = 100000  #starting capital


for episode in range(episodes):
    state = env.reset()
    total_reward = 0
    portfolio_value = initial_balance
    baseline_value = initial_balance  

    for t in range(200):
        action = agent.get_action(state)
        next_state, reward, done, _ = env.step(action)
        
        
        reward = np.clip(reward, -1, 1)
        
        
        replay_buffer.append((state, action, reward, next_state))
        total_reward += reward

        
        if action == 1:  #invest more
            portfolio_value *= 1.01  #assume 1% 
        elif action == 2:  #invest less
            portfolio_value *= 0.99  #assume 1%
        
        baseline_value *= 1.005  #assume 0.5% 

        if done:
            break
        
        state = next_state

    
    loss = agent.train(replay_buffer, batch_size=32)
    loss_log.append(loss)
    reward_log.append(total_reward)
    portfolio_rl.append(portfolio_value)
    portfolio_baseline.append(baseline_value)
    
    print(f"Episode {episode}: Total Reward = {total_reward:.2f}, Portfolio Value (RL) = {portfolio_value:.2f}, Portfolio Value (Baseline) = {baseline_value:.2f}, Epsilon = {agent.epsilon:.3f}, Loss = {loss:.4f}")


torch.save(agent.model.state_dict(), "models/trained_rl_model.pth")
print("Model saved successfully!")


plt.figure(figsize=(10, 5))
plt.plot(reward_log, label="Total Reward per Episode", color="blue")
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.legend()
plt.title("Training Progress - Reward Over Time")
plt.savefig("results/reward_plot.png")
plt.show()


plt.figure(figsize=(10, 5))
plt.plot(loss_log, label="Loss per Episode", color="red")
plt.xlabel("Episode")
plt.ylabel("Loss")
plt.legend()
plt.title("Training Progress - Loss Over Time")
plt.savefig("results/loss_plot.png")
plt.show()


plt.figure(figsize=(10, 5))
plt.plot(portfolio_rl, label="RL-Based Portfolio", color="green")
plt.plot(portfolio_baseline, label="Baseline Portfolio", color="gray", linestyle="dashed")
plt.xlabel("Episode")
plt.ylabel("Portfolio Value")
plt.legend()
plt.title("Portfolio Performance: RL vs. Baseline")
plt.savefig("results/portfolio_comparison.png")
plt.show()

print("All results saved in 'results/' folder!")