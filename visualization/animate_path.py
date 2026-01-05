import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
from config.settings import FREE, OBSTACLE, START, GOAL

def animate_path(grid, path, output_file="path_animation.gif"):
    """
    Creates a bright, high-visibility GIF animation.
    Theme: "Clean Laboratory" (White background, high contrast).
    """
    if not path:
        return

    # --- 1. Bright & Clear Color Palette ---
    COLOR_BG    = '#FFFFFF'  # White (Free Space)
    COLOR_OBS   = '#34495E'  # Dark Slate Blue (Obstacles) - High Contrast
    COLOR_START = '#2ECC71'  # Emerald Green (Start)
    COLOR_GOAL  = '#E74C3C'  # Alizarin Red (Goal)
    
    COLOR_PATH  = '#3498DB'  # Bright Blue (Path Trace)
    COLOR_ROBOT = '#F1C40F'  # Sun Yellow (Robot)
    
    # Map grid values to colors
    # 0=Free, 1=Obstacle, 2=Start, 3=Goal
    cmap = ListedColormap([COLOR_BG, COLOR_OBS, COLOR_START, COLOR_GOAL])

    # --- 2. Setup Figure ---
    # Use default style (white background) instead of dark_background
    plt.style.use('default') 
    
    fig, ax = plt.subplots(figsize=(10, 8), dpi=100)
    
    # Draw the Grid Map
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=3)
    
    # Add light grey grid lines for structure
    ax.grid(which='major', color='#BDC3C7', linewidth=1, alpha=0.5)
    
    # Remove axis ticks
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Title
    scenario_title = output_file.split("/")[-1].replace(".gif", "").replace("_", " ").title()
    ax.set_title(f"Simulation: {scenario_title}", fontsize=16, fontweight='bold', color='#2C3E50', pad=20)

    # --- 3. The Legend (Updated for Bright Theme) ---
    legend_elements = [
        mpatches.Patch(color=COLOR_START, label='Start'),
        mpatches.Patch(color=COLOR_GOAL, label='Goal'),
        mpatches.Patch(color=COLOR_OBS, label='Obstacle'),
        plt.Line2D([0], [0], color=COLOR_PATH, lw=3, label='Path'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=COLOR_ROBOT, markeredgecolor='black', markersize=10, label='Robot'),
    ]
    
    # Legend with shadow and frame
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05),
              ncol=5, fontsize=11, frameon=True, shadow=True, facecolor='#ECF0F1', edgecolor='#BDC3C7')

    # --- 4. Graphic Elements ---
    path_line, = ax.plot([], [], color=COLOR_PATH, linewidth=3, alpha=0.7)
    
    # Robot: Yellow square with solid black border for visibility
    robot_body, = ax.plot([], [], marker='s', color=COLOR_ROBOT, markersize=16, 
                          markeredgecolor='black', markeredgewidth=2)

    # Status Box: Dark text on light background
    status_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='#2C3E50',
                          fontsize=12, fontweight='bold', 
                          bbox=dict(facecolor='white', alpha=0.9, edgecolor='#BDC3C7', boxstyle='round,pad=0.5'))

    # --- 5. Animation Logic ---
    def init():
        path_line.set_data([], [])
        robot_body.set_data([], [])
        status_text.set_text('')
        return path_line, robot_body, status_text

    def update(frame):
        current_path = path[:frame+1]
        y = [p[0] for p in current_path]
        x = [p[1] for p in current_path]
        
        path_line.set_data(x, y)
        if current_path:
            robot_body.set_data([x[-1]], [y[-1]])
        
        # Step Counter
        percent = int((frame / (len(path)-1)) * 100)
        status_text.set_text(f'Step: {frame}/{len(path)-1} ({percent}%)')
        
        return path_line, robot_body, status_text

    # --- 6. Save (Slower Speed) ---
    plt.tight_layout()
    
    # Interval=200 means 200ms per frame (5 frames per second) -> Much Slower
    ani = FuncAnimation(fig, update, frames=len(path), init_func=init, blit=True, interval=200)
    
    try:
        # Saving at 5 FPS to match the interval
        ani.save(output_file, writer='pillow', fps=5)
    except Exception as e:
        print(f"Error saving GIF: {e}")

    plt.close()