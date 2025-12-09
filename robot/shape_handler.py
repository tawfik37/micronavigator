from config.settings import OBSTACLE, ROBOT_WIDTH, ROBOT_HEIGHT

def inflate_obstacles(grid, robot_width=None, robot_height=None):
    """
    Inflates obstacles to account for robot's rectangular shape.

    The robot is treated as a rectangle of size (robot_height x robot_width).
    We inflate obstacles so that planning can treat the robot as a point.

    Args:
        grid: 2D list representing the occupancy grid
        robot_width: width of robot in grid cells (default from settings)
        robot_height: height of robot in grid cells (default from settings)

    Returns:
        inflated_grid: new grid with inflated obstacles
    """
    if robot_width is None:
        robot_width = ROBOT_WIDTH
    if robot_height is None:
        robot_height = ROBOT_HEIGHT

    rows = len(grid)
    cols = len(grid[0])

    # Create a copy of the grid
    inflated_grid = [row[:] for row in grid]

    # Calculate inflation radius (half the robot size, rounded up)
    inflate_r = (robot_height - 1) // 2
    inflate_c = (robot_width - 1) // 2

    # Find all obstacle cells
    obstacles = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == OBSTACLE:
                obstacles.append((r, c))

    # Inflate each obstacle
    for obs_r, obs_c in obstacles:
        for dr in range(-inflate_r, inflate_r + 1):
            for dc in range(-inflate_c, inflate_c + 1):
                nr, nc = obs_r + dr, obs_c + dc

                # Check bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Only inflate free cells
                    if inflated_grid[nr][nc] == 0:
                        inflated_grid[nr][nc] = OBSTACLE

    return inflated_grid


def check_robot_collision(grid, position, robot_width=None, robot_height=None):
    """
    Checks if a robot at the given position would collide with obstacles.

    Args:
        grid: 2D list representing the occupancy grid
        position: (row, col) tuple - center of the robot
        robot_width: width of robot in grid cells
        robot_height: height of robot in grid cells

    Returns:
        True if collision detected, False otherwise
    """
    if robot_width is None:
        robot_width = ROBOT_WIDTH
    if robot_height is None:
        robot_height = ROBOT_HEIGHT

    r, c = position
    rows = len(grid)
    cols = len(grid[0])

    # Calculate robot bounds
    half_h = robot_height // 2
    half_w = robot_width // 2

    # Check all cells the robot occupies
    for dr in range(-half_h, half_h + 1):
        for dc in range(-half_w, half_w + 1):
            nr, nc = r + dr, c + dc

            # Out of bounds = collision
            if not (0 <= nr < rows and 0 <= nc < cols):
                return True

            # Obstacle = collision
            if grid[nr][nc] == OBSTACLE:
                return True

    return False
