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
    print('-' * (4 * grid.shape[1] - 1))
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

# Function to generate obstacles on the grid
def generate_obstacles(grid, num_obstacles, key_pos, door_pos, robot_pos):
    grid_size_X, grid_size_Y = grid.shape
    obstacles = 0
    while obstacles < num_obstacles:
        x, y = random_position(grid_size_X, grid_size_Y)
        if (x, y) != key_pos and (x, y) != door_pos and (x, y) != robot_pos and grid[x, y] == ' ':
            grid[x, y] = 'O'  # O represents an obstacle
            obstacles += 1

# Q-learning parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate

# Initialize Q-table
q_table = defaultdict(lambda: np.zeros(4))  # 4 possible actions: up, down, left, right

# Define actions
actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
action_names = ['Up', 'Down', 'Left', 'Right']

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

# Initialize performance metrics
total_rewards = []
steps_to_key = []
steps_to_door = []

# Training the robot
num_episodes = 1
for episode in range(num_episodes):
    while True:
        # Reinitialize the grid and positions for each episode
        grid_size_X = random.randint(5, 8)
        grid_size_Y = random.randint(10, 15)
        key_x, key_y = random_position(grid_size_X, grid_size_Y)
        door_x, door_y = random_door_position(grid_size_X, grid_size_Y)
        robot_start = (grid_size_X - 1, 0)
        grid = np.full((grid_size_X, grid_size_Y), ' ')
        grid[key_x, key_y] = 'K'
        grid[door_x, door_y] = 'D'
        grid[robot_start] = 'R'
        num_obstacles = int(0.20 * grid_size_X * grid_size_Y)
        generate_obstacles(grid, num_obstacles, (key_x, key_y), (door_x, door_y), robot_start)

        # Check if there is a valid path to both the key and the door
        if bfs_pathfinding(grid, robot_start, (key_x, key_y)) and bfs_pathfinding(grid, (key_x, key_y), (door_x, door_y)):
            print("There is a valid path to both")
            break

    state = robot_start
    total_reward = 0
    steps = 0
    found_key = False
    while state != (door_x, door_y) or not found_key:
        action = choose_action(state)
        next_state = (state[0] + actions[action][0], state[1] + actions[action][1])
        print_grid(grid)
        if 0 <= next_state[0] < grid_size_X and 0 <= next_state[1] < grid_size_Y:
            reward = get_reward(state, next_state, (key_x, key_y), (door_x, door_y), found_key)
            if grid[next_state] == 'O':  # Hit an obstacle
                reward = -10
                update_q_table(state, action, reward, state)  # Update Q-table with the same state
                total_reward += reward
                print(f"Hit an obstacle at {next_state}. Turning back. Penalty: {reward}")
                # Choose a random valid move
                valid_moves = [a for a in actions if 0 <= state[0] + a[0] < grid_size_X and 0 <= state[1] + a[1] < grid_size_Y and grid[state[0] + a[0], state[1] + a[1]] != 'O']
                if valid_moves:
                    random_move = random.choice(valid_moves)
                    next_state = (state[0] + random_move[0], state[1] + random_move[1])
                    print(f"Random move to: {next_state}")
            else:
                update_q_table(state, action, reward, next_state)
                grid[state] = ' '  # Clear the robot's previous position
                state = next_state
                grid[state] = 'R'  # Mark the robot's new position
                total_reward += reward
                steps += 1
                print(f"Action: {action_names[action]}")
                print(f"State: {state}")
                print(f"Reward: {reward}")
                print('=' * 40)
                if state == (key_x, key_y):
                    found_key = True
                if steps >= 20:
                    break
        else:
            reward = -10  # Penalty for invalid move
            update_q_table(state, action, reward, state)
            total_reward += reward

    total_rewards.append(total_reward)
    if found_key:
        steps_to_key.append(steps)
    steps_to_door.append(steps)

    print(f"Episode {episode + 1}: Total Reward: {total_reward}")