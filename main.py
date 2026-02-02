"""Main entry point for Snake AI project"""

import sys
sys.path.append('/workspaces/AI-project')

from training.train import train_agent, evaluate_agent
from training.test import test_trained_agent, play_single_game
from utils.visualization import plot_training_progress, print_statistics
from utils.config import *
import os
import pickle


def list_checkpoints(checkpoint_dir=CHECKPOINT_DIR):
    """List timestamped checkpoint folders under checkpoint_dir"""
    if not os.path.exists(checkpoint_dir):
        print("No checkpoints directory found.")
        return []

    entries = [d for d in os.listdir(checkpoint_dir) if os.path.isdir(os.path.join(checkpoint_dir, d))]
    entries.sort()
    if not entries:
        print("No checkpoints available.")
        return []

    print("\nAvailable checkpoints:")
    for idx, name in enumerate(entries, 1):
        print(f"{idx}. {name}")
    return entries


def find_best_checkpoint(metric='max', checkpoint_dir=CHECKPOINT_DIR):
    """Find best checkpoint by metric ('max' for best single-game, 'mean' for highest average).

    Returns (checkpoint_name, metric_value) or (None, None) if none found.
    """
    if not os.path.exists(checkpoint_dir):
        print("No checkpoints directory found.")
        return None, None

    best_name = None
    best_value = None

    for name in sorted(os.listdir(checkpoint_dir)):
        folder = os.path.join(checkpoint_dir, name)
        stats_path = os.path.join(folder, CHECKPOINT_STATS_FILENAME)
        if not os.path.isfile(stats_path):
            continue
        try:
            with open(stats_path, 'rb') as f:
                stats = pickle.load(f)
            scores = stats.get('scores', [])
            if not scores:
                continue
            if metric == 'max':
                v = max(scores)
            elif metric == 'mean':
                v = sum(scores) / len(scores)
            else:
                raise ValueError("Unknown metric")

            if best_value is None or v > best_value:
                best_value = v
                best_name = name
        except Exception as e:
            print(f"Failed to read stats for {name}: {e}")
            continue

    if best_name is None:
        print("No valid checkpoints found.")
        return None, None

    print(f"Best checkpoint by {metric}: {best_name} (value={best_value})")
    return best_name, best_value


