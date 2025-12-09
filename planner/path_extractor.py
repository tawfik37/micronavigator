import math
from collections import deque

# 8 possible moves (up, down, left, right, and diagonals)
NEIGHBORS = [
    (-1, 0),   # up
    (1, 0),    # down
    (0, -1),   # left
    (0, 1),    # right
    (-1, -1),  # up-left
    (-1, 1),   # up-right
    (1, -1),   # down-left
    (1, 1),    # down-right
]

def extract_path(potential, start, goal, statistics=None):
    """
    Uses A* search guided by the potential field to find a path.
    Falls back to simple gradient descent if A* fails.

    Args:
        potential: 2D potential field
        start: (row, col) starting position
        goal: (row, col) goal position
        statistics: PlanningStatistics object (optional)

    Returns:
        path: list of (row, col) tuples
    """
    # First try: A* search using potential as heuristic
    path, nodes_explored = astar_search(potential, start, goal)

    if statistics:
        statistics.nodes_explored += nodes_explored

    if path and path[-1] == goal:
        return path

    # A* failed - likely no valid path exists
    if not path:
        print("A* search failed: no valid path exists from start to goal.")
        print("The map may have obstacles blocking all routes.")
        # Try gradient descent anyway to get as close as possible
        return gradient_descent_path(potential, start, goal)

    # Fallback: gradient descent with cycle detection
    print("A* found partial path, trying gradient descent...")
    return gradient_descent_path(potential, start, goal)


def astar_search(potential, start, goal):
    """
    A* pathfinding using the potential field as a heuristic.

    Returns:
        tuple: (path, nodes_explored)
    """
    from heapq import heappush, heappop

    rows = len(potential)
    cols = len(potential[0])

    # Priority queue: (f_score, g_score, position, path)
    open_set = []
    heappush(open_set, (potential[start[0]][start[1]], 0, start, [start]))

    # Track best g_score for each cell
    g_scores = {start: 0}

    # Limit iterations to prevent infinite loops
    max_iterations = rows * cols * 4
    iterations = 0
    nodes_explored = 0

    while open_set and iterations < max_iterations:
        iterations += 1
        f_score, g_score, current, path = heappop(open_set)
        nodes_explored += 1

        if current == goal:
            return path, nodes_explored

        r, c = current

        for dr, dc in NEIGHBORS:
            nr, nc = r + dr, c + dc

            # Check bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            neighbor = (nr, nc)

            # Skip obstacles
            if potential[nr][nc] == float("inf"):
                continue

            # Calculate cost (diagonal moves cost more)
            move_cost = 1.414 if (dr != 0 and dc != 0) else 1.0
            tentative_g = g_score + move_cost

            # Only consider if this is a better path
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                f_score = tentative_g + potential[nr][nc]
                new_path = path + [neighbor]
                heappush(open_set, (f_score, tentative_g, neighbor, new_path))

    return [], nodes_explored


def gradient_descent_path(potential, start, goal):
    """
    Simple gradient descent following the potential field.
    Allows revisiting cells but detects cycles.
    """
    path = [start]
    current = start
    recent_positions = deque(maxlen=20)  # Track recent positions to detect cycles
    recent_positions.append(start)

    max_steps = len(potential) * len(potential[0]) * 2

    for step in range(max_steps):
        if current == goal:
            return path

        r, c = current
        best_neighbor = None
        best_value = float("inf")

        # Find neighbor with lowest potential
        for dr, dc in NEIGHBORS:
            nr, nc = r + dr, c + dc

            if 0 <= nr < len(potential) and 0 <= nc < len(potential[0]):
                neighbor = (nr, nc)
                v = potential[nr][nc]

                if v < best_value:
                    best_value = v
                    best_neighbor = neighbor

        if best_neighbor is None or best_value == float("inf"):
            print("Path extraction failed: no valid neighbors.")
            return path

        # Detect if we're cycling (visiting same positions repeatedly)
        if step > 10 and best_neighbor in recent_positions:
            cycle_count = list(recent_positions).count(best_neighbor)
            if cycle_count > 2:
                print("Path extraction failed: detected cycle.")
                return path

        path.append(best_neighbor)
        recent_positions.append(best_neighbor)
        current = best_neighbor

    print("Path extraction failed: exceeded step limit.")
    return path
