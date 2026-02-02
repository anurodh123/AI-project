# Getting Started with Snake AI

## Quick Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Train the AI
```bash
python training/train.py
```
This will train the Q-Learning agent for 5000 episodes. Training takes approximately 5-10 minutes depending on your system.

### Step 3: Test the Trained AI
```bash
python training/test.py
```
This will run 10 test games and show the results.

## Available Commands

### Training
```bash
# Train a new agent
python training/train.py

# Or use the interactive menu
python main.py
# Then select option 1
```

### Testing
```bash
# Test the trained agent on multiple games
python training/test.py

# Or use the interactive menu
python main.py
# Then select option 2 or 3
```

### Visualization
```bash
# Show training progress plots and statistics
python -c "from utils.visualization import *; print_statistics(); plot_training_progress()"

# Or use the interactive menu
python main.py
# Then select option 4
```

### Interactive Menu
```bash
python main.py
```
Provides an interactive menu with all options:
1. Train a new agent
2. Test trained agent
3. Play a single game
4. View training progress
5. Evaluate trained agent
6. Exit

## Understanding the Code

### Core Components

1. **Game (`game/snake_game.py`)**
   - Simulates the Snake game
   - Returns state, reward, and game status
   - Tracks score and steps

2. **Agent (`agent/q_agent.py`)**
   - Implements Q-Learning algorithm
   - Maintains Q-table (state → action values)
   - Selects actions using epsilon-greedy strategy

3. **State Encoding (`utils/state_representation.py`)**
   - Converts game state to hashable form
   - Encodes relative food position
   - Detects obstacles

4. **Training Loop (`training/train.py`)**
   - Runs multiple episodes
   - Updates Q-values
   - Saves trained models

## Configuration

Edit `utils/config.py` to customize:

```python
# Game grid size
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Learning parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95
EPSILON = 1.0

# Training episodes
NUM_EPISODES = 5000
MAX_STEPS_PER_EPISODE = 500

# Rewards
REWARD_FOOD = 10
REWARD_STEP = -0.01
REWARD_DEATH = -10
```

## Expected Output

### Training Output
```
Starting training for 5000 episodes...
Grid size: 10x10
Initial epsilon: 1.0
--------------------------------------------------
Episode 500/5000
  Average Score (last 500): 1.32
  Average Steps (last 500): 87.43
  Epsilon: 0.6065
  Q-Table Size: 156
--------------------------------------------------
Episode 1000/5000
  Average Score (last 500): 1.89
  Average Steps (last 500): 124.56
  Epsilon: 0.3679
  Q-Table Size: 287
--------------------------------------------------
...
Training completed!
```

### Test Output
```
Testing trained agent for 10 games
--------------------------------------------------
Game 1: Score = 3, Steps = 156
Game 2: Score = 2, Steps = 98
Game 3: Score = 4, Steps = 201
Game 4: Score = 2, Steps = 112
...
Average Score: 2.80
Best Score: 5
Worst Score: 1
```

## Troubleshooting

### Issue: Import errors when running scripts
**Solution**: Make sure you're running from the project root directory:
```bash
cd /workspaces/AI-project
python training/train.py
```

### Issue: matplotlib not found when plotting
**Solution**: Install visualization dependencies:
```bash
pip install matplotlib
```

### Issue: Model file not found when testing
**Solution**: Train the agent first before testing:
```bash
python training/train.py
# Wait for training to complete
python training/test.py
```

## Next Steps

1. **Analyze Results**: Check training plots in `saved_models/training_progress.png`
2. **Experiment**: Modify hyperparameters in `config.py` and retrain
3. **Improve State**: Enhance `state_representation.py` for better learning
4. **Visualize**: Create custom visualization scripts
5. **Enhance**: Add pygame GUI for real-time game visualization

## Project Files Reference

| File | Purpose |
|------|---------|
| `game/snake_game.py` | Snake game logic |
| `agent/q_agent.py` | Q-Learning implementation |
| `utils/config.py` | Configuration settings |
| `utils/state_representation.py` | State encoding |
| `training/train.py` | Training script |
| `training/test.py` | Testing script |
| `main.py` | Interactive menu |
| `saved_models/` | Trained models storage |

## Performance Tips

- **Faster Training**: Reduce NUM_EPISODES to 1000 for testing
- **Better Performance**: Increase NUM_EPISODES to 10000
- **Better Learning**: Decrease LEARNING_RATE to 0.05-0.08
- **Faster Convergence**: Increase EPSILON_DECAY to 0.99

## Common Questions

**Q: How long does training take?**
A: About 5-10 minutes for 5000 episodes on a typical machine.

**Q: How much memory does it use?**
A: Very little! Q-table typically uses ~1-2 MB.

**Q: Can I train on a GPU?**
A: Not needed - the model is simple enough for CPU-only training.

**Q: What's a good score?**
A: Average score of 2-4 after 5000 episodes is normal. Increase training for better results.

**Q: How do I improve the AI?**
A: Train longer, adjust hyperparameters, or improve state representation.

---

For more details, see [README.md](README.md) and [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
