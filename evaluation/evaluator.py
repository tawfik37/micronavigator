import os
import json
import csv
from map.grid_loader import load_grid
from planner.potential_field import compute_potential_field
from planner.path_extractor import extract_path
from planner.statistics import PlanningStatistics
from robot.shape_handler import inflate_obstacles
from visualization.draw_path import draw_path
from config.settings import ROBOT_WIDTH, ROBOT_HEIGHT


class PerformanceEvaluator:
    """
    Evaluates the planner's performance across multiple scenarios.
    """

    def __init__(self):
        self.results = []

    def run_scenario(self, map_file, scenario_name, robot_width=None, robot_height=None):
        """
        Runs planning on a single scenario and collects statistics.

        Args:
            map_file: path to map file
            scenario_name: descriptive name for this scenario
            robot_width: override robot width (optional)
            robot_height: override robot height (optional)

        Returns:
            PlanningStatistics object with results
        """
        if robot_width is None:
            robot_width = ROBOT_WIDTH
        if robot_height is None:
            robot_height = ROBOT_HEIGHT

        print(f"\n{'='*60}")
        print(f"Running Scenario: {scenario_name}")
        print(f"Map File: {map_file}")
        print(f"Robot Size: {robot_height} x {robot_width}")
        print(f"{'='*60}")

        stats = PlanningStatistics()

        try:
            # Load the map
            grid, start, goal = load_grid(map_file)
            stats.set_map_info(grid, robot_width, robot_height)

            # Inflate obstacles for robot shape
            inflated_grid = inflate_obstacles(grid, robot_width, robot_height)

            # Start timing
            stats.start_timer()

            # Compute potential field
            potential = compute_potential_field(inflated_grid, goal)

            # Extract path
            path = extract_path(potential, start, goal, statistics=stats)

            # Stop timing
            stats.stop_timer()

            # Check if we reached the goal
            if path and path[-1] == goal:
                stats.set_success(True)
                stats.set_path_info(path)

                # Save visualization
                output_file = f"evaluation/{scenario_name}_path.png"
                os.makedirs("evaluation", exist_ok=True)
                draw_path(grid, path, output_file)
                print(f"Visualization saved: {output_file}")

            else:
                stats.set_success(False, "Path did not reach goal")

        except Exception as e:
            stats.stop_timer()
            stats.set_success(False, str(e))
            print(f"ERROR: {e}")

        # Print statistics
        print(stats.get_summary())

        # Store results
        result = {
            "scenario_name": scenario_name,
            "map_file": map_file,
            **stats.get_dict()
        }
        self.results.append(result)

        return stats

    def run_all_scenarios(self, scenario_configs):
        """
        Runs multiple scenarios in batch.

        Args:
            scenario_configs: list of dicts with keys: 'name', 'map_file', 'robot_width', 'robot_height'
        """
        self.results = []

        for config in scenario_configs:
            self.run_scenario(
                map_file=config['map_file'],
                scenario_name=config['name'],
                robot_width=config.get('robot_width'),
                robot_height=config.get('robot_height')
            )

    def save_results(self, output_dir="evaluation"):
        """
        Saves evaluation results to JSON and CSV files.
        """
        os.makedirs(output_dir, exist_ok=True)

        # Save as JSON
        json_file = os.path.join(output_dir, "results.json")
        with open(json_file, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to: {json_file}")

        # Save as CSV
        csv_file = os.path.join(output_dir, "results.csv")
        if self.results:
            with open(csv_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                writer.writeheader()
                writer.writerows(self.results)
            print(f"Results saved to: {csv_file}")

    def print_comparison_table(self):
        """
        Prints a comparison table of all scenarios.
        """
        if not self.results:
            print("No results to display.")
            return

        print("\n" + "="*100)
        print("PERFORMANCE COMPARISON TABLE")
        print("="*100)

        # Header
        header = f"{'Scenario':<25} {'Status':<10} {'Time (ms)':<12} {'Nodes':<10} {'Path Len':<12} {'Path Cost':<12}"
        print(header)
        print("-"*100)

        # Data rows
        for result in self.results:
            status = "SUCCESS" if result["success"] else "FAILED"
            time_ms = f"{result['planning_time_ms']:.2f}"
            nodes = result['nodes_explored']
            path_len = result['path_length'] if result['success'] else "N/A"
            path_cost = f"{result['path_cost']:.2f}" if result['success'] else "N/A"

            row = f"{result['scenario_name']:<25} {status:<10} {time_ms:<12} {nodes:<10} {str(path_len):<12} {str(path_cost):<12}"
            print(row)

        print("="*100)

    def get_summary_statistics(self):
        """
        Calculates overall summary statistics.
        """
        if not self.results:
            return None

        total = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        failed = total - successful

        avg_time = sum(r['planning_time_ms'] for r in self.results) / total
        avg_nodes = sum(r['nodes_explored'] for r in self.results) / total

        successful_results = [r for r in self.results if r['success']]
        if successful_results:
            avg_path_length = sum(r['path_length'] for r in successful_results) / len(successful_results)
            avg_path_cost = sum(r['path_cost'] for r in successful_results) / len(successful_results)
        else:
            avg_path_length = 0
            avg_path_cost = 0

        summary = {
            "total_scenarios": total,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "avg_planning_time_ms": avg_time,
            "avg_nodes_explored": avg_nodes,
            "avg_path_length": avg_path_length,
            "avg_path_cost": avg_path_cost,
        }

        return summary

    def print_summary(self):
        """
        Prints overall summary of evaluation.
        """
        summary = self.get_summary_statistics()

        if not summary:
            print("No results to summarize.")
            return

        print("\n" + "="*60)
        print("OVERALL SUMMARY")
        print("="*60)
        print(f"Total Scenarios: {summary['total_scenarios']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print()
        print(f"Average Planning Time: {summary['avg_planning_time_ms']:.2f} ms")
        print(f"Average Nodes Explored: {summary['avg_nodes_explored']:.1f}")
        if summary['successful'] > 0:
            print(f"Average Path Length: {summary['avg_path_length']:.2f} steps")
            print(f"Average Path Cost: {summary['avg_path_cost']:.2f} units")
        print("="*60)
