# 🤖 Micro-Navigator

A potential field-based path planning system for rectangular robots navigating grid-based environments.

## ✨ Features

- 🧭 Potential field path planning algorithm
- 📏 Variable robot size support with obstacle inflation
- 📊 Path visualization and statistics
- 💾 CSV export for robot execution

## 📁 Structure

- `config/` - ⚙️ Configuration settings
- `map/` - 🗺️ Map loading utilities
- `planner/` - 🎯 Path planning algorithms
- `robot/` - 🤖 Robot shape handling and path export
- `visualization/` - 🎨 Map and path visualization
- `evaluation/` - 📈 Performance evaluation tools

## 🚀 Usage

### Running Path Planning

```bash
python3 main.py
```

### Running Evaluation

```bash
python3 run_evaluation.py
```

The evaluation system benchmarks the path planning algorithm performance across multiple scenarios:
- Tests different robot sizes (1x1 to 5x5 grid cells)
- Evaluates various map configurations
- Measures key metrics: path length, computation time, and success rate
- Generates comprehensive visualizations and statistics
- Outputs results to `evaluation/results/` directory

## ⚙️ Configuration

Edit `config/settings.py` to adjust:
-  Robot dimensions (ROBOT_WIDTH, ROBOT_HEIGHT)
- Potential field parameters
- Visualization options
