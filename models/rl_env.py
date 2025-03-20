import gym
import numpy as np
import pandas as pd
from gym import spaces
from sklearn.preprocessing import MinMaxScaler

def load_and_preprocess_data(data_path):
    df = pd.read_csv(data_path)

    
    grade_mapping = {"A": 3, "B": 2, "BB": 1, "BBB": 0}  
    df["Gov_Grade"] = df["Gov_Grade"].map(grade_mapping)

    
    env_cols = ["avg_air_pollution", "avg_deforestation", "Weighted_ESG_Score"]
    df[env_cols] = df[env_cols].fillna(df[env_cols].median())  #median
    
    df["Gov_Grade"] = df["Gov_Grade"].fillna(0)  #fill with 0
    
    return df

class ESGTradingEnv(gym.Env):
    def __init__(self, data_path):
        super(ESGTradingEnv, self).__init__()

        self.data = load_and_preprocess_data(data_path)
        self.current_step = 0

        #action Space: invest (1), sell (-1), hold (0)
        self.action_space = spaces.Discrete(3)
        
        self.observation_space = spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)

    def step(self, action):
        self.current_step += 1
        done = self.current_step >= len(self.data) - 1
        
        esg_score = self.data.loc[self.current_step, "Weighted_ESG_Score"]
        pollution = self.data.loc[self.current_step, "avg_air_pollution"]
        deforestation = self.data.loc[self.current_step, "avg_deforestation"]
        governance = self.data.loc[self.current_step, "Gov_Grade"]

        
        reward = self.compute_reward(esg_score, pollution, deforestation, governance, action)

        
        next_state = np.nan_to_num(np.array([esg_score, pollution, deforestation, governance]))  

        return next_state, reward, done, {}

    def compute_reward(self, esg_score, pollution, deforestation, governance, action):
        reward = 0
        
        #scaled reward 
        if esg_score > 200:
            reward += (esg_score - 200) * 0.05 

        if governance > 1:
            reward += governance * 2  
        
        pollution_threshold = 0.01
        deforestation_threshold = 10.0

        if pollution > pollution_threshold or deforestation > deforestation_threshold:
            penalty = (pollution * 1000 + deforestation) * 0.1
            reward -= penalty

        
        if action == 0:  #hold
            reward += 0  #neutral
        elif action == 1:  #invest
            reward += esg_score * 0.02  #higher ESG = better rewards
        elif action == 2:  #invest Less
            reward -= esg_score * 0.02  #lower ESG = penalty

        return reward

    def reset(self):
        self.current_step = np.random.randint(0, len(self.data) // 2)  #random point
        return np.array([
            self.data.loc[self.current_step, "Weighted_ESG_Score"],
            self.data.loc[self.current_step, "avg_air_pollution"],
            self.data.loc[self.current_step, "avg_deforestation"],
            self.data.loc[self.current_step, "Gov_Grade"]
        ], dtype=np.float32)
