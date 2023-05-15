
import matplotlib.pyplot as plt
import time

import constants as c
import a_star as a
import maze_operations as m


directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Directions (Right, Down, Left, Up)


# Function to calculate Manhattan distance
def calc_manhattan_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)


# Function to initiate agent 2 simulations
def initiate_agent_2_sim():
    for d in directions:
        new_pos = (c.AGENT_POS[0] + d[0], c.AGENT_POS[1] + d[1])

        # Check if cell at new position is movable or not
        if c.GRID[new_pos] == c.OUTER_WALL_KEY or c.GRID[new_pos] == c.BLOCKED_CELL_KEY or c.GRID[new_pos] == c.GHOST_OUTSIDE_WALL_KEY:
            continue
        else:
            count = 0
            max = 0
            min_dist = 999999
            for _ in range(20):  # Loop for 20 simulations from each neighbour of the agent
                last_pos_sim = agent_2_sim(new_pos)  # Last position where the simulation ended
                if last_pos_sim == c.END:  # If last position is the end cell then increment count of the no. of times agent simulation reached the end cell
                    count += 1
                temp_dist = calc_manhattan_dist(last_pos_sim, c.END)  # Calculate distance between last simulation position and end cell
                if temp_dist < min_dist:  # Find the cell that reached closest to the end cell
                    min_dist = temp_dist
                    min_key = new_pos
                if count > max:  # Find the cell that reached the end cell maximum times
                    max = count
                    max_key = new_pos
        
    if max == 0:  # If none of the simulations reached the end cell then return the cell which reached closest to the end cell
        return min_key
    return max_key  # Else return the cell that reached the end cell maximum times


# Function to move away from ghost in case of no path
def move_away_from_ghost():
    ghost_agent_dist = {}  # Dictionary to store original distance between agent and ghosts
    run_away_to = {}  # Dictionary to store distance between each neighbour of the agent and the nearest ghost
    for ghost in c.GHOST_POS:
        ghost_agent_dist[ghost] = calc_manhattan_dist(c.AGENT_POS, ghost)
    min_dist_ghost = min(ghost_agent_dist, key=ghost_agent_dist.get)  # Retrieve key of min distance
    for dir in directions:
        temp = tuple(map(lambda x, y: x + y, c.AGENT_POS, dir))
        if c.GRID[temp] == c.UNBLOCKED_CELL_KEY or c.GRID[temp] == c.PATH_COVERED_KEY or c.GRID[temp] == c.PATH_REMAINING_KEY:
            run_away_to[temp] = calc_manhattan_dist(temp, min_dist_ghost)
    if run_away_to != {}:  # If cell available to move away from nearest ghost then move to cell with max distance
        return max(run_away_to, key=run_away_to.get)
    else:  # If cell not available to move away from nearest ghost then stay at the same position
        return c.AGENT_POS


