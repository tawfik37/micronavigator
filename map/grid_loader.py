import os
from config.settings import START, GOAL

def load_grid(file_path):
    """
    Loads a grid map from a text file, It reads each row - Converts text → numbers - So "0 1 0 3" becomes [0, 1, 0, 3] - 
    Finds start & goal locations 
    Returns:
        grid: 2D list of ints
        start: (row, col)
        goal: (row, col)
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Map file not found: {file_path}")

    grid = []
    start = None
    goal = None

    with open(file_path, "r") as f:
        for row_index, line in enumerate(f):
            # Split each line by spaces and convert to integers
            row = [int(x) for x in line.strip().split()]
            grid.append(row)

            # Search for start & goal in this row
            for col_index, cell in enumerate(row):
                if cell == START:
                    start = (row_index, col_index)
                elif cell == GOAL:
                    goal = (row_index, col_index)

    if start is None:
        raise ValueError("Start point (2) not found in map file.")
    if goal is None:
        raise ValueError("Goal point (3) not found in map file.")

    return grid, start, goal
