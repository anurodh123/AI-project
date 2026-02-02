"""Snake game environment"""

import random
import numpy as np
from enum import Enum


class Direction(Enum):
    """Direction enum for snake movement"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class SnakeGame:
    """Snake game environment for AI training"""
    
    def __init__(self, grid_width=10, grid_height=10):
        """
        Initialize the Snake game.
        
        Args:
            grid_width: Width of the game grid
            grid_height: Height of the game grid
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.reset()
    
    def reset(self):
        """Reset the game to initial state"""
        # Start snake in middle of grid
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        self.snake = [(start_x, start_y)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self._spawn_food()
        self.score = 0
        self.steps = 0
        
        return self._get_state()
    
    def step(self, action):
        """
        Execute one step of the game.
        
        Args:
            action: Action to take (0=up, 1=down, 2=left, 3=right)
        
        Returns:
            state: Current game state
            reward: Reward for this action
            done: Whether the game is over
            info: Additional information
        """
        self.steps += 1
        
        # Convert action to direction
        direction_map = {
            0: Direction.UP,
            1: Direction.DOWN,
            2: Direction.LEFT,
            3: Direction.RIGHT
        }
        self.next_direction = direction_map[action]
        
        # Move snake
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check if hit wall
        if not self._is_valid_position(new_head):
            return self._get_state(), -10, True, {"reason": "hit_wall"}
        
        # Check if hit self
        if new_head in self.snake:
            return self._get_state(), -10, True, {"reason": "hit_self"}
        
        # Move snake
        self.snake.insert(0, new_head)
        reward = -0.01  # Small penalty for each step
        
        # Check if ate food
        if new_head == self.food:
            self.score += 1
            reward = 10
            self.food = self._spawn_food()
        else:
            # Remove tail if didn't eat food
            self.snake.pop()
        
        done = False
        return self._get_state(), reward, done, {"score": self.score}
    
    def _is_valid_position(self, pos):
        """Check if position is within grid boundaries"""
        x, y = pos
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height
    
    def _spawn_food(self):
        """Spawn food at random location not occupied by snake"""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def _get_state(self):
        """Get current game state"""
        return {
            'snake': self.snake.copy(),
            'food': self.food,
            'score': self.score,
            'steps': self.steps
        }
    
    def get_snake_head(self):
        """Get snake head position"""
        return self.snake[0]
    
    def get_food_position(self):
        """Get food position"""
        return self.food
    
    def get_snake_body(self):
        """Get snake body positions"""
        return self.snake.copy()
    
    def get_score(self):
        """Get current score"""
        return self.score

    def render(self, ax=None, pause=0.05, cmap='viridis'):
        """
        Render the current game state using matplotlib.

        Args:
            ax: Optional matplotlib Axes to draw into. If None a new figure is created.
            pause: Time to pause after drawing (seconds)
            cmap: Colormap for display
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except Exception as e:
            raise RuntimeError(f"Rendering requires matplotlib and numpy: {e}")

        grid = np.zeros((self.grid_height, self.grid_width), dtype=int)

        # Mark snake body (1) and head (3)
        for i, (x, y) in enumerate(self.snake):
            # note: numpy array indexed [row, col] -> [y, x]
            val = 1
            if i == 0:
                val = 3
            grid[y, x] = val

        # Mark food (2)
        fx, fy = self.food
        grid[fy, fx] = 2

        created_fig = False
        if ax is None:
            fig, ax = plt.subplots(figsize=(4, 4))
            created_fig = True

        ax.clear()
        # Use a discrete colormap for clarity: 0-empty,1-snake,2-food,3-head
        cmap = plt.get_cmap('tab10')
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=3)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Score: {self.score}")

        plt.pause(pause)
        if created_fig:
            plt.show(block=False)