# Function to simulate Agent 2
def agent_2_sim(start):

    # Copying variables for simulations
    grid_copy = c.GRID.copy()
    ghost_pos_copy = c.GHOST_POS.copy()
    c.AGENT_POS_SIM = c.AGENT_POS
    c.PATH_COVERED_SIM = []

    algo = a.a_star()
    path_sim = algo.algorithm(grid_copy, start, c.END, ghost_pos_copy)

    is_alive_sim = True
    while c.AGENT_POS_SIM != c.END:  # Loop till simulation reaches end cell
        if is_alive_sim:  # Check if agent is alive in simulation
            if path_sim:  # Check if path is available till end cell in simulation
                cell_sim = path_sim[-1]
                path_sim.remove(cell_sim)
                
                is_alive_sim = m.ghost_movement(grid_copy, c.AGENT_POS_SIM, ghost_pos_copy, path_sim)
                if any(p in path_sim for p in ghost_pos_copy) is True:  # Check if any ghost is obstructing the planned path
                    for i in path_sim:
                        grid_copy[i] = c.UNBLOCKED_CELL_KEY
                    path_sim = algo.algorithm(grid_copy, c.AGENT_POS_SIM, c.END, ghost_pos_copy)  # Replan path for the simulation
                    if path_sim:
                        cell_sim = path_sim[-1]
                is_alive_sim = is_alive_sim and m.agent_movement_sim(grid_copy, cell_sim, ghost_pos_copy)
                if c.AGENT_POS_SIM == c.END:  # If agent reaches the end cell in simulation then return end cell as the last position of the agent
                    return c.END
            else:  # If no path is available to the end cell
                ghost_agent_dist = {}  # Dictionary to store original distance between agent and ghosts
                run_away_to = {}  # Dictionary to store distance between each neighbour of the agent and the nearest ghost
                is_alive_sim = is_alive_sim and m.ghost_movement(grid_copy, c.AGENT_POS_SIM, ghost_pos_copy, [[]])
                for ghost in ghost_pos_copy:
                    ghost_agent_dist[ghost] = calc_manhattan_dist(c.AGENT_POS_SIM, ghost)
                min_dist_ghost = min(ghost_agent_dist, key=ghost_agent_dist.get)  # Retrieve key of min distance
                for dir in directions:
                    temp = tuple(map(lambda x, y: x + y, c.AGENT_POS, dir))
                    if grid_copy[temp] == c.UNBLOCKED_CELL_KEY or grid_copy[temp] == c.PATH_COVERED_KEY or grid_copy[temp] == c.PATH_REMAINING_KEY:
                        run_away_to[temp] = calc_manhattan_dist(temp, min_dist_ghost)
                if run_away_to != {}:  # If cell available to move away from nearest ghost then move to cell with max distance
                    max_dist_run = max(run_away_to, key=run_away_to.get)
                    is_alive_sim = is_alive_sim and m.agent_movement_sim(grid_copy, max_dist_run, ghost_pos_copy)
                else:  # If cell not available to move away from nearest ghost then stay at the same position
                    is_alive_sim = is_alive_sim and m.agent_movement_sim(grid_copy, c.AGENT_POS_SIM, ghost_pos_copy)
                path_sim = algo.algorithm(grid_copy, c.AGENT_POS_SIM, c.END, ghost_pos_copy)
        else:  # If agent dies in simulation then return the postion at which the agent died
            return c.AGENT_POS_SIM


# Function for agent 3
def agent_3():
    algo = a.a_star()
    path = algo.algorithm(c.GRID, c.START, c.END, c.GHOST_POS)  # Plan the initial path

    # Visualization
    plt.ion()
    fig, ax = plt.subplots()
    plot1 = ax.imshow(c.GRID)

    is_alive = True
    while c.AGENT_POS != c.END:  # Loop till the agent reaches the end cell
        # Update data for visualizations
        plot1.set_data(c.GRID)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.001)
        
        if is_alive:  # Check if agent is alive
            if path:  # Check if path is available till the end cell
                cell = path[-1]
                path.remove(cell)
                is_alive = m.ghost_movement(c.GRID, c.AGENT_POS, c.GHOST_POS, [])
                for ghost in c.GHOST_POS:
                    dist = calc_manhattan_dist(c.AGENT_POS, ghost)
                    if dist <= 5:
                        break

                if dist <= 5:  # If the nearest ghost is less than or equal to 5 Manhattan distance then simulate agent 2 for better survivability
                    max_survival_pos = initiate_agent_2_sim()  # Storing the best cell as determined by the simulations
                    if max_survival_pos not in c.GHOST_POS:  # If ghost does not exists on the new position then move to that position
                        is_alive = is_alive and m.agent_movement(c.GRID, max_survival_pos, c.GHOST_POS)
                    else:  # Else move away from the nearest ghost
                        move_away_from_ghost()
                elif any(p in path for p in c.GHOST_POS):  # Check if any ghost obstructs the planned path
                    for i in path:
                        c.GRID[i] = c.UNBLOCKED_CELL_KEY
                    path = algo.algorithm(c.GRID, c.AGENT_POS, c.END, c.GHOST_POS)  # Replan the path
                    if path:  # If path exists till the end cell then move to that cell
                        cell = path[-1]
                        path.remove(cell)
                    else:  # Else move away from the nearest ghost
                        cell = move_away_from_ghost()
                is_alive = is_alive and m.agent_movement(c.GRID, cell, c.GHOST_POS)

                if c.AGENT_POS == c.END:  # If agent reaches the end cell then break the loop
                    plt.close()
                    break
            else:  # If there is no path then move away from the nearest ghost
                is_alive = is_alive and m.ghost_movement(c.GRID, c.AGENT_POS, c.GHOST_POS, path)
                new_pos = move_away_from_ghost()
                is_alive = is_alive and m.agent_movement(c.GRID, new_pos, c.GHOST_POS)
                path = algo.algorithm(c.GRID, c.AGENT_POS, c.END, c.GHOST_POS)  # Replan the path
        else:  # If agent dies then break the loop
            print("You are a ghost now")
            plt.close()
            break
    plt.show()
