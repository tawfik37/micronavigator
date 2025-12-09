import time
import math

class PlanningStatistics:
    """
    Tracks and stores statistics during the planning process.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all statistics to initial values."""
        self.start_time = None
        self.end_time = None
        self.planning_time = 0.0

        self.nodes_explored = 0
        self.path_length = 0
        self.path_cost = 0.0

        self.success = False
        self.failure_reason = None

        self.map_size = (0, 0)
        self.num_obstacles = 0
        self.robot_size = (0, 0)

    def start_timer(self):
        """Start the planning timer."""
        self.start_time = time.time()

    def stop_timer(self):
        """Stop the planning timer and calculate elapsed time."""
        self.end_time = time.time()
        if self.start_time:
            self.planning_time = self.end_time - self.start_time

    def set_map_info(self, grid, robot_width, robot_height):
        """Store map-related information."""
        self.map_size = (len(grid), len(grid[0]) if grid else 0)

        # Count obstacles
        self.num_obstacles = sum(row.count(1) for row in grid)

        self.robot_size = (robot_height, robot_width)

    def set_path_info(self, path):
        """Calculate and store path-related statistics."""
        self.path_length = len(path)

        # Calculate path cost (accounting for diagonal moves)
        self.path_cost = 0.0
        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i + 1]

            # Euclidean distance between consecutive points
            dist = math.sqrt((r2 - r1) ** 2 + (c2 - c1) ** 2)
            self.path_cost += dist

    def set_success(self, success, failure_reason=None):
        """Mark planning as successful or failed."""
        self.success = success
        self.failure_reason = failure_reason

    def get_summary(self):
        """
        Returns a formatted string summary of all statistics.
        """
        lines = []
        lines.append("=" * 50)
        lines.append("PLANNING STATISTICS")
        lines.append("=" * 50)

        lines.append(f"Status: {'SUCCESS' if self.success else 'FAILED'}")
        if not self.success and self.failure_reason:
            lines.append(f"Failure Reason: {self.failure_reason}")

        lines.append("")
        lines.append("Map Information:")
        lines.append(f"  - Map Size: {self.map_size[0]} x {self.map_size[1]} = {self.map_size[0] * self.map_size[1]} cells")
        lines.append(f"  - Number of Obstacles: {self.num_obstacles}")
        lines.append(f"  - Robot Size: {self.robot_size[0]} x {self.robot_size[1]} cells")

        lines.append("")
        lines.append("Planning Performance:")
        lines.append(f"  - Planning Time: {self.planning_time * 1000:.2f} ms")
        lines.append(f"  - Nodes Explored: {self.nodes_explored}")

        if self.success:
            lines.append("")
            lines.append("Path Quality:")
            lines.append(f"  - Path Length: {self.path_length} steps")
            lines.append(f"  - Path Cost: {self.path_cost:.2f} units")
            if self.path_length > 0:
                lines.append(f"  - Average Step Cost: {self.path_cost / self.path_length:.2f} units")

        lines.append("=" * 50)

        return "\n".join(lines)

    def get_dict(self):
        """
        Returns statistics as a dictionary for easy export.
        """
        return {
            "success": self.success,
            "failure_reason": self.failure_reason,
            "planning_time_ms": self.planning_time * 1000,
            "map_rows": self.map_size[0],
            "map_cols": self.map_size[1],
            "num_obstacles": self.num_obstacles,
            "robot_width": self.robot_size[1],
            "robot_height": self.robot_size[0],
            "nodes_explored": self.nodes_explored,
            "path_length": self.path_length,
            "path_cost": self.path_cost,
        }
