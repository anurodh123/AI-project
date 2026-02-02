"""Configuration settings for the Snake AI training"""

# Game settings
GRID_WIDTH = 10
GRID_HEIGHT = 10
CELL_SIZE = 20

# Training settings
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95
EPSILON = 1.0  # Exploration rate
EPSILON_DECAY = 0.995
EPSILON_MIN = 0.01

# Training parameters
NUM_EPISODES = 5000
MAX_STEPS_PER_EPISODE = 500
BATCH_SIZE = 32

# Reward settings
REWARD_FOOD = 10
REWARD_STEP = -0.01
REWARD_DEATH = -10
REWARD_BOUNDARY = -10

# Model settings
MODEL_SAVE_PATH = "saved_models/snake_ai_model.pkl"
STATS_SAVE_PATH = "saved_models/training_stats.pkl"

# Checkpoint settings (timestamped checkpoints saved under AI_PROJECT folder)
CHECKPOINT_DIR = "saved_models/checkpoints"
CHECKPOINT_MODEL_FILENAME = "model.pkl"
CHECKPOINT_STATS_FILENAME = "stats.pkl"
