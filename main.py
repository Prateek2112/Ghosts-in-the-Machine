
import pandas as pd
import os.path

import maze_operations as m
import constants as c
import a_star as a
import agent_1 as a1
import agent_2 as a2


# Function to reset the values before the next execution
def value_reset():
    c.AGENT_POS = c.START
    c.GRID = []
    c.GHOST_POS = []
    c.PATH_COVERED = []


# Funtion to generate maze
def generate_maze():
    c.GRID = m.maze_generator()  # Generate a random maze
    path = algo.is_valid(c.GRID, c.START, c.END)  # Check if generated maze is valid or not
    while not path:  # If maze is not valid then generate and validate again
        c.GRID = m.maze_generator()
        path = algo.is_valid(c.GRID, c.START, c.END)

algo = a.a_star()
agent2_data = pd.DataFrame(columns = ["Ghosts", "Status"])  # DataFrame for data collection
for ghost_num in range(10, 101, 5):  # Loop to iterate the no. of ghosts
    for j in range(50):  # Loop to run executions over each no. of ghosts
        generate_maze()  # Generate maze
        c.GHOST_POS = m.ghost_spawn(ghost_num, c.GRID)  # Randomly spawn 'ghost_num' no. of ghosts in the maze
        is_success = a2.agent_2()  # Returns whether the execution was successful or not
        DoA = "Dead"
        if is_success:  # If execution was success then 'Dead or Alive' variable is changed to Alive
            DoA = "Alive"
        
        # No. of ghosts and the status of the execution are appended to the dataframe as a row
        row = pd.DataFrame([{"Ghosts": ghost_num, "Status": DoA}])
        agent2_data = pd.concat([agent2_data, row], ignore_index=True)
        
        value_reset()  # Value reset before next execution
agent2_data.to_csv(os.path.join("data", "Agent2-Raw.csv"))  # Data frame exported to csv file
