"""State representation for Snake game"""

import numpy as np


def encode_state(snake_pos, food_pos, grid_width, grid_height):
    """
    Encode the game state into a tuple that can be used as a Q-table key.
    
    Args:
        snake_pos: List of tuples representing snake body positions (head is first)
        food_pos: Tuple of (x, y) representing food position
        grid_width: Width of game grid
        grid_height: Height of game grid
    
    Returns:
        A tuple representing the state
    """
    head_x, head_y = snake_pos[0]
    food_x, food_y = food_pos
    
    # Calculate relative positions
    dx = food_x - head_x
    dy = food_y - head_y
    
    # Normalize directions to [-1, 0, 1]
    dx = max(-1, min(1, dx))
    dy = max(-1, min(1, dy))
    
    # Check for obstacles in all directions
    obstacles = get_obstacles(snake_pos, grid_width, grid_height)
    
    # Create state tuple
    state = (dx, dy, tuple(obstacles))
    
    return state


def get_obstacles(snake_pos, grid_width, grid_height):
    """
    Detect obstacles (walls or snake body) in all 4 directions from head.
    
    Args:
        snake_pos: List of tuples representing snake body positions
        grid_width: Width of game grid
        grid_height: Height of game grid
    
    Returns:
        List of 4 booleans [up, down, left, right] indicating obstacles
    """
    head_x, head_y = snake_pos[0]
    snake_body = set(snake_pos[1:])  # Exclude head
    
    obstacles = [0, 0, 0, 0]  # [up, down, left, right]
    
    # Check up
    if head_y - 1 < 0 or (head_x, head_y - 1) in snake_body:
        obstacles[0] = 1
    
    # Check down
    if head_y + 1 >= grid_height or (head_x, head_y + 1) in snake_body:
        obstacles[1] = 1
    
    # Check left
    if head_x - 1 < 0 or (head_x - 1, head_y) in snake_body:
        obstacles[2] = 1
    
    # Check right
    if head_x + 1 >= grid_width or (head_x + 1, head_y) in snake_body:
        obstacles[3] = 1
    
    return obstacles


def get_state_size(grid_width, grid_height):
    """
    Calculate the approximate number of possible states.
    
    Returns:
        Estimated number of states
    """
    # Direction to food: 9 possibilities (3x3 grid of relative positions)
    # Obstacles: 16 possibilities (4 binary indicators)
    return 9 * 16
