"""Visualization utilities for training progress"""

import pickle
import matplotlib.pyplot as plt
import numpy as np


def plot_training_progress(stats_file='saved_models/training_stats.pkl'):
    """
    Plot training progress from saved statistics.
    
    Args:
        stats_file: Path to the saved statistics file
    """
    try:
        with open(stats_file, 'rb') as f:
            stats = pickle.load(f)
    except FileNotFoundError:
        print(f"Statistics file not found at {stats_file}")
        return
    
    scores = stats['scores']
    steps = stats['steps']
    epsilon_values = stats['epsilon_values']
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # Plot scores
    axes[0].plot(scores, alpha=0.6, label='Score')
    # Plot moving average
    window = 100
    moving_avg = np.convolve(scores, np.ones(window)/window, mode='valid')
    axes[0].plot(range(window-1, len(scores)), moving_avg, label=f'Moving Avg ({window} episodes)', linewidth=2)
    axes[0].set_xlabel('Episode')
    axes[0].set_ylabel('Score')
    axes[0].set_title('Training Score Progress')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot steps
    axes[1].plot(steps, alpha=0.6, label='Steps')
    moving_avg_steps = np.convolve(steps, np.ones(window)/window, mode='valid')
    axes[1].plot(range(window-1, len(steps)), moving_avg_steps, label=f'Moving Avg ({window} episodes)', linewidth=2)
    axes[1].set_xlabel('Episode')
    axes[1].set_ylabel('Steps')
    axes[1].set_title('Steps per Episode')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # Plot epsilon decay
    axes[2].plot(epsilon_values, label='Epsilon')
    axes[2].set_xlabel('Episode')
    axes[2].set_ylabel('Epsilon')
    axes[2].set_title('Exploration Rate (Epsilon) Decay')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('saved_models/training_progress.png', dpi=100)
    print("Training progress plot saved to saved_models/training_progress.png")
    plt.show()


def print_statistics(stats_file='saved_models/training_stats.pkl'):
    """
    Print training statistics.
    
    Args:
        stats_file: Path to the saved statistics file
    """
    try:
        with open(stats_file, 'rb') as f:
            stats = pickle.load(f)
    except FileNotFoundError:
        print(f"Statistics file not found at {stats_file}")
        return
    
    scores = stats['scores']
    steps = stats['steps']
    
    print("\n" + "="*50)
    print("TRAINING STATISTICS")
    print("="*50)
    print(f"Total Episodes: {len(scores)}")
    print(f"Max Score: {max(scores)}")
    print(f"Min Score: {min(scores)}")
    print(f"Average Score: {np.mean(scores):.2f}")
    print(f"Median Score: {np.median(scores):.2f}")
    print(f"Std Dev: {np.std(scores):.2f}")
    print(f"\nAverage Score (last 100): {np.mean(scores[-100:]):.2f}")
    print(f"Average Score (last 500): {np.mean(scores[-500:]):.2f}")
    print(f"\nMax Steps per Episode: {max(steps)}")
    print(f"Average Steps: {np.mean(steps):.2f}")
    print(f"Q-Table Size: {stats['q_table_size']}")
    print("="*50 + "\n")


if __name__ == "__main__":
    print_statistics()
    plot_training_progress()
