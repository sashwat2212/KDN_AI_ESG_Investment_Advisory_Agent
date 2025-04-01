import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np

class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(4, 16)
        self.act1 = nn.LeakyReLU()  
        self.fc2 = nn.Linear(16, 16)
        self.act2 = nn.LeakyReLU()
        self.fc3 = nn.Linear(16, 3)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, x):
        x = self.act1(self.fc1(x))
        
        x = self.act2(self.fc2(x))
        
        x = self.softmax(self.fc3(x)) 
        
        return x  #giving raw Q-values

class ESGAgent:
    def __init__(self, state_dim, action_dim, lr=0.0005, gamma=0.99, epsilon_decay=0.990):
        self.model = DQN(state_dim, action_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()
        
        #parameters
        self.epsilon = 0.5  #not full exploration
        self.epsilon_min = 0.01
        self.epsilon_decay = epsilon_decay
        self.gamma = gamma

        self.action_dim = action_dim

    def get_action(self, state):
        if random.random() < self.epsilon:
            action = random.choice(range(self.action_dim))
            print(f"Random Action: {action}")
            return action
        else:
            state_tensor = torch.FloatTensor(state).unsqueeze(0)  #batch dimension
            action_probs = self.model(state_tensor)
            action = torch.argmax(action_probs).item()
            print(f"🤖 Model Action: {action}, Q-values: {action_probs.tolist()}")
            return action
        
    @staticmethod
    def load(model_path, state_dim, action_dim):
        
        agent = ESGAgent(state_dim, action_dim)
        agent.model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
        agent.model.eval()  #evaluation mode
        return agent

    def train(self, replay_buffer, batch_size=64):
        if len(replay_buffer) < batch_size:
            return None  #skip if not enough samples
        
        batch = random.sample(replay_buffer, batch_size)
        states, actions, rewards, next_states = zip(*batch)

        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).unsqueeze(1)  
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        next_states = torch.FloatTensor(next_states)

        
        with torch.no_grad():
            next_q_values = self.model(next_states)
            max_next_q_values = torch.max(next_q_values, dim=1, keepdim=True)[0]  
            targets = rewards + self.gamma * max_next_q_values

        
        predicted_q_values = self.model(states).gather(1, actions)

        #loss
        loss = self.loss_fn(predicted_q_values, targets)
        
        #backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        #decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

        print(f"Training Loss: {loss.item():.4f}, Epsilon: {self.epsilon:.3f}")
        return loss.item()  #return loss


# import torch
# import torch.nn as nn
# import torch.optim as optim
# import random
# import numpy as np

# class DQN_GRU(nn.Module):
    
#     def __init__(self, state_dim, action_dim, hidden_size=16):
#         super(DQN_GRU, self).__init__()
#         self.hidden_size = hidden_size  # Add this line
#         self.fc1 = nn.Linear(state_dim, hidden_size)
#         self.act1 = nn.LeakyReLU()
#         self.gru = nn.GRU(input_size=hidden_size, hidden_size=hidden_size, batch_first=True)
#         self.fc2 = nn.Linear(hidden_size, hidden_size)
#         self.act2 = nn.LeakyReLU()
#         self.fc3 = nn.Linear(hidden_size, action_dim)

        
#     def forward(self, x, hidden=None):
#         x = self.act1(self.fc1(x))

#         # Ensure input has batch dimension
#         x = x.unsqueeze(1)  # Shape: (batch_size, seq_len=1, hidden_dim)
        
#         # Pass through GRU
#         if hidden is None:
#             x, hidden = self.gru(x)
#         else:
#             x, hidden = self.gru(x, hidden)
        
#         x = self.act2(self.fc2(x.squeeze(1)))  # Remove seq_len dimension
        
#         x = self.fc3(x)  # Get Q-values
        
#         return x, hidden  # Return hidden state for tracking

# class ESGAgent:
#     def __init__(self, state_dim, action_dim, lr=0.00005, gamma=0.99, epsilon_decay=0.990):
#         self.model = DQN_GRU(state_dim, action_dim)
#         self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
#         self.loss_fn = nn.MSELoss()
        
#         self.epsilon = 1.0  
#         self.epsilon_min = 0.01
#         self.epsilon_decay = epsilon_decay
#         self.gamma = gamma

#         self.action_dim = action_dim
#         self.hidden = None  # Initialize GRU hidden state

#     def get_action(self, state):
#         if random.random() < self.epsilon:
#             action = random.choice(range(self.action_dim))
#             print(f"Random Action: {action}")
#             return action
#         else:
#             state_tensor = torch.FloatTensor(state).unsqueeze(0)  # (batch_size=1, state_dim)
#             q_values, self.hidden = self.model(state_tensor, self.hidden)  # Pass hidden state
            
#             action = torch.argmax(q_values).item()
#             print(f"Model Action: {action}, Q-values: {q_values.tolist()}")
#             return action
        
#     @staticmethod
#     def load(model_path, state_dim, action_dim):
#         agent = ESGAgent(state_dim, action_dim)
#         agent.model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
#         agent.model.eval()
#         return agent

#     def train(self, replay_buffer, batch_size=64):
#         if len(replay_buffer) < batch_size:
#             return None 
        
#         batch = random.sample(replay_buffer, batch_size)
#         states, actions, rewards, next_states = zip(*batch)

#         states = torch.FloatTensor(states)
#         actions = torch.LongTensor(actions).unsqueeze(1)
#         rewards = torch.FloatTensor(rewards).unsqueeze(1)
#         next_states = torch.FloatTensor(next_states)

#         # Compute target Q-values
#         with torch.no_grad():
#             next_q_values, _ = self.model(next_states)
#             max_next_q_values = torch.max(next_q_values, dim=1, keepdim=True)[0]
#             targets = rewards + self.gamma * max_next_q_values

#         # Compute predicted Q-values
#         predicted_q_values, _ = self.model(states)
#         predicted_q_values = predicted_q_values.gather(1, actions)

#         # Compute loss
#         loss = self.loss_fn(predicted_q_values, targets)
        
#         self.optimizer.zero_grad()
#         loss.backward()
#         self.optimizer.step()

#         self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

#         print(f"Training Loss: {loss.item():.4f}, Epsilon: {self.epsilon:.3f}")
#         return loss.item()