def main():
    """Main menu for the Snake AI project"""

    while True:
        print("\n" + "="*60)
        print("SNAKE GAME AI - Q-LEARNING AGENT")
        print("="*60)
        print("\nOptions:")
        print("1 Train a new agent")
        print("2 Test trained agent")
        print("3 Play a single game with trained agent")
        print("4 View training progress and statistics")
        print("5 Evaluate trained agent")
        print("6 Manage checkpoints (list/restore)")
        print("7 Evaluate top checkpoint (auto-find best)")
        print("8 Exit")
        print("-"*60)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            # Ask whether to continue training the saved agent (default: yes)
            resume_input = input("\nContinue training saved agent if available? (Y/n): ").strip().lower()
            if resume_input in ("n", "no"):
                resume = False
            else:
                resume = True

            # Ask how many episodes to train in this session
            try:
                extra_eps = input(f"Number of episodes to run (default {NUM_EPISODES}): ").strip()
                if extra_eps == "":
                    episodes_to_run = NUM_EPISODES
                else:
                    episodes_to_run = int(extra_eps)
            except ValueError:
                print("Invalid number entered, using default.")
                episodes_to_run = NUM_EPISODES

            # Ask whether to render demo gameplay during training
            render_train_input = input("Render demo gameplay during training? (y/N): ").strip().lower()
            render_during_training = render_train_input in ("y", "yes")
            if render_during_training:
                try:
                    interval_in = input("Render every N episodes (default 500): ").strip()
                    render_interval = int(interval_in) if interval_in else 500
                except ValueError:
                    print("Invalid number, using default 500")
                    render_interval = 500
                try:
                    pause_in = input("Frame pause for demo render in seconds (default 0.1): ").strip()
                    render_pause = float(pause_in) if pause_in else 0.1
                except ValueError:
                    print("Invalid value, using default 0.1s")
                    render_pause = 0.1
            else:
                render_interval = 500
                render_pause = 0.1

            print(f"\nStarting training for {episodes_to_run} episodes (resume={resume}, render_demo={render_during_training})...")
            train_agent(
                num_episodes=episodes_to_run,
                max_steps=MAX_STEPS_PER_EPISODE,
                save_model=True,
                resume=resume,
                model_path=MODEL_SAVE_PATH,
                stats_path=STATS_SAVE_PATH,
                verbose=True,
                render_during_training=render_during_training,
                render_interval=render_interval,
                render_pause=render_pause
            )
        elif choice == "2":
            print("\nTesting trained agent...")
            test_trained_agent(num_tests=10)

        elif choice == "3":
            print("\nPlaying a game...")
            render_input = input("Render the game visually? (y/N): ").strip().lower()
            render = render_input in ("y", "yes")
            try:
                pause_in = input("Frame pause in seconds (default 0.1): ").strip()
                render_pause = float(pause_in) if pause_in else 0.1
            except ValueError:
                print("Invalid value, using default 0.1s")
                render_pause = 0.1

            score = play_single_game(verbose=True, render=render, render_pause=render_pause)
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
            # Manage checkpoints: list and allow user to restore one
            entries = list_checkpoints()
            if not entries:
                continue

            try:
                sel = int(input("Select a checkpoint number to manage (0 to cancel): ").strip())
            except ValueError:
                print("Invalid selection.")
                continue

            if sel == 0:
                continue
            if sel < 1 or sel > len(entries):
                print("Invalid selection.")
                continue

            selected = entries[sel - 1]
            cp_path = os.path.join(CHECKPOINT_DIR, selected)
            cp_model = os.path.join(cp_path, CHECKPOINT_MODEL_FILENAME)
            cp_stats = os.path.join(cp_path, CHECKPOINT_STATS_FILENAME)

            print(f"\nSelected checkpoint: {selected}")
            print("1 Resume training from this checkpoint")
            print("2 Evaluate agent from this checkpoint")
            print("3 Cancel")
            sub = input("Enter choice (1-3): ").strip()

            if sub == "1":
                try:
                    eps_in = input(f"Number of episodes to run (default {NUM_EPISODES}): ").strip()
                    episodes_to_run = int(eps_in) if eps_in else NUM_EPISODES
                except ValueError:
                    print("Invalid number entered, using default.")
                    episodes_to_run = NUM_EPISODES

                # Optionally render demo gameplay during resumed training
                render_train_input = input("Render demo gameplay during training? (y/N): ").strip().lower()
                render_during_training = render_train_input in ("y", "yes")
                if render_during_training:
                    try:
                        interval_in = input("Render every N episodes (default 500): ").strip()
                        render_interval = int(interval_in) if interval_in else 500
                    except ValueError:
                        print("Invalid number, using default 500")
                        render_interval = 500
                    try:
                        pause_in = input("Frame pause for demo render in seconds (default 0.1): ").strip()
                        render_pause = float(pause_in) if pause_in else 0.1
                    except ValueError:
                        print("Invalid value, using default 0.1s")
                        render_pause = 0.1
                else:
                    render_interval = 500
                    render_pause = 0.1

                train_agent(
                    num_episodes=episodes_to_run,
                    max_steps=MAX_STEPS_PER_EPISODE,
                    save_model=True,
                    resume=True,
                    model_path=cp_model,
                    stats_path=cp_stats,
                    checkpoint=True,
                    checkpoint_dir=CHECKPOINT_DIR,
                    render_during_training=render_during_training,
                    render_interval=render_interval,
                    render_pause=render_pause
                )

            elif sub == "2":
                from agent.q_agent import QAgent
                agent = QAgent(GRID_WIDTH, GRID_HEIGHT)
                try:
                    agent.load_model(cp_model)
                    evaluate_agent(agent, num_episodes=100)
                except FileNotFoundError:
                    print("Checkpoint model file not found.")

            else:
                continue

        elif choice == "7":
            # Evaluate best checkpoint automatically.
            print("\nEvaluate best checkpoint automatically.")
            print("1 Best single-game (max score)")
            print("2 Best average (mean score)")
            sel_metric = input("Select metric (1-2, default 1): ").strip()
            metric = 'max' if sel_metric in ('', '1') else 'mean'

            try:
                num_eval = input("Number of episodes for evaluation (default 100): ").strip()
                num_eval = int(num_eval) if num_eval else 100
            except ValueError:
                print("Invalid number; using default 100")
                num_eval = 100

            best_name, best_val = find_best_checkpoint(metric=metric)
            if not best_name:
                continue

            cp_path = os.path.join(CHECKPOINT_DIR, best_name)
            cp_model = os.path.join(cp_path, CHECKPOINT_MODEL_FILENAME)

            from agent.q_agent import QAgent
            agent = QAgent(GRID_WIDTH, GRID_HEIGHT)
            try:
                agent.load_model(cp_model)
                print(f"Evaluating checkpoint {best_name} ({metric}={best_val})")
                evaluate_agent(agent, num_episodes=num_eval)
            except FileNotFoundError:
                print("Checkpoint model file not found.")
            except Exception as e:
                print(f"Failed to load/evaluate checkpoint: {e}")

        elif choice == "8":
            print("Exiting...")
            sys.exit(0)

        else:
            print("Invalid choice. Please try again.")

        # Ask the user if they want to perform another action
        cont = input("\nDo you want to run another option? (y/n): ").strip().lower()
        if cont not in ("y", "yes"):
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
