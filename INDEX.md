# Snake Game AI - Q-Learning Project Index

## 📁 Complete Project Structure

```
/workspaces/AI-project/
│
├── 📄 README.md                          # Main project documentation
├── 📄 GETTING_STARTED.md                 # Quick start guide
├── 📄 PROJECT_SUMMARY.md                 # Detailed project summary
├── 📄 requirements.txt                   # Python dependencies
├── 📄 setup.sh                           # Setup script
│
├── 📁 game/                              # Game Environment
│   ├── __init__.py
│   └── snake_game.py                     # Snake game implementation
│
├── 📁 agent/                             # AI Agent
│   ├── __init__.py
│   └── q_agent.py                        # Q-Learning agent
│
├── 📁 training/                          # Training & Testing
│   ├── __init__.py
│   ├── train.py                          # Training script
│   └── test.py                           # Testing & demo script
│
├── 📁 utils/                             # Utilities
│   ├── __init__.py
│   ├── config.py                         # Hyperparameter configuration
│   ├── state_representation.py           # State encoding logic
│   └── visualization.py                  # Training visualization
│
├── 📁 saved_models/                      # Trained models storage
│   ├── snake_ai_model.pkl               # (Generated after training)
│   ├── training_stats.pkl               # (Generated after training)
│   └── training_progress.png            # (Generated after training)
│
└── 📄 main.py                            # Interactive menu entry point
```

## 🎯 Quick Navigation

### To Start Training
```bash
python training/train.py
```
→ See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed instructions

### To Test the AI
```bash
python training/test.py
```

### For Interactive Menu
```bash
python main.py
```

### To View Results
```bash
python -c "from utils.visualization import *; print_statistics(); plot_training_progress()"
```

## 📚 Documentation Files

| File | Purpose | Read First? |
|------|---------|------------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | Quick setup & usage guide | ✅ YES |
| [README.md](README.md) | Full project documentation | ✅ YES |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Detailed component overview | After README |

## 🔧 Core Module Files

### Game Module (`game/`)
- **`snake_game.py`**: Snake game environment
  - `SnakeGame` class with game logic
  - Methods: `reset()`, `step()`, `get_score()`
  - Collision detection, food spawning, scoring

### Agent Module (`agent/`)
- **`q_agent.py`**: Q-Learning AI agent
  - `QAgent` class implementing Q-learning
  - Methods: `get_action()`, `update_q_value()`, `save_model()`, `load_model()`
  - Epsilon-greedy strategy, Q-table management

### Utils Module (`utils/`)
- **`config.py`**: Configuration and hyperparameters
  - Grid size, learning rates, episode counts
  - Reward values, decay schedules
  
- **`state_representation.py`**: State encoding
  - `encode_state()`: Game state to Q-table key
  - `get_obstacles()`: Obstacle detection
  
- **`visualization.py`**: Training visualization
  - `plot_training_progress()`: Generate plots
  - `print_statistics()`: Display metrics

### Training Module (`training/`)
- **`train.py`**: Main training script
  - `train_agent()`: Training loop with episodes
  - `evaluate_agent()`: Evaluate on test set
  
- **`test.py`**: Testing and demonstrations
  - `test_trained_agent()`: Multiple game tests
  - `play_single_game()`: Single game with verbose output

## 🚀 Getting Started (5 Minutes)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Training**
   ```bash
   python training/train.py
   ```

3. **Test Results**
   ```bash
   python training/test.py
   ```

4. **View Progress**
   ```bash
   python main.py  # Select option 4
   ```

## 📊 What Each Component Does

### Game Environment (`game/snake_game.py`)
- Manages 10×10 grid
- Handles snake movement (up, down, left, right)
- Spawns food randomly
- Detects collisions
- Calculates rewards

**Example Usage:**
```python
from game.snake_game import SnakeGame
game = SnakeGame(10, 10)
state = game.reset()
next_state, reward, done, info = game.step(action)
```

