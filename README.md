# MicroNavigator

A hybrid path planning system combining A* search with potential field methods for rectangular robots navigating grid-based environments.

## Overview

MicroNavigator implements a unique hybrid approach that combines the completeness guarantees of A* search with the smooth navigation capabilities of potential field methods. The system uses potential fields as a heuristic for A*, resulting in efficient pathfinding with obstacle avoidance properties.

## Key Features

- **Hybrid A* + Potential Field Algorithm**: Combines A* completeness with potential field smoothness
- **Algorithm Comparison Tools**: Compare hybrid approach against pure A* and pure gradient descent
- **Variable Robot Size Support**: Handles rectangular robots with automatic obstacle inflation
- **Comprehensive Evaluation System**: Benchmark performance across multiple scenarios
- **Professional Visualizations**: High-quality 300 DPI path visualization outputs
- **Performance Metrics**: Track planning time, nodes explored, path length, and success rate

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
micronavigator/
├── config/              # Configuration settings and parameters
├── map/                 # Map files and grid loading utilities
├── planner/             # Path planning algorithms
│   ├── path_extractor.py       # Hybrid A* + Potential Field
│   ├── pure_astar.py           # Pure A* for comparison
│   └── pure_gradient.py        # Pure gradient descent for comparison
├── robot/               # Robot shape handling and path export
├── visualization/       # Visualization and comparison tools
│   ├── draw_path.py            # Path visualization
│   ├── algorithm_comparison.py # Algorithm comparison charts
│   └── comparison_charts.py    # Performance comparison charts
├── evaluation/          # Performance evaluation framework
└── run_scenarios.py     # Main evaluation script
```

## Usage

### Running Evaluation Scenarios

Run the comprehensive evaluation across all test scenarios:

```bash
python3 run_scenarios.py
```

This executes 8 different scenarios testing:
- Basic open maps
- Long corridors
- Complex mazes
- Cluttered environments
- Narrow passages
- Large-scale maps
- Variable robot sizes (1x1 to 5x5 cells)

Results are saved to `evaluation_results/` including:
- Path visualizations (PNG)
- Performance statistics (TXT)
- Comparison charts

### Running Algorithm Comparison

Compare the hybrid approach against pure A* and pure gradient descent:

```bash
python3 full_algorithm_comparison.py
```

This generates:
- Side-by-side algorithm visualizations
- Performance comparison charts
- Aggregate statistics across scenarios

## Algorithm Details

### Hybrid A* + Potential Field

The core algorithm uses potential fields as the heuristic in A* search:

```
f(n) = g(n) + U(n)
```

Where:
- `g(n)` is the actual cost from start to node n
- `U(n)` is the potential field value (attractive + repulsive)

**Potential Field Components:**
- Attractive Potential: Draws robot toward goal
- Repulsive Potential: Pushes robot away from obstacles

This hybrid approach provides:
- **Completeness**: Guaranteed to find a path if one exists (from A*)
- **Smoothness**: Natural obstacle avoidance behavior (from potential fields)
- **Efficiency**: Guided search reduces exploration (from informed heuristic)

### Comparison Algorithms

- **Pure A***: Standard A* with Manhattan distance heuristic
- **Pure Gradient Descent**: Follows steepest descent of potential field

## Configuration

Edit `config/settings.py` to customize:
- Robot dimensions
- Potential field parameters (attractive/repulsive coefficients)
- Visualization options
- Obstacle inflation radius

## Results

The evaluation system measures:
- **Planning Time**: Computation time in milliseconds
- **Path Length**: Total path distance in grid cells
- **Nodes Explored**: Number of nodes expanded during search
- **Success Rate**: Percentage of scenarios solved successfully

## Output Files

Generated files in `evaluation_results/`:
- `scenario_X_path.png` - Path visualizations (300 DPI)
- `scenario_X_stats.txt` - Performance statistics
- `comparison_*.png` - Algorithm comparison charts
- `aggregate_statistics.txt` - Overall performance summary

## Map Format

Maps are defined in text files using:
- `0` - Free space
- `1` - Obstacle
- `S` - Start position
- `G` - Goal position

Example:
```
0 0 0 0 0
0 1 1 1 0
S 0 0 0 G
0 1 1 1 0
0 0 0 0 0
```

## Authors

Micro-Navigator Path Planning Project

## License

Academic Project
