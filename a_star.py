
from queue import PriorityQueue
import constants as c


class a_star:

    def __init__(self):
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Directions (Right, Down, Left, Up)


    def h(self, pt1, pt2):  # Manhattan distance heuristic
        x1, y1 = pt1
        x2, y2 = pt2
        return abs(x1-x2) + abs(y1-y2)


    def reconstruct(self, grid, came_from, current):  # Retrace the path
        path = []
        while current in came_from:
            path.append(current)
            grid[current] = c.PATH_REMAINING_KEY
            current = came_from[current]
        return path

    def is_valid(self, grid, start, end):  # Required for maze validation
        maze = grid.copy()
        return self.algorithm(maze, start, end, [])


    def algorithm(self, grid, start, end, ghost_pos):  # A star search algorithm
        count = 0
        priorityQueue = PriorityQueue()
        priorityQueue.put((0, count, start))
        came_from = {}
        g_score = {(i, j): float("inf") for i in range(c.SIZE) for j in range(c.SIZE)}
        g_score[start] = 0
        f_score = {(i, j): float("inf") for i in range(c.SIZE) for j in range(c.SIZE)}
        f_score[start] = self.h(start, end)

        open_set_hash = {start}

        while not priorityQueue.empty():
            current = priorityQueue.get()[2]
            open_set_hash.remove(current)

            if current == end:
                return self.reconstruct(grid, came_from, current)

            for d in self.directions:
                temp_g_score = g_score[current] + 1

                neighbour = (current[0]+d[0], current[1]+d[1])
                # Path should be within bounds and should not be a blocked cell or ghost
                if 0 < neighbour[0] < c.SIZE-1 and 0 < neighbour[1] < c.SIZE-1 and (grid[neighbour] == c.UNBLOCKED_CELL_KEY or grid[neighbour] == c.PATH_COVERED_KEY or grid[neighbour] == c.PATH_REMAINING_KEY) and neighbour not in ghost_pos:
                    if temp_g_score < g_score[neighbour]:
                        came_from[neighbour] = current
                        g_score[neighbour] = temp_g_score
                        f_score[neighbour] = temp_g_score + self.h(neighbour, end)
                        if neighbour not in open_set_hash:
                            count += 1
                            priorityQueue.put((f_score[neighbour], count, neighbour))
                            open_set_hash.add(neighbour)
        return []
