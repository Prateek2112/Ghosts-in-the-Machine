
import numpy as np
import random
import constants as c

# Function to check if agent position and any ghost position matches i.e. is agent alive or not
def is_alive(agent_pos, ghost_pos):
    return not(agent_pos in ghost_pos)


# Function for agent movement
def agent_movement(maze, cell, ghost_pos):
    c.PATH_COVERED.append(cell)
    maze[c.AGENT_POS] = c.PATH_COVERED_KEY
    maze[cell] = c.AGENT_KEY
    c.AGENT_POS = cell

    return is_alive(c.AGENT_POS, ghost_pos)


# Function for agent movement in simulations
def agent_movement_sim(maze, cell, ghost_pos):
    c.PATH_COVERED_SIM.append(cell)
    maze[c.AGENT_POS_SIM] = c.PATH_COVERED_KEY
    maze[cell] = c.AGENT_KEY
    c.AGENT_POS_SIM = cell

    return is_alive(c.AGENT_POS_SIM, ghost_pos)


# Function for ghost movements
def ghost_movement(maze, agent_pos, ghost_pos, path):
    dir_movement = [(1,0),(0,1),(-1,0),(0,-1)]   # Directions (Down, Left, Up, Right)

    # Loop to iterate over each ghost
    for i in range(len(ghost_pos)):
        # Revert the cells of the ghosts' previous position to the original value
        if maze[ghost_pos[i]] == c.GHOST_INSIDE_WALL_KEY:
            maze[ghost_pos[i]] = c.BLOCKED_CELL_KEY
        elif maze[ghost_pos[i]] == c.GHOST_OUTSIDE_WALL_KEY:
            if ghost_pos[i] in path:
                maze[ghost_pos[i]] = c.PATH_REMAINING_KEY
            elif ghost_pos[i] in c.PATH_COVERED:
                maze[ghost_pos[i]] = c.PATH_COVERED_KEY
            else:
                maze[ghost_pos[i]] = c.UNBLOCKED_CELL_KEY

        # Loop to restrict the ghost movement in the inner 51x51 grid
        while True:
            new_pos = tuple(map(lambda x, y: x + y, ghost_pos[i], random.choice(dir_movement)))
            if maze[new_pos] != c.OUTER_WALL_KEY:  # Check if new ghost position is not out of bounds
                if maze[new_pos] == c.BLOCKED_CELL_KEY:
                    # If the new position is blocked cell then it will move in it with a 0.5 probability
                    if np.random.choice([0,1], p=[0.5,0.5]) == 1:
                        maze[new_pos] = c.GHOST_INSIDE_WALL_KEY
                        ghost_pos[i] = new_pos
                    else:
                        if maze[ghost_pos[i]] == c.BLOCKED_CELL_KEY:
                            maze[ghost_pos[i]] = c.GHOST_INSIDE_WALL_KEY
                        else:
                            maze[ghost_pos[i]] = c.GHOST_OUTSIDE_WALL_KEY
                else:
                    maze[new_pos] = c.GHOST_OUTSIDE_WALL_KEY
                    ghost_pos[i] = new_pos
                break

    return is_alive(agent_pos, ghost_pos)  # Return the alive status of the agent


# Function for ghost movements for low information scenario
def ghost_movement_low_info(maze, agent_pos, ghost_pos, ghost_pos_low_info, path):
    dir_movement = [(1,0),(0,1),(-1,0),(0,-1)]   # Directions (Down, Left, Up, Right)

    # Loop to iterate over each ghost
    for i in range(len(ghost_pos)):
        # Revert the cells of the ghosts' previous position to the original value
        if maze[ghost_pos[i]] == c.GHOST_INSIDE_WALL_KEY:
            maze[ghost_pos[i]] = c.BLOCKED_CELL_KEY
        elif maze[ghost_pos[i]] == c.GHOST_OUTSIDE_WALL_KEY:
            if ghost_pos[i] in path:
                maze[ghost_pos[i]] = c.PATH_REMAINING_KEY
            elif ghost_pos[i] in c.PATH_COVERED:
                maze[ghost_pos[i]] = c.PATH_COVERED_KEY
            else:
                maze[ghost_pos[i]] = c.UNBLOCKED_CELL_KEY

        # Loop to restrict the ghost movement in the inner 51x51 grid
        while True:
            new_pos = tuple(map(lambda x, y: x + y, ghost_pos[i], random.choice(dir_movement)))
            if maze[new_pos] != c.OUTER_WALL_KEY:  # Check if new ghost position is not out of bounds
                if maze[new_pos] == c.BLOCKED_CELL_KEY:
                    # If the new position is blocked cell then it will move in it with a 0.5 probability
                    if np.random.choice([0,1], p=[0.5,0.5]) == 1:
                        if maze[ghost_pos[i]] != c.BLOCKED_CELL_KEY:
                            # Remove the ghosts that move into the wall from the list is visible to the agent
                            ghost_pos_low_info.remove(ghost_pos[i])
                        maze[new_pos] = c.GHOST_INSIDE_WALL_KEY
                        ghost_pos[i] = new_pos
                    else:
                        if maze[ghost_pos[i]] == c.BLOCKED_CELL_KEY:
                            maze[ghost_pos[i]] = c.GHOST_INSIDE_WALL_KEY
                        else:
                            maze[ghost_pos[i]] = c.GHOST_OUTSIDE_WALL_KEY
                else:
                    maze[new_pos] = c.GHOST_OUTSIDE_WALL_KEY
                    ghost_pos[i] = new_pos
                break

    return is_alive(agent_pos, ghost_pos)  # Return the alive status of the agent

# Function for ghost movements for Agent 5 to store the last known location of ghosts that move into walls
def ghost_movement_a5(maze, agent_pos, ghost_pos, ghost_pos_low_info, path):
    dir_movement = [(1,0),(0,1),(-1,0),(0,-1)]   # Directions (Down, Left, Up, Right)

    # Loop to iterate over each ghost
    for i in range(len(ghost_pos)):
        # Revert the cells of the ghosts' previous position to the original value
        if maze[ghost_pos[i]] == c.GHOST_INSIDE_WALL_KEY:
            maze[ghost_pos[i]] = c.BLOCKED_CELL_KEY
        elif maze[ghost_pos[i]] == c.GHOST_OUTSIDE_WALL_KEY:
            if ghost_pos[i] in path:
                maze[ghost_pos[i]] = c.PATH_REMAINING_KEY
            elif ghost_pos[i] in c.PATH_COVERED:
                maze[ghost_pos[i]] = c.PATH_COVERED_KEY
            else:
                maze[ghost_pos[i]] = c.UNBLOCKED_CELL_KEY

        # Loop to restrict the ghost movement in the inner 51x51 grid
        while True:
            new_pos = tuple(map(lambda x, y: x + y, ghost_pos[i], random.choice(dir_movement)))
            if maze[new_pos] != c.OUTER_WALL_KEY:  # Check if new ghost position is not out of bounds
                if maze[new_pos] == c.BLOCKED_CELL_KEY:
                    # If the new position is blocked cell then it will move in it with a 0.5 probability
                    if np.random.choice([0,1], p=[0.5,0.5]) == 1:
                        if maze[ghost_pos[i]] != c.BLOCKED_CELL_KEY:
                            # Store the last known position of the ghosts that move into the walls in the list visible to the agent
                            ghost_pos_low_info = ghost_pos[i]
                        maze[new_pos] = c.GHOST_INSIDE_WALL_KEY
                        ghost_pos[i] = new_pos
                    else:
                        if maze[ghost_pos[i]] == c.BLOCKED_CELL_KEY:
                            maze[ghost_pos[i]] = c.GHOST_INSIDE_WALL_KEY
                        else:
                            maze[ghost_pos[i]] = c.GHOST_OUTSIDE_WALL_KEY
                else:
                    maze[new_pos] = c.GHOST_OUTSIDE_WALL_KEY
                    ghost_pos[i] = new_pos
                break

    return is_alive(agent_pos, ghost_pos)  # Return the alive status of the agent


# Funtion to randomly spawn 'num_of_ghosts' ghosts in the maze
def ghost_spawn(num_of_ghost, maze):
    unblocked_path = list(zip(*np.where(maze == c.UNBLOCKED_CELL_KEY)))

    # Randomly select from a list of unblocked cells for ghost spawn
    ghost_pos = random.sample(unblocked_path, num_of_ghost)
    # For each ghost, assign correct key to represent it in the maze
    for i in ghost_pos:
        if maze[i] == c.BLOCKED_CELL_KEY:
            maze[i] = c.GHOST_INSIDE_WALL_KEY
        elif maze[i] == c.UNBLOCKED_CELL_KEY:
            maze[i] = c.GHOST_OUTSIDE_WALL_KEY

    return ghost_pos  # Return the list of position of all the ghosts


# Function to randomly generate maze
def maze_generator():
    # Initiate maze to be solely of zeros
    maze = np.zeros(shape=(c.SIZE,c.SIZE))

    for i in range(c.SIZE):
        for j in range(c.SIZE):
            if (i == 0) or (i == c.SIZE-1):
                maze[i][j] = c.OUTER_WALL_KEY  # Border of the maze
            elif (j == 0) or (j == c.SIZE-1):
                maze[i][j] = c.OUTER_WALL_KEY  # Border of the maze
            else:
                # Randomly select 0 with probability of 28% and 1 with probability 72%
                maze[i][j] = np.random.choice([c.BLOCKED_CELL_KEY, c.UNBLOCKED_CELL_KEY], p=[0.28,0.72])
    # Place the agent at the start cell
    maze[c.START] = c.AGENT_KEY
    # Set the end cell to unblocked cell to ensure it is not blocked during maze generation
    maze[c.END] = c.UNBLOCKED_CELL_KEY
    
    return maze.astype(int)
