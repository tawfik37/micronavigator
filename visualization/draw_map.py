import matplotlib.pyplot as plt
from config.settings import FREE, OBSTACLE, START, GOAL

def draw_map(grid):
    """
    Draws the occupancy grid using matplotlib.
    """
    color_map = {
        FREE: 1.0,        # white
        OBSTACLE: 0.0,    # black
        START: 0.5,       # gray
        GOAL: 0.7         # light gray
    }

    # Convert grid to color intensities
    image = [[color_map[cell] for cell in row] for row in grid]

    plt.imshow(image, cmap="gray")
    plt.title("Occupancy Grid")
    plt.savefig("map_output.png")
