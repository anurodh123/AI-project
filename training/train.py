"""Training script for Snake AI using Q-Learning"""

import sys
sys.path.append('/workspaces/AI-project')

import numpy as np
import pickle
from game.snake_game import SnakeGame
from agent.q_agent import QAgent
from utils.config import *


def train_agent(num_episodes=NUM_EPISODES, max_steps=MAX_STEPS_PER_EPISODE, 
                save_model=True):
    """
    Train the Q-Learning agent to play Snake.
    
    Args:
        num_episodes: Number of training episodes
        max_steps: Maximum steps per episode
        save_model: Whether to save the trained model
    """
    # Initialize game and agent
    game = SnakeGame(GRID_WIDTH, GRID_HEIGHT)
    agent = QAgent(
        grid_width=GRID_WIDTH,
        grid_height=GRID_HEIGHT,
        learning_rate=LEARNING_RATE,
        discount_factor=DISCOUNT_FACTOR,
        epsilon=EPSILON,
        epsilon_decay=EPSILON_DECAY,
        epsilon_min=EPSILON_MIN
    )
    
    # Training statistics
    scores = []
    steps_list = []
    epsilon_values = []
    
    print(f"Starting training for {num_episodes} episodes...")
    print(f"Grid size: {GRID_WIDTH}x{GRID_HEIGHT}")
    print(f"Initial epsilon: {agent.epsilon}")
    print("-" * 50)
    
    # Training loop
    for episode in range(num_episodes):
        state = game.reset()
        episode_score = 0
        episode_steps = 0
        
        for step in range(max_steps):
            # Get action from agent
            action = agent.get_action(state, training=True)
            
            # Take action in game
            next_state, reward, done, info = game.step(action)
            
            # Update Q-value
            agent.update_q_value(state, action, reward, next_state, done)
            
            state = next_state
            episode_score = game.get_score()
            episode_steps = step + 1
            
            if done:
                break
        
        # Decay epsilon
        agent.decay_epsilon()
        
        # Store statistics
        scores.append(episode_score)
        steps_list.append(episode_steps)
        epsilon_values.append(agent.epsilon)
        
        # Print progress
        if (episode + 1) % 500 == 0:
            avg_score = np.mean(scores[-500:])
            avg_steps = np.mean(steps_list[-500:])
            print(f"Episode {episode + 1}/{num_episodes}")
            print(f"  Average Score (last 500): {avg_score:.2f}")
            print(f"  Average Steps (last 500): {avg_steps:.2f}")
            print(f"  Epsilon: {agent.epsilon:.4f}")
            print(f"  Q-Table Size: {agent.get_q_table_size()}")
            print("-" * 50)
    
    # Save model and statistics
    if save_model:
        agent.save_model(MODEL_SAVE_PATH)
        
        stats = {
            'scores': scores,
            'steps': steps_list,
            'epsilon_values': epsilon_values,
            'q_table_size': agent.get_q_table_size()
        }
        with open(STATS_SAVE_PATH, 'wb') as f:
            pickle.dump(stats, f)
        print(f"\nStatistics saved to {STATS_SAVE_PATH}")
    
    print(f"\nTraining completed!")
    print(f"Final Q-Table Size: {agent.get_q_table_size()}")
    print(f"Max Score Achieved: {max(scores)}")
    print(f"Average Score (last 100 episodes): {np.mean(scores[-100:]):.2f}")
    
    return agent, scores, steps_list, epsilon_values


def evaluate_agent(agent, num_episodes=100, max_steps=MAX_STEPS_PER_EPISODE):
    """
    Evaluate the trained agent.
    
    Args:
        agent: The trained Q-Learning agent
        num_episodes: Number of evaluation episodes
        max_steps: Maximum steps per episode
    
    Returns:
        List of scores from evaluation episodes
    """
    game = SnakeGame(GRID_WIDTH, GRID_HEIGHT)
    eval_scores = []
    
    print(f"\nEvaluating agent for {num_episodes} episodes...")
    print("-" * 50)
    
    for episode in range(num_episodes):
        state = game.reset()
        episode_score = 0
        
        for step in range(max_steps):
            # Get action from agent (no exploration)
            action = agent.get_action(state, training=False)
            
            # Take action in game
            next_state, reward, done, info = game.step(action)
            
            state = next_state
            episode_score = game.get_score()
            
            if done:
                break
        
        eval_scores.append(episode_score)
        
        if (episode + 1) % 20 == 0:
            print(f"Episode {episode + 1}/{num_episodes} - Score: {episode_score}")
    
    avg_score = np.mean(eval_scores)
    max_score = max(eval_scores)
    print("-" * 50)
    print(f"Evaluation Results:")
    print(f"  Average Score: {avg_score:.2f}")
    print(f"  Max Score: {max_score}")
    print(f"  Min Score: {min(eval_scores)}")
    
    return eval_scores


if __name__ == "__main__":
    # Train the agent
    agent, scores, steps, epsilon_vals = train_agent(
        num_episodes=NUM_EPISODES,
        max_steps=MAX_STEPS_PER_EPISODE,
        save_model=True
    )
    
    # Evaluate the agent
    eval_scores = evaluate_agent(agent, num_episodes=100)