### Q-Learning Agent (`agent/q_agent.py`)
- Maintains Q-table (state → action values)
- Selects actions via epsilon-greedy
- Updates Q-values after each step
- Saves/loads trained models

**Example Usage:**
```python
from agent.q_agent import QAgent
agent = QAgent(10, 10)
action = agent.get_action(state, training=True)
agent.update_q_value(state, action, reward, next_state, done)
```

### State Encoding (`utils/state_representation.py`)
- Converts game state to hashable tuple
- Encodes relative food position
- Detects obstacles in 4 directions

**Example Usage:**
```python
from utils.state_representation import encode_state
encoded = encode_state(snake_pos, food_pos, 10, 10)
```

### Training Loop (`training/train.py`)
- Runs episodes with Q-learning updates
- Tracks scores and epsilon decay
- Saves model and statistics
- Provides training progress updates

## 🎓 Learning Algorithm

The project implements **Q-Learning** with:
- **State Space**: Relative food position + obstacle detection
- **Action Space**: 4 directions (up, down, left, right)
- **Update Rule**: Q(s,a) ← Q(s,a) + α[r + γmax Q(s',a') - Q(s,a)]
- **Exploration**: ε-greedy with decay schedule

## ⚙️ Configuration

All hyperparameters in [utils/config.py](utils/config.py):
```python
LEARNING_RATE = 0.1          # α in Q-learning
DISCOUNT_FACTOR = 0.95       # γ for future rewards
EPSILON = 1.0                # Initial exploration rate
NUM_EPISODES = 5000          # Training episodes
```

## 📈 Expected Results

After training 5000 episodes:
- **Average Score**: 2-4 food pieces
- **Q-Table Size**: 300-400 unique states
- **Training Time**: 5-10 minutes
- **Memory Usage**: ~1-2 MB

## 🔄 Workflow

```
1. Run training/train.py
   ↓
2. Train for 5000 episodes
   ↓
3. Save model to saved_models/
   ↓
4. Run training/test.py
   ↓
5. Evaluate performance
```

## 💾 File Locations

| Content | Location |
|---------|----------|
| Trained Model | `saved_models/snake_ai_model.pkl` |
| Training Stats | `saved_models/training_stats.pkl` |
| Progress Plot | `saved_models/training_progress.png` |
| Configuration | `utils/config.py` |

## 🔗 File Dependencies

```
main.py
  ├── training/train.py
  ├── training/test.py
  ├── game/snake_game.py
  ├── agent/q_agent.py
  └── utils/

training/train.py
  ├── game/snake_game.py
  ├── agent/q_agent.py
  └── utils/config.py

agent/q_agent.py
  └── utils/state_representation.py
```

## 🎮 Running the Project

### Option 1: Interactive Menu
```bash
python main.py
```
Choose from:
1. Train new agent
2. Test trained agent  
3. Play single game
4. View progress
5. Evaluate agent

### Option 2: Direct Commands
```bash
# Train
python training/train.py

# Test
python training/test.py

# Visualize
python utils/visualization.py
```

## 📝 Additional Resources

- **Quick Start**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **Full Docs**: [README.md](README.md)
- **Project Info**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## ✅ Project Completion Checklist

- ✅ Game environment (snake_game.py)
- ✅ Q-Learning agent (q_agent.py)
- ✅ State representation (state_representation.py)
- ✅ Training loop (train.py)
- ✅ Testing suite (test.py)
- ✅ Visualization tools (visualization.py)
- ✅ Configuration system (config.py)
- ✅ Main menu (main.py)
- ✅ Documentation (README.md, guides)
- ✅ Requirements file (requirements.txt)

## 🎉 Ready to Use!

The project is complete and ready for:
- Training AI agents
- Testing performance
- Visualizing results
- Experimenting with hyperparameters
- Learning Q-Learning concepts

---

**Start here**: [GETTING_STARTED.md](GETTING_STARTED.md)
