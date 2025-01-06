# UniAI Project - Robot Pathfinding 🤖

## Overview
This project involves creating a robot that navigates a grid to find a key and then an exit door. The grid size is randomly generated, and obstacles are placed on the grid. The robot uses both the Breadth-First Search (BFS) algorithm and Q-learning to find the optimal path to its objectives.

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

## Q-learning Implementation

### Overview
Q-learning is a model-free reinforcement learning algorithm used to find the optimal action-selection policy for any given finite Markov decision process. It learns the value of an action in a particular state by receiving rewards and updating its Q-values.

### How Q-learning Works
1. **Initialization**:
   - Initialize the Q-table with zeros.
   - Set the learning rate (`alpha`), discount factor (`gamma`), and exploration rate (`epsilon`).

2. **Action Selection**:
   - Use an epsilon-greedy policy to choose an action:
     - With probability `epsilon`, choose a random action (exploration).
     - With probability `1 - epsilon`, choose the action with the highest Q-value (exploitation).

3. **Q-value Update**:
   - Execute the chosen action and observe the reward and next state.
   - Update the Q-value using the formula:
     ```python
     Q(state, action) = Q(state, action) + alpha * (reward + gamma * max(Q(next_state, all_actions)) - Q(state, action))
     ```

4. **Rewards and Penalties**:
   - The robot receives rewards and penalties based on its actions:
     - **+10** for reaching the key.
     - **+20** for reaching the door after obtaining the key.
     - **+3** for moving towards the key or door.
     - **-1** for moving away from the key or door.
     - **-10** for hitting an obstacle.
     - **-5** for reaching a dead end.
     - **-5** for reaching the door without the key.

### Q-learning Implementation in the Project
In this project, Q-learning is used to train the robot to find the optimal path to the key and then to the door.

#### Q-learning Parameters
```python
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate
```

#### Q-learning Functions
```python
# Function to choose an action based on epsilon-greedy policy
def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, 3)  # Explore: random action
    else:
        return np.argmax(q_table[state])  # Exploit: best action based on Q-table

# Function to update Q-table
def update_q_table(state, action, reward, next_state):
    best_next_action = np.argmax(q_table[next_state])
    td_target = reward + gamma * q_table[next_state][best_next_action]
    td_error = td_target - q_table[state][action]
    q_table[state][action] += alpha * td_error

# Function to get the reward for a given state
def get_reward(state, next_state, key_pos, door_pos, found_key):
    x, y = state
    nx, ny = next_state
    if next_state == key_pos:
        return 10
    elif next_state == door_pos:
        if found_key:
            return 20
        else:
            return -5  # Penalty for reaching the door without the key
    elif grid[nx, ny] == 'O':
        return -10
    elif not any(0 <= nx + dx < grid_size_X and 0 <= ny + dy < grid_size_Y and grid[nx + dx, ny + dy] != 'O' for dx, dy in actions):
        return -5  # Dead end
    else:
        if found_key:
            current_distance = abs(x - door_pos[0]) + abs(y - door_pos[1])
            next_distance = abs(nx - door_pos[0]) + abs(ny - door_pos[1])
            if next_distance < current_distance:
                return 3  # Reward for moving towards the door
            else:
                return -1  # Penalty for moving away from the door
        else:
            current_distance = abs(x - key_pos[0]) + abs(y - key_pos[1])
            next_distance = abs(nx - key_pos[0]) + abs(ny - key_pos[1])
            if next_distance < current_distance:
                return 3  # Reward for moving towards the key
            else:
                return -1  # Penalty for moving away from the key
```

### Usage in the Project
1. **Training the Robot**:
   ```python
   num_episodes = 1000
   for episode in range(num_episodes):
       # Initialize the grid and positions
       # ...existing code...
       
       state = robot_start
       total_reward = 0
       steps = 0
       found_key = False
       while state != (door_x, door_y) or not found_key:
           action = choose_action(state)
           next_state = (state[0] + actions[action][0], state[1] + actions[action][1])
           reward = get_reward(state, next_state, (key_x, key_y), (door_x, door_y), found_key)
           update_q_table(state, action, reward, next_state)
           state = next_state
           total_reward += reward
           steps += 1
           if state == (key_x, key_y):
               found_key = True
           if steps >= 20:
               break
       total_rewards.append(total_reward)
   ```

2. **Performance Metrics**:
   - Track total rewards, steps to the key, and steps to the door to evaluate the robot's performance over time.

### Summary
The BFS algorithm is used to ensure there is a valid path from the robot's starting position to the key and then to the door. The Q-learning algorithm allows the robot to learn the optimal path to the key and then to the door by exploring the grid, receiving rewards and penalties, and updating its Q-table. This approach enables the robot to improve its performance over multiple episodes, even with random grid configurations.