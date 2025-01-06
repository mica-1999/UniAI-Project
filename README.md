# UniAI Project - Robot Pathfinding

## Overview
This project involves creating a robot that navigates a grid to find a key and then an exit door. The grid size is randomly generated, and obstacles are placed on the grid. The robot uses the Breadth-First Search (BFS) algorithm to find the shortest path to its objectives.

## Project Setup
1. **Grid Initialization**:
   - The grid size is randomly generated with dimensions between 5x10 and 8x15.
   - The grid is initialized with empty cells represented by spaces (`' '`).

2. **Random Position Generation**:
   - Random positions are generated for the key and the door.
   - The door is placed at either `x = 0` or `y = grid_size_Y - 1`.

3. **Placing Items on the Grid**:
   - The key is represented by `'K'`.
   - The door is represented by `'D'`.
   - The robot's starting position is represented by `'R'`.

4. **Pathfinding**:
   - The BFS algorithm is used to determine if there is a valid path from the robot's starting position to the key and then from the key to the door.

## Breadth-First Search (BFS) Algorithm

### Overview
Breadth-First Search (BFS) is a graph traversal algorithm used to explore nodes and edges of a graph. It starts from a given node (the root) and explores all its neighboring nodes at the present depth before moving on to nodes at the next depth level. BFS is particularly useful for finding the shortest path in unweighted graphs.

### How BFS Works
1. **Initialization**:
   - Start with the initial position (e.g., the robot's starting position) in the queue.
   - Add the initial position to the visited set.

2. **Exploration Loop**:
   - Enter the `while queue` loop, which continues until the queue is empty.
   - Dequeue the current position from the queue.
   - Check if the current position is the goal. If it is, return `True`.

3. **Neighbor Exploration**:
   - For each possible move (up, down, left, right), calculate the new position.
   - Check if the new position is within bounds, not an obstacle, and not visited.
   - If the new position is valid, append it to the queue and add it to the visited set.

4. **Repetition**:
   - The algorithm continues this process, exploring positions level by level.
   - If the queue becomes empty without finding the goal, return `False`.

### BFS Implementation in the Project
In this project, BFS is used to determine if there is a valid path from the robot's starting position to its first objective (the key) and then from the key to the door.

#### BFS Pathfinding Function
```python
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
```

### Explanation
1. **Initialization**:
   - `rows, cols = grid.shape`: Get the dimensions of the grid.
   - `queue = deque([start])`: Initialize the queue with the starting position.
   - `visited = set()`: Create a set to keep track of visited positions.
   - `visited.add(start)`: Mark the starting position as visited.

2. **Directions**:
   - `directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]`: Define the possible directions to move (up, down, left, right).

3. **Exploration Loop**:
   - `while queue`: Continue exploring until the queue is empty.
   - `x, y = queue.popleft()`: Dequeue the current position.
   - `if (x, y) == goal`: Check if the current position is the goal. If it is, return `True`.

4. **Neighbor Exploration**:
   - For each direction `(dx, dy)`:
     - `nx, ny = x + dx, y + dy`: Calculate the new position.
     - `if 0 <= nx < rows and 0 <= ny < cols and grid[nx, ny] != 'O' and (nx, ny) not in visited`: Check if the new position is valid:
       - `0 <= nx < rows`: Ensure the new row index is within the grid bounds.
       - `0 <= ny < cols`: Ensure the new column index is within the grid bounds.
       - `grid[nx, ny] != 'O'`: Ensure the new position is not an obstacle.
       - `(nx, ny) not in visited`: Ensure the new position has not been visited before.
     - `queue.append((nx, ny))`: Add the valid new position `(nx, ny)` to the queue for further exploration.
     - `visited.add((nx, ny))`: Mark the new position as visited to avoid re-exploring it.

5. **No Path Found**:
   - If the queue becomes empty without finding the goal, return `False`.

### Usage in the Project
1. **Path to Key**:
   ```python
   path_to_key = bfs_pathfinding(grid, robot_start, (key_x, key_y))
   ```
   - Checks if there is a path from the robot's starting position to the key.

2. **Path to Door**:
   ```python
   path_to_door = bfs_pathfinding(grid, (key_x, key_y), (door_x, door_y))
   ```
   - Checks if there is a path from the key to the door.

3. **Result**:
   - If both `path_to_key` and `path_to_door` are `True`, it means there is a valid path from the robot's starting position to the key and then from the key to the door.

### Summary
The BFS algorithm systematically explores all possible moves from the current position, ensuring that it visits every coordinate in the grid if there are no obstacles. It uses a queue to keep track of positions to explore and a set to keep track of visited positions. By exploring positions level by level, it guarantees that the shortest path is found if it exists.