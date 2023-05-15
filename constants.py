
SIZE = 53  # 51 + 2 outer wall

# Initial positions
START = (1, 1)  # Start cell
END = (51, 51)  # End cell
AGENT_POS = START  # Current Agent position

# Maze representation keys
BLOCKED_CELL_KEY = 0  # Key to represent blocked cell on the maze
UNBLOCKED_CELL_KEY = 1  # Key to represent unblocked cell on the maze
GHOST_OUTSIDE_WALL_KEY = 2  # Key to represent ghost outside of wall on the maze
GHOST_INSIDE_WALL_KEY = 3  # Key to represent ghost inside of wall on the maze
AGENT_KEY = 4  # Key to represent agent on the maze
PATH_COVERED_KEY = 5  # Key to represent the path covered by the agent
PATH_REMAINING_KEY = 6  # Key to represent the planned path that the agent follows
OUTER_WALL_KEY = 7  # Key to represent the outer border

GRID = []  # Maze
GHOST_POS = []  # Ghost Positions
PATH_COVERED = []  # Path covered by the agent

# Simulation variable copies
AGENT_POS_SIM = START  # Current Agent Position for simulation
PATH_COVERED_SIM = []  # Path covered by the agent in the simulation
