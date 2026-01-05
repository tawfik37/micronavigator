import os
import json
import csv
from map.grid_loader import load_grid
from planner.potential_field import compute_potential_field
from planner.path_extractor import extract_path
from planner.statistics import PlanningStatistics
from robot.shape_handler import inflate_obstacles
from visualization.draw_path import draw_path
from visualization.animate_path import animate_path
from visualization.comparison_charts import create_comparison_charts
from visualization.draw_potential_3d import draw_potential_3d, draw_potential_3d_interactive
from config.settings import ROBOT_WIDTH, ROBOT_HEIGHT

# Define the single folder where everything will be saved
OUTPUT_DIR = "evaluation_results"

class PerformanceEvaluator:
    """
    Evaluates the planner's performance across multiple scenarios.
    """

    def __init__(self):
        self.results = []
        # Create the output directory immediately
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def run_scenario(self, map_file, scenario_name, robot_width=None, robot_height=None):
        """
        Runs planning on a single scenario and collects statistics.
        """
        if robot_width is None:
            robot_width = ROBOT_WIDTH
        if robot_height is None:
            robot_height = ROBOT_HEIGHT

        print(f"\n{'='*60}")
        print(f"Running Scenario: {scenario_name}")
        print(f"Map File: {map_file}")
        print(f"{'='*60}")

        stats = PlanningStatistics()

        try:
            # Load and Inflate
            grid, start, goal = load_grid(map_file)
            stats.set_map_info(grid, robot_width, robot_height)
            inflated_grid = inflate_obstacles(grid, robot_width, robot_height)

            # Plan
            stats.start_timer()
            potential = compute_potential_field(inflated_grid, goal)
            path = extract_path(potential, start, goal, statistics=stats)
            stats.stop_timer()

            # Check Success
            if path and path[-1] == goal:
                stats.set_success(True)
                stats.set_path_info(path)

                # --- NEW: Generate Clean Filename ---
                # Converts "Scenario 1: Simple" -> "scenario_1_simple"
                safe_name = scenario_name.replace(":", "").replace(" ", "_").lower()
                
                # --- NEW: Save PNG and GIF ---
                png_file = os.path.join(OUTPUT_DIR, f"{safe_name}.png")
                gif_file = os.path.join(OUTPUT_DIR, f"{safe_name}.gif")

                print(f"Generating visualizations in {OUTPUT_DIR}/...")
                draw_path(grid, path, png_file)
                animate_path(grid, path, gif_file)
                print(f"Saved: {safe_name}.gif")

            else:
                stats.set_success(False, "Path did not reach goal")

        except Exception as e:
            stats.stop_timer()
            stats.set_success(False, str(e))
            print(f"ERROR: {e}")

        # Store results
        result = {
            "scenario_name": scenario_name,
            "map_file": map_file,
            **stats.get_dict()
        }
        self.results.append(result)
        return stats

    def run_all_scenarios(self, scenario_configs):
        self.results = []
        for config in scenario_configs:
            self.run_scenario(
                map_file=config['map_file'],
                scenario_name=config['name'],
                robot_width=config.get('robot_width'),
                robot_height=config.get('robot_height')
            )

    def save_results(self):
        """
        Saves statistics to JSON and CSV in the output folder.
        Also generates comparison charts.
        """
        # Save as JSON
        json_file = os.path.join(OUTPUT_DIR, "results.json")
        with open(json_file, "w") as f:
            json.dump(self.results, f, indent=2)

        # Save as CSV
        csv_file = os.path.join(OUTPUT_DIR, "results.csv")
        if self.results:
            with open(csv_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                writer.writeheader()
                writer.writerows(self.results)

        # Generate comparison charts
        print("\nGenerating comparison charts...")
        create_comparison_charts(self.results, OUTPUT_DIR)

        print(f"\nAll results, animations, and comparison charts saved to: /{OUTPUT_DIR}")

    def print_comparison_table(self):
        # (Same as before - keeping this for console output)
        if not self.results: return
        print("\n" + "="*100)
        print("PERFORMANCE COMPARISON TABLE")
        print("="*100)
        header = f"{'Scenario':<30} {'Status':<10} {'Time(ms)':<10} {'Nodes':<8} {'Path':<8}"
        print(header)
        print("-"*100)
        for r in self.results:
            status = "SUCCESS" if r["success"] else "FAILED"
            print(f"{r['scenario_name']:<30} {status:<10} {r['planning_time_ms']:.2f}{'':<6} {r['nodes_explored']:<8} {r['path_length']}")
        print("="*100)

    def print_summary(self):
        # (Same as before)
        pass