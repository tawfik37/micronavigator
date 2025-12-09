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

```bash
python3 main.py
```

## ⚙️ Configuration

Edit `config/settings.py` to adjust:
-  Robot dimensions (ROBOT_WIDTH, ROBOT_HEIGHT)
- Potential field parameters
- Visualization options
