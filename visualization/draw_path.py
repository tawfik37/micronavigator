import matplotlib.pyplot as plt
from config.settings import FREE, OBSTACLE, START, GOAL

def draw_path(grid, path, output_file="path_output.png"):
    """
    Draws the grid and overlays the path.

    Args:
        grid: 2D occupancy grid
        path: list of (row, col) tuples
        output_file: where to save the image (default: "path_output.png")
    """

    color_map = {
        FREE: 1.0,
        OBSTACLE: 0.0,
        START: 0.5,
        GOAL: 0.7
    }

    image = [[color_map[cell] for cell in row] for row in grid]

    plt.figure()
    plt.imshow(image, cmap="gray")

    # Extract x and y coordinates of the path
    y_coords = [p[1] for p in path]  # column = x axis
    x_coords = [p[0] for p in path]  # row = y axis

    plt.plot(y_coords, x_coords, color="red", linewidth=2)
    plt.title("Path on Grid")
    plt.savefig(output_file)
    plt.close()

