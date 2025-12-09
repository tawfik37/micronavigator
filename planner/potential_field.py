import math
from config.settings import (
    ATTRACTIVE_GAIN,
    REPULSIVE_GAIN,
    OBSTACLE_INFLUENCE,
    OBSTACLE
)

def compute_potential_field(grid, goal):
    rows = len(grid)
    cols = len(grid[0])

    potential = [[0.0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):

            if grid[r][c] == OBSTACLE:
                potential[r][c] = float("inf")
                continue

            # Attractive Potential (pull toward goal)
            # Far from goal → high value
            # Close to goal → low value
            dist_goal = math.dist((r, c), goal)
            U_att = ATTRACTIVE_GAIN * dist_goal

            # Repulsive Potential (push away from obstacles)
            min_dist_obs = find_distance_to_nearest_obstacle(grid, r, c)
            
            if min_dist_obs <= OBSTACLE_INFLUENCE:
                U_rep = REPULSIVE_GAIN * (1.0 / min_dist_obs - 1.0 / OBSTACLE_INFLUENCE) ** 2
            else:
                U_rep = 0

            # Combine both potentials
            potential[r][c] = U_att + U_rep

    return potential


def find_distance_to_nearest_obstacle(grid, r, c):
    rows = len(grid)
    cols = len(grid[0])

    min_dist = float("inf")

    for rr in range(rows):
        for cc in range(cols):
            if grid[rr][cc] == OBSTACLE:
                d = math.dist((r, c), (rr, cc))
                if d < min_dist:
                    min_dist = d

    return min_dist
