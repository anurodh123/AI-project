"""Test and demonstration script for the trained Snake AI"""

import sys
sys.path.append('/workspaces/AI-project')

from game.snake_game import SnakeGame
from agent.q_agent import QAgent
from utils.config import MODEL_SAVE_PATH, GRID_WIDTH, GRID_HEIGHT


def test_trained_agent(num_tests=10):
    """
    Test the trained agent and display results.
    
    Args:
        num_tests: Number of test games to play
    """
    # Initialize game and agent
    game = SnakeGame(GRID_WIDTH, GRID_HEIGHT)
    agent = QAgent(GRID_WIDTH, GRID_HEIGHT)
    
    # Load trained model
    try:
        agent.load_model(MODEL_SAVE_PATH)
    except FileNotFoundError:
        print(f"Model not found at {MODEL_SAVE_PATH}")
        print("Please train the agent first using training/train.py")
        return
    
    print(f"Testing trained agent for {num_tests} games")
    print("-" * 50)
    
    scores = []
    max_steps = 500
    
    for test_num in range(num_tests):
        state = game.reset()
        score = 0
        steps = 0
        
        for step in range(max_steps):
            # Get action from trained agent (no exploration)
            action = agent.get_action(state, training=False)
            
            # Take action
            next_state, reward, done, info = game.step(action)
            
            state = next_state
            score = game.get_score()
            steps = step + 1
            
            if done:
                break
        
        scores.append(score)
        print(f"Game {test_num + 1}: Score = {score}, Steps = {steps}")
    
    print("-" * 50)
    print(f"Average Score: {sum(scores) / len(scores):.2f}")
    print(f"Best Score: {max(scores)}")
    print(f"Worst Score: {min(scores)}")


def play_single_game(verbose=True, render=False, render_pause=0.1):
    """
    Play a single game with the trained agent.

    Args:
        verbose: Whether to print detailed game information
        render: Whether to render the game visually using matplotlib
        render_pause: Pause time between frames when rendering
    """
    game = SnakeGame(GRID_WIDTH, GRID_HEIGHT)
    agent = QAgent(GRID_WIDTH, GRID_HEIGHT)

    try:
        agent.load_model(MODEL_SAVE_PATH)
    except FileNotFoundError:
        print(f"Model not found at {MODEL_SAVE_PATH}")
        return

    state = game.reset()
    max_steps = 500

    if render:
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(4, 4))
            plt.ion()
        except Exception as e:
            print(f"Rendering unavailable: {e}. Continuing without render.")
            render = False

    if verbose:
        print("\nStarting game...")
        print("-" * 50)

    for step in range(max_steps):
        action = agent.get_action(state, training=False)
        next_state, reward, done, info = game.step(action)

        if render:
            try:
                game.render(ax=ax, pause=render_pause)
            except Exception as e:
                print(f"Render failed: {e}")
                render = False

        if verbose and step % 50 == 0:
            print(f"Step {step}: Score = {game.get_score()}, Snake Length = {len(game.get_snake_body())}")

        state = next_state

        if done:
            break

    if render:
        try:
            plt.ioff()
            plt.show()
        except Exception:
            pass

    if verbose:
        print("-" * 50)
        print(f"Game Over! Final Score: {game.get_score()}")

    return game.get_score()


if __name__ == "__main__":
    print("="*50)
    print("SNAKE AI - TEST SCRIPT")
    print("="*50)
    
    test_trained_agent(num_tests=10)
    
    print("\n" + "="*50)
    print("Playing a single game...")
    print("="*50)
    play_single_game(verbose=True)
