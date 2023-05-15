
import matplotlib.pyplot as plt

import a_star as a
import maze_operations as m
import constants as c

def agent_1():
    # Path generation
    algo = a.a_star()
    path = algo.algorithm(c.GRID, c.START, c.END, c.GHOST_POS)

    is_alive = True
    for cell in path[::-1]:
        if is_alive:  # Check if agent is alive
            path.remove(cell)
            is_alive = m.ghost_movement(c.GRID, c.AGENT_POS, c.GHOST_POS, path)
            is_alive = is_alive and m.agent_movement(c.GRID, cell, c.GHOST_POS)

            # Visualization
            plt.imshow(c.GRID)
            plt.pause(0.001)
            plt.clf()
            if c.AGENT_POS == c.END:  # If Agent reaches goal then break out of loop
                plt.close()
                break
        else:  # If Agent dies
            print("You are a ghost now")
            plt.close()
            break

    plt.show()
