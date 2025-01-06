import numpy as np 
import random # Used on the grid size, door and key positions
from collections import deque, defaultdict #Q-table

# Function to generate a random position in the grid
def random_position(grid_size_X, grid_size_Y):
    return random.randint(0, grid_size_X - 1), random.randint(0, grid_size_Y - 1)

# Function to generate a random door position at either x = 0 or y = grid_size_Y - 1
def random_door_position(grid_size_X, grid_size_Y):
    if random.choice([True, False]):
        return 0, random.randint(0, grid_size_Y - 1)
    else:
        return random.randint(0, grid_size_X - 1), grid_size_Y - 1

# Function to print the grid in a readable format with separators
def print_grid(grid):
    for row in grid:
        print(' | '.join(row))
        print('-' * (4 * grid.shape[1] - 1))

# BFS pathfinding function
def bfs_pathfinding(grid, start, goal):
    rows, cols = grid.shape
    queue = deque([start])
    visited = set()
    visited.add(start)
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) == goal:
            return True
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx, ny] != 'O' and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
    
    return False

# Initialize system variables
grid_size_X = random.randint(5, 8) # Random grid size
grid_size_Y = random.randint(10, 15) # Random grid size
key_x, key_y = random_position(grid_size_X, grid_size_Y) # Random key coordinates on the grid
door_x, door_y = random_door_position(grid_size_X, grid_size_Y) # Random door coordinates on the grid
robot_start = (grid_size_X - 1, 0)  # Assuming the robot starts at the bottom-left corner
grid = np.full((grid_size_X, grid_size_Y), ' ') # Initialize the grid with empty strings to represent empty cells

# Example of placing items on the grid
grid[key_x, key_y] = 'K'  # K represents the key
grid[door_x, door_y] = 'D'  # D represents the door
grid[robot_start] = 'R'  # D represents the door

# Example of checking pathfinding

path_to_key = bfs_pathfinding(grid, robot_start, (key_x, key_y))
path_to_door = bfs_pathfinding(grid, (key_x, key_y), (door_x, door_y))



# Print the grid
print_grid(grid)

print("\n \nPath to key:", path_to_key)
print("Path to door:", path_to_door)