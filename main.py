import matplotlib
matplotlib.use("Agg")

from map.grid_loader import load_grid
from planner.potential_field import compute_potential_field
from planner.path_extractor import extract_path
from planner.statistics import PlanningStatistics
from visualization.draw_map import draw_map
from visualization.draw_path import draw_path
from robot.exporter import export_path
from robot.shape_handler import inflate_obstacles
from config.settings import ROBOT_WIDTH, ROBOT_HEIGHT

def main():
    print("\n" + "="*60)
    print(" MICRO-NAVIGATOR - SINGLE SCENARIO RUN")
    print("="*60)

    # Initialize statistics tracker
    stats = PlanningStatistics()

    # 1) Load the map
    grid, start, goal = load_grid("map/example_map.txt")
    print(f"Start: {start}, Goal: {goal}")
    print(f"Robot Size: {ROBOT_HEIGHT} x {ROBOT_WIDTH} cells")

    # Set map info for statistics
    stats.set_map_info(grid, ROBOT_WIDTH, ROBOT_HEIGHT)

    # 2) Show the map
    draw_map(grid)

    # 3) Inflate obstacles to account for robot shape
    print("\nInflating obstacles for robot shape...")
    inflated_grid = inflate_obstacles(grid, ROBOT_WIDTH, ROBOT_HEIGHT)

    # 4) Compute potential field
    print("Computing potential field...")
    stats.start_timer()
    potential = compute_potential_field(inflated_grid, goal)

    # 5) Extract path
    print("Extracting path...")
    path = extract_path(potential, start, goal, statistics=stats)
    stats.stop_timer()

    # 6) Check success
    if path and path[-1] == goal:
        stats.set_success(True)
        stats.set_path_info(path)
        print(f"Path found! Length: {len(path)} steps")
    else:
        stats.set_success(False, "Did not reach goal")
        print("Warning: Path did not reach goal")

    # 7) Visualize path
    draw_path(grid, path)
    print("Path visualization saved to path_output.png")

    # 8) Export path for the robot
    export_path(path, "robot/path_output.csv")
    print("Path exported to robot/path_output.csv")

    # 9) Print statistics
    print("\n" + stats.get_summary())

if __name__ == "__main__":
    main()
