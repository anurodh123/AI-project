# Snake Game AI - Q-Learning Agent

A complete implementation of a Q-Learning AI agent that learns to play the Snake game through reinforcement learning.

## Project Structure

```
AI-project/
├── game/                      # Game implementation
│   ├── __init__.py
│   └── snake_game.py         # Core Snake game logic
├── agent/                     # AI Agent implementation
│   ├── __init__.py
│   └── q_agent.py            # Q-Learning agent
├── training/                  # Training scripts
│   ├── __init__.py
│   ├── train.py              # Main training loop
│   └── test.py               # Testing and demo script
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── config.py             # Configuration settings
│   ├── state_representation.py # State encoding
│   └── visualization.py      # Visualization utilities
├── saved_models/             # Directory for saved models
├── main.py                   # Main entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the main menu:
```bash
python main.py
```

### Training the Agent

Train a new agent from scratch:
```bash
python training/train.py
```

Or from the main menu, select option 1.

**Training Parameters** (configurable in `utils/config.py`):
- `NUM_EPISODES`: Number of training episodes (default: 5000)
- `LEARNING_RATE`: Q-learning rate alpha (default: 0.1)
- `DISCOUNT_FACTOR`: Discount factor gamma (default: 0.95)
- `EPSILON`: Initial exploration rate (default: 1.0)
- `EPSILON_DECAY`: Exploration decay rate (default: 0.995)

### Testing the Agent

Test the trained agent:
```bash
python training/test.py
```

Or from the main menu, select option 2 or 3.

### Visualizing Training Progress

Plot training statistics and progress:
```bash
python -c "from utils.visualization import *; print_statistics(); plot_training_progress()"
```

Or from the main menu, select option 4.

## How It Works

### Q-Learning Algorithm

The agent uses the Q-Learning algorithm to learn an optimal policy:

1. **State Representation**: The game state is encoded as:
   - Relative position of food from snake head (dx, dy)
   - Obstacles in 4 directions (up, down, left, right)

2. **Actions**: 4 possible actions
   - 0: Move UP
   - 1: Move DOWN
   - 2: Move LEFT
   - 3: Move RIGHT

3. **Rewards**:
   - +10: Eating food
   - -0.01: Each step (encourages quick gameplay)
   - -10: Hitting wall or self

4. **Q-Update Rule**:
   ```
   Q(s, a) ← Q(s, a) + α[r + γ max Q(s', a') - Q(s, a)]
   ```

### Training Process

- The agent explores the environment using an epsilon-greedy policy
- Epsilon (exploration rate) decays over time, shifting focus to exploitation
- Q-values are updated after each action based on the reward and next state
- Model is saved after training completes

## Configuration

Edit `utils/config.py` to modify:

```python
# Game settings
GRID_WIDTH = 10          # Game grid width
GRID_HEIGHT = 10         # Game grid height

# Training parameters
LEARNING_RATE = 0.1      # Q-learning rate
DISCOUNT_FACTOR = 0.95   # Discount factor
EPSILON = 1.0            # Initial exploration rate
EPSILON_DECAY = 0.995    # Decay per episode
EPSILON_MIN = 0.01       # Minimum exploration rate

# Episode settings
NUM_EPISODES = 5000      # Total training episodes
MAX_STEPS_PER_EPISODE = 500  # Max steps per game

# Reward settings
REWARD_FOOD = 10         # Reward for eating food
REWARD_STEP = -0.01      # Step penalty
REWARD_DEATH = -10       # Death penalty
```

## Files Description

### `game/snake_game.py`
- `SnakeGame` class: Implements the Snake game environment
- Methods: `reset()`, `step()`, `get_score()`, etc.

### `agent/q_agent.py`
- `QAgent` class: Implements Q-Learning algorithm
- Methods: `get_action()`, `update_q_value()`, `save_model()`, `load_model()`

### `utils/state_representation.py`
- `encode_state()`: Converts game state to hashable Q-table key
- `get_obstacles()`: Detects obstacles in all directions

### `utils/config.py`
- Centralized configuration for all hyperparameters

### `training/train.py`
- `train_agent()`: Main training loop
- `evaluate_agent()`: Evaluate performance on test episodes

### `training/test.py`
- `test_trained_agent()`: Test agent on multiple games
- `play_single_game()`: Play a single game with detailed output

## Training Results

After training on 5000 episodes:
- The agent learns to navigate the grid and catch food
- Q-table grows to contain optimal values for discovered states
- Average score improves significantly over time
- Training progress can be visualized in real-time

## Improving Performance

To improve the agent's performance:

1. **Increase training episodes**: Higher NUM_EPISODES for more training
2. **Adjust learning rate**: Modify LEARNING_RATE (0.05-0.3 typically good)
3. **Tune discount factor**: DISCOUNT_FACTOR affects long-term planning (0.9-0.99)
4. **Adjust exploration decay**: EPSILON_DECAY controls exploration schedule
5. **Better state representation**: Enhance `encode_state()` in state_representation.py

## Future Enhancements

- [ ] GUI using pygame for visualization
- [ ] Deep Q-Network (DQN) implementation
- [ ] Policy Gradient methods
- [ ] Multi-agent training
- [ ] Curriculum learning with grid size progression
- [ ] Experience replay buffer
- [ ] Target network for stability

## License

This project is provided as-is for educational purposes.

## Author

Created as a complete Q-Learning implementation for Snake game AI training.
