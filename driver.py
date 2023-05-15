
import maze_operations as m
import constants as c
import a_star as a
import agent_1 as a1
import agent_2 as a2
import agent_3 as a3
import agent_4 as a4
import agent_5 as a5

import agent_4_low_info as a4_li

# Driver code to run single instances of any agent

algo = a.a_star()
c.GRID = m.maze_generator()  # Generate a random maze
path = algo.is_valid(c.GRID, c.START, c.END)  # Check if generated maze is valid or not
while not path:  # If maze is not valid then generate and validate again
    c.GRID = m.maze_generator()
    path = algo.is_valid(c.GRID, c.START, c.END)

c.GHOST_POS = m.ghost_spawn(100, c.GRID)  # Randomly spawn ghosts in the maze

# Uncomment the agent that you want to run

# a1.agent_1()
# a2.agent_2()
# a3.agent_3()
# a4.agent_4()
# a5.agent_5()

# a4_li.agent_4_low_info()
