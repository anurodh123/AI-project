"""Training script for Snake AI using Q-Learning"""

import sys
sys.path.append('/workspaces/AI-project')

import numpy as np
import pickle
import os
from datetime import datetime
from game.snake_game import SnakeGame
from agent.q_agent import QAgent
from utils.config import *


def train_agent(num_episodes=NUM_EPISODES, max_steps=MAX_STEPS_PER_EPISODE, 
                save_model=True, resume=False, model_path=MODEL_SAVE_PATH, stats_path=STATS_SAVE_PATH, agent=None, checkpoint=True, checkpoint_dir=CHECKPOINT_DIR):
    """
    Train the Q-Learning agent to play Snake.

    Supports resuming training from a saved model and appending statistics.

    Args:
        num_episodes: Number of training episodes to run in this call
        max_steps: Maximum steps per episode
        save_model: Whether to save the trained model and stats
        resume: If True, attempt to load existing model and stats
        model_path: Path to the saved model file
        stats_path: Path to the saved training statistics file
        agent: Existing QAgent instance to continue training (optional)
        checkpoint: Whether to write timestamped checkpoints into checkpoint_dir
        checkpoint_dir: Base directory for checkpoint folders
    """
    # Initialize game
    game = SnakeGame(GRID_WIDTH, GRID_HEIGHT)

    # Load or create agent
    if agent is None:
        agent = QAgent(
            grid_width=GRID_WIDTH,
            grid_height=GRID_HEIGHT,
            learning_rate=LEARNING_RATE,
            discount_factor=DISCOUNT_FACTOR,
            epsilon=EPSILON,
            epsilon_decay=EPSILON_DECAY,
            epsilon_min=EPSILON_MIN
        )

    if resume and os.path.exists(model_path):
        try:
            agent.load_model(model_path)
            print("Resumed agent from saved model.")
        except Exception as e:
            print(f"Failed to load model: {e}. Starting fresh agent.")

    # Training statistics (append if resuming stats exist)
    if resume and os.path.exists(stats_path):
        try:
            with open(stats_path, 'rb') as f:
                prev_stats = pickle.load(f)
            scores = prev_stats.get('scores', [])
            steps_list = prev_stats.get('steps', [])
            epsilon_values = prev_stats.get('epsilon_values', [])
            print(f"Loaded previous statistics: {len(scores)} episodes")
        except Exception as e:
            print(f"Failed to load previous stats: {e}. Starting fresh stats.")
            scores, steps_list, epsilon_values = [], [], []
    else:
        scores, steps_list, epsilon_values = [], [], []

    print(f"Starting training for {num_episodes} additional episodes...")
    print(f"Grid size: {GRID_WIDTH}x{GRID_HEIGHT}")
    print(f"Initial epsilon: {agent.epsilon}")
    print("-" * 50)

    # Ensure checkpoint dir exists
    if checkpoint:
        os.makedirs(checkpoint_dir, exist_ok=True)

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

        # Print progress and periodic checkpointing
        total_episode_index = len(scores)
        if total_episode_index % 500 == 0:
            avg_score = np.mean(scores[-500:])
            avg_steps = np.mean(steps_list[-500:])
            print(f"Episode {total_episode_index} (total)")
            print(f"  Average Score (last 500): {avg_score:.2f}")
            print(f"  Average Steps (last 500): {avg_steps:.2f}")
            print(f"  Epsilon: {agent.epsilon:.4f}")
            print(f"  Q-Table Size: {agent.get_q_table_size()}")
            print("-" * 50)

            # Save checkpoint
            if save_model:
                agent.save_model(model_path)
                stats = {
                    'scores': scores,
                    'steps': steps_list,
                    'epsilon_values': epsilon_values,
                    'q_table_size': agent.get_q_table_size()
                }
                with open(stats_path, 'wb') as f:
                    pickle.dump(stats, f)
                print(f"Checkpoint saved at episode {total_episode_index}.")

                if checkpoint:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    cp_subdir = os.path.join(checkpoint_dir, f"{ts}_ep{total_episode_index}")
                    os.makedirs(cp_subdir, exist_ok=True)
                    agent.save_model(os.path.join(cp_subdir, CHECKPOINT_MODEL_FILENAME))
                    with open(os.path.join(cp_subdir, CHECKPOINT_STATS_FILENAME), 'wb') as f:
                        pickle.dump(stats, f)
                    print(f"Timestamped checkpoint written to {cp_subdir}")

    # Save model and statistics at the end
    if save_model:
        agent.save_model(model_path)

        stats = {
            'scores': scores,
            'steps': steps_list,
            'epsilon_values': epsilon_values,
            'q_table_size': agent.get_q_table_size()
        }
        with open(stats_path, 'wb') as f:
            pickle.dump(stats, f)
        print(f"\nStatistics saved to {stats_path}")

        # Final timestamped checkpoint
        if checkpoint:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            cp_subdir = os.path.join(checkpoint_dir, f"{ts}_ep{len(scores)}")
            os.makedirs(cp_subdir, exist_ok=True)
            agent.save_model(os.path.join(cp_subdir, CHECKPOINT_MODEL_FILENAME))
            with open(os.path.join(cp_subdir, CHECKPOINT_STATS_FILENAME), 'wb') as f:
                pickle.dump(stats, f)
            print(f"Final timestamped checkpoint written to {cp_subdir}")

    print(f"\nTraining completed!")
    print(f"Final Q-Table Size: {agent.get_q_table_size()}")
    if scores:
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
