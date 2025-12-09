# This file holds all parameters in one place so you can tune the behavior
# General settings for the planner

# Map characters
FREE = 0
OBSTACLE = 1
START = 2
GOAL = 3

# Potential field parameters
ATTRACTIVE_GAIN = 1.0     # strength of goal attraction
REPULSIVE_GAIN = 50.0     # strength of obstacle repulsion
OBSTACLE_INFLUENCE = 3    # how many grid cells around an obstacle repel the robot

# Robot settings
ROBOT_WIDTH = 2           # in grid cells (simple inflation model)
ROBOT_HEIGHT = 2

# Visualization settings
SHOW_POTENTIAL = True