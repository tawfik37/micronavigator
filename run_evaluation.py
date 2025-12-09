"""
Performance Evaluation Script

This script evaluates the micro-navigator planner across multiple scenarios
with different map configurations and robot sizes.
"""

import matplotlib
matplotlib.use("Agg")

from evaluation.evaluator import PerformanceEvaluator


def main():
    evaluator = PerformanceEvaluator()

    # Define all test scenarios
    scenarios = [
        {
            "name": "Scenario 1: Simple",
            "map_file": "map/scenario1_simple.txt",
            "robot_width": 1,
            "robot_height": 1,
        },
        {
            "name": "Scenario 2: Corridor",
            "map_file": "map/scenario2_corridor.txt",
            "robot_width": 1,
            "robot_height": 1,
        },
        {
            "name": "Scenario 3: Maze",
            "map_file": "map/scenario3_maze.txt",
            "robot_width": 1,
            "robot_height": 1,
        },
        {
            "name": "Scenario 4: Cluttered",
            "map_file": "map/scenario4_cluttered.txt",
            "robot_width": 1,
            "robot_height": 1,
        },
        {
            "name": "Scenario 5: Narrow",
            "map_file": "map/scenario5_narrow.txt",
            "robot_width": 1,
            "robot_height": 1,
        },
        {
            "name": "Scenario 6: Large",
            "map_file": "map/scenario6_large.txt",
            "robot_width": 1,
            "robot_height": 1,
        },
        # Test with larger robot size
        {
            "name": "Scenario 3: Maze (2x2 Robot)",
            "map_file": "map/scenario3_maze.txt",
            "robot_width": 2,
            "robot_height": 2,
        },
        {
            "name": "Scenario 4: Cluttered (2x2 Robot)",
            "map_file": "map/scenario4_cluttered.txt",
            "robot_width": 2,
            "robot_height": 2,
        },
    ]

    print("\n" + "="*70)
    print(" MICRO-NAVIGATOR PERFORMANCE EVALUATION")
    print("="*70)
    print(f"Total scenarios to evaluate: {len(scenarios)}")
    print("="*70)

    # Run all scenarios
    evaluator.run_all_scenarios(scenarios)

    # Print comparison table
    evaluator.print_comparison_table()

    # Print overall summary
    evaluator.print_summary()

    # Save results
    evaluator.save_results()

    print("\n" + "="*70)
    print(" EVALUATION COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
