"""Q-Learning agent for Snake game"""

import numpy as np
import random
import pickle
from utils.state_representation import encode_state


class QAgent:
    """Q-Learning agent for Snake game"""
    
    def __init__(self, grid_width=10, grid_height=10, learning_rate=0.1, 
                 discount_factor=0.95, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        """
        Initialize the Q-Learning agent.
        
        Args:
            grid_width: Width of game grid
            grid_height: Height of game grid
            learning_rate: Learning rate (alpha)
            discount_factor: Discount factor (gamma)
            epsilon: Exploration rate
            epsilon_decay: Decay rate for epsilon
            epsilon_min: Minimum epsilon value
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        # Q-table: maps states to action values
        self.q_table = {}
        
        # Number of actions (up, down, left, right)
        self.num_actions = 4
    
    def get_action(self, state, training=True):
        """
        Get action using epsilon-greedy policy.
        
        Args:
            state: Current game state
            training: Whether in training mode
        
        Returns:
            Action to take (0=up, 1=down, 2=left, 3=right)
        """
        # Encode state
        encoded_state = encode_state(state['snake'], state['food'], 
                                     self.grid_width, self.grid_height)
        
        # Initialize state in Q-table if not exists
        if encoded_state not in self.q_table:
            self.q_table[encoded_state] = np.zeros(self.num_actions)
        
        # Epsilon-greedy selection
        if training and random.random() < self.epsilon:
            # Explore: random action
            return random.randint(0, self.num_actions - 1)
        else:
            # Exploit: best action
            q_values = self.q_table[encoded_state]
            return np.argmax(q_values)
    
    def update_q_value(self, state, action, reward, next_state, done):
        """
        Update Q-value using Q-learning formula.
        
        Args:
            state: Previous state
            action: Action taken
            reward: Reward received
            next_state: Next state
            done: Whether episode is done
        """
        # Encode states
        encoded_state = encode_state(state['snake'], state['food'], 
                                     self.grid_width, self.grid_height)
        encoded_next_state = encode_state(next_state['snake'], next_state['food'], 
                                          self.grid_width, self.grid_height)
        
        # Initialize states in Q-table if not exists
        if encoded_state not in self.q_table:
            self.q_table[encoded_state] = np.zeros(self.num_actions)
        if encoded_next_state not in self.q_table:
            self.q_table[encoded_next_state] = np.zeros(self.num_actions)
        
        # Q-learning update rule
        current_q = self.q_table[encoded_state][action]
        if done:
            max_next_q = 0
        else:
            max_next_q = np.max(self.q_table[encoded_next_state])
        
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[encoded_state][action] = new_q
    
    def decay_epsilon(self):
        """Decay epsilon for exploration-exploitation tradeoff"""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def save_model(self, filepath):
        """
        Save the Q-table to a file.
        
        Args:
            filepath: Path to save the model
        """
        with open(filepath, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load the Q-table from a file.
        
        Args:
            filepath: Path to load the model from
        """
        with open(filepath, 'rb') as f:
            self.q_table = pickle.load(f)
        print(f"Model loaded from {filepath}")
    
    def get_q_table_size(self):
        """Get the size of the Q-table"""
        return len(self.q_table)
    
    def reset_q_table(self):
        """Reset the Q-table"""
        self.q_table = {}
