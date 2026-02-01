"""Main entry point for Snake AI project"""

import sys
sys.path.append('/workspaces/AI-project')

from training.train import train_agent, evaluate_agent
from training.test import test_trained_agent, play_single_game
from utils.visualization import plot_training_progress, print_statistics
from utils.config import *


def main():
    """Main menu for the Snake AI project"""
    
    print("\n" + "="*60)
    print("SNAKE GAME AI - Q-LEARNING AGENT")
    print("="*60)
    print("\nOptions:")
    print("1. Train a new agent")
    print("2. Test trained agent")
    print("3. Play a single game with trained agent")
    print("4. View training progress and statistics")
    print("5. Evaluate trained agent")
    print("6. Exit")
    print("-"*60)
    
    choice = input("Enter your choice (1-6): ").strip()
    
    if choice == "1":
        print("\nStarting training...")
        train_agent(
            num_episodes=NUM_EPISODES,
            max_steps=MAX_STEPS_PER_EPISODE,
            save_model=True
        )
    
    elif choice == "2":
        print("\nTesting trained agent...")
        test_trained_agent(num_tests=10)
    
    elif choice == "3":
        print("\nPlaying a game...")
        score = play_single_game(verbose=True)
        print(f"\nScore: {score}")
    
    elif choice == "4":
        print("\nGenerating visualizations...")
        try:
            print_statistics()
            plot_training_progress()
        except FileNotFoundError:
            print("Training statistics not found. Please train the agent first.")
    
    elif choice == "5":
        print("\nEvaluating agent...")
        from game.snake_game import SnakeGame
        from agent.q_agent import QAgent
        
        game = SnakeGame(GRID_WIDTH, GRID_HEIGHT)
        agent = QAgent(GRID_WIDTH, GRID_HEIGHT)
        
        try:
            agent.load_model(MODEL_SAVE_PATH)
            evaluate_agent(agent, num_episodes=100)
        except FileNotFoundError:
            print(f"Model not found at {MODEL_SAVE_PATH}")
    
    elif choice == "6":
        print("Exiting...")
        sys.exit(0)
    
    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
