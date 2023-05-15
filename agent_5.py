
import matplotlib.pyplot as plt
import time
import a_star as a
import maze_operations as m
import constants as c


# Function to give the the nearest ghost and its bubble of radius 1
def near_ghost_func(ghost_pos_li):

    ghost_directions = [(1,0),(0,1),(-1,0),(0,-1)]  # Directions (Down, Left, Up, Right)
    
    ghost_agent_dist = {}  # Dictionary to store original distance between agent and ghosts
    
    for ghost in ghost_pos_li:
        x1, y1 = c.AGENT_POS
        x2, y2 = ghost
        ghost_agent_dist[ghost]=(abs(x1-x2) + abs(y1-y2))  # Manhattan Distance between each ghost and the agent
    min_dist_ghost = min(ghost_agent_dist, key=ghost_agent_dist.get)  # Retrieve key of min distance

    # Create a bubble around the nearest ghost
    near_ghost = [min_dist_ghost]
    for i in ghost_directions:
        x1, y1 = c.AGENT_POS
        ghost_move = tuple(map(lambda x, y: x + y, min_dist_ghost, i))
        near_ghost.append(ghost_move)

    return near_ghost  # Return the nearest ghost and the bubble


# Function for Agent 5
def agent_5():
    # Inital path generation
    algo = a.a_star()
    path = algo.algorithm(c.GRID, c.START, c.END,[])

    # Visualization
    plt.ion()
    fig, ax = plt.subplots()
    plot1 = ax.imshow(c.GRID)

    low_info_ghost_pos = c.GHOST_POS.copy()

    is_alive = True
    while c.AGENT_POS != c.END:  # Loop till agent does not reach end cell
        # Update data for visualization
        plot1.set_data(c.GRID)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.001)

        # Check if alive
        if is_alive:
            # Check if path is available
            if path:
                cell = path[-1]
                path.remove(cell)
                is_alive = m.ghost_movement_a5(c.GRID, c.AGENT_POS, c.GHOST_POS, low_info_ghost_pos, path)

                # Retrieve the nearest ghost and its bubble and join it with the remaining ghost positions
                ghost_near = near_ghost_func(low_info_ghost_pos)
                ghost_near.append(low_info_ghost_pos)

                # Check if ghost is obstructing the planned path
                if any(gp in path for gp in ghost_near) is True:
                    for i in path:
                        c.GRID[i] = c.UNBLOCKED_CELL_KEY
                    # Replan path beacuse ghost is obstructing the previously planned path
                    path = algo.algorithm(c.GRID, c.AGENT_POS, c.END, ghost_near)
                    if path:  # If replanning returned a path to the end cell then follow that path
                        cell = path[-1]
                is_alive = is_alive and m.agent_movement(c.GRID, cell, c.GHOST_POS)
                if c.AGENT_POS == c.END:  # If agent reaches end cell then break the loop
                    plt.close()
                    return True
            else:  # If there is no path then move away from nearest ghost (Manhattan Distance)
                m.ghost_movement_a5(c.GRID, c.AGENT_POS, c.GHOST_POS, low_info_ghost_pos, [])
                
                ghost_near = near_ghost_func(low_info_ghost_pos)  # Retrieve the nearest ghost and its bubble
                run_away_to = {}  # Dictionary to store distance between each neighbour of the agent and the nearest ghost
            
                for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # For each neighbour of agent
                    temp = tuple(map(lambda x, y: x + y, c.AGENT_POS, dir))
                    if c.GRID[temp] == c.UNBLOCKED_CELL_KEY or c.GRID[temp] == c.PATH_COVERED_KEY or c.GRID[temp] == c.PATH_REMAINING_KEY:
                        x3, y3 = temp
                        x4, y4 = ghost_near[0]
                        run_away_to[temp] = (abs(x4-x3) + abs(y4-y3))  # Manhattan Distance

                if run_away_to != {}:  # If cell available to move away from nearest ghost then move to cell with max distance
                    max_dist_run = max(run_away_to, key=run_away_to.get)
                    is_alive = is_alive and m.agent_movement(c.GRID, max_dist_run, c.GHOST_POS)
                else:  # If cell not available to move away from nearest ghost then stay at the same position
                    is_alive = is_alive and m.agent_movement(c.GRID, c.AGENT_POS, c.GHOST_POS)
                path = algo.algorithm(c.GRID, c.AGENT_POS, c.END, ghost_near)  # Check if path available for next iteration
        else:  # If agent dies
            print("You are a ghost now")
            plt.close()
            return False

    plt.show()
