# Project Summary

## Complete Snake Game AI with Q-Learning

This project provides a fully functional AI training system for playing Snake using Q-Learning.

### What's Included

#### 1. **Game Environment** (`game/`)
- `snake_game.py`: Complete Snake game implementation
  - 10x10 grid environment
  - Snake movement and collision detection
  - Food spawning system
  - Score tracking

#### 2. **AI Agent** (`agent/`)
- `q_agent.py`: Q-Learning agent implementation
  - Q-table based learning
  - Epsilon-greedy exploration strategy
  - Model save/load functionality
  - Adjustable hyperparameters

#### 3. **State Representation** (`utils/`)
- `state_representation.py`: Intelligent state encoding
  - Relative food position (dx, dy normalized to -1, 0, 1)
  - Obstacle detection in 4 directions
  - Hashable state tuples for Q-table

#### 4. **Training System** (`training/`)
- `train.py`: Complete training loop
  - Configurable episodes and parameters
  - Progress tracking and logging
  - Model and statistics saving
  - Performance evaluation

- `test.py`: Testing and evaluation scripts
  - Test on multiple games
  - Single game demonstration
  - Score statistics

#### 5. **Configuration** (`utils/`)
- `config.py`: Centralized hyperparameters
  - Grid size (10x10)
  - Learning rate (0.1)
  - Discount factor (0.95)
  - Epsilon decay schedule
  - Reward structure

#### 6. **Visualization** (`utils/`)
- `visualization.py`: Training progress visualization
  - Score progression plots
  - Epsilon decay visualization
  - Training statistics summary

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the agent:**
   ```bash
   python training/train.py
   ```
   This will run 5000 training episodes and save the model.

3. **Test the trained agent:**
   ```bash
   python training/test.py
   ```
   This will run 10 test games and display scores.

4. **View training progress:**
   ```bash
   python utils/visualization.py
   ```
   This generates plots showing training statistics.

5. **Interactive menu:**
   ```bash
   python main.py
   ```
   Choose from multiple options to train, test, or visualize.

### Project Structure

```
AI-project/
├── game/
│   ├── __init__.py
│   └── snake_game.py          # Snake game logic
├── agent/
│   ├── __init__.py
│   └── q_agent.py             # Q-Learning agent
├── training/
│   ├── __init__.py
│   ├── train.py               # Training script
│   └── test.py                # Testing script
├── utils/
│   ├── __init__.py
│   ├── config.py              # Configuration
│   ├── state_representation.py # State encoding
│   └── visualization.py       # Visualization
├── saved_models/              # Trained models storage
├── main.py                    # Main menu
├── requirements.txt           # Dependencies
├── setup.sh                   # Quick setup script
└── README.md                  # Full documentation
```

### Key Features

✅ **Complete Q-Learning Implementation**
- Proper state encoding for efficient learning
- Epsilon-greedy exploration strategy
- Adaptive learning with epsilon decay

✅ **Flexible Configuration**
- Easy adjustment of all hyperparameters
- Grid size customization
- Reward structure modification

✅ **Comprehensive Evaluation**
- Training progress tracking
- Performance metrics
- Visualization tools

✅ **Production Ready**
- Model persistence (save/load)
- Error handling
- Clean code structure

### Default Hyperparameters

- **Grid Size**: 10x10
- **Learning Rate**: 0.1
- **Discount Factor**: 0.95
- **Initial Epsilon**: 1.0
- **Epsilon Decay**: 0.995
- **Episodes**: 5000
- **Max Steps per Episode**: 500

### Reward Structure

- Food eaten: +10
- Each step: -0.01
- Hit wall/self: -10

### Expected Performance

After training on 5000 episodes:
- Average score: 2-4 points
- Q-table size: ~300-400 unique states
- Learning curve shows clear improvement

### Customization Tips

1. **Faster Learning**: Increase learning rate to 0.2-0.3
2. **Better Long-term Planning**: Increase discount factor to 0.98-0.99
3. **More Exploration**: Decrease epsilon decay to 0.99
4. **Larger Grid**: Modify GRID_WIDTH and GRID_HEIGHT in config.py
5. **Custom Rewards**: Adjust REWARD_* values in config.py

### File Dependencies

- `main.py` - Entry point, imports from training and utils
- `training/train.py` - Uses game, agent, utils
- `training/test.py` - Uses game and agent
- `agent/q_agent.py` - Uses state_representation and config
- `game/snake_game.py` - Standalone game logic

### Next Steps for Enhancement

1. **Pygame GUI**: Add visual game display
2. **Deep Q-Network**: Implement neural network based agent
3. **Experience Replay**: Add memory buffer for better learning
4. **Policy Gradient**: Try actor-critic methods
5. **Multi-grid Training**: Progressive difficulty increase

---

**Created**: Complete AI project for Snake game training using Q-Learning
**Status**: Ready to use
**Python Version**: 3.8+
