import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from config.settings import FREE, OBSTACLE, START, GOAL

def draw_path(grid, path, output_file="path_output.png", potential=None):
    """
    Creates a professional, publication-ready visualization of path planning results.
    """
    if not path:
        return

    # --- 1. Professional Color Palette ---
    COLOR_BG       = '#FFFFFF'
    COLOR_OBS      = '#2C3E50'  # Darker, more professional gray-blue
    COLOR_START    = '#27AE60'  # Professional green
    COLOR_GOAL     = '#E74C3C'  # Professional red
    COLOR_PATH     = '#3498DB'  # Clean blue
    COLOR_GRID     = '#ECF0F1'  # Very subtle grid
    COLOR_TEXT     = '#2C3E50'  # Professional dark text

    # --- 2. Calculate Optimal Figure Size ---
    rows = len(grid)
    cols = len(grid[0])
    aspect_ratio = cols / rows

    # Base size on grid dimensions for proper aspect ratio
    # Use cell size to ensure proper scaling
    cell_size = 0.6  # inches per cell
    fig_width = cols * cell_size + 1.5  # Add margins
    fig_height = rows * cell_size + 2.5  # Add space for title/legend

    # Clamp to reasonable sizes
    fig_width = max(8, min(fig_width, 16))
    fig_height = max(6, min(fig_height, 14))

    # --- 3. Setup Figure with High DPI ---
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=300)
    fig.patch.set_facecolor(COLOR_BG)

    # Dynamic margins based on aspect ratio
    if aspect_ratio > 2.5:  # Very wide (like corridor)
        plt.subplots_adjust(left=0.05, right=0.95, top=0.82, bottom=0.15)
    elif aspect_ratio < 0.5:  # Very tall
        plt.subplots_adjust(left=0.12, right=0.88, top=0.90, bottom=0.10)
    else:  # Normal aspect ratio
        plt.subplots_adjust(left=0.08, right=0.92, top=0.88, bottom=0.12)

    # --- 4. Draw Background ---
    if potential:
        flat_pot = [v for row in potential for v in row if v != float('inf')]
        max_val = max(flat_pot) if flat_pot else 100

        plot_potential = np.array([
            [min(cell, max_val) for cell in row]
            for row in potential
        ])

        heatmap = ax.imshow(
            plot_potential,
            cmap='YlOrRd',
            interpolation='bilinear',
            alpha=0.3,
            extent=[-0.5, cols - 0.5, rows - 0.5, -0.5],
            aspect='equal'
        )

        cbar = plt.colorbar(heatmap, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Potential Cost', rotation=270, labelpad=20,
                      fontsize=10, color=COLOR_TEXT)
        cbar.ax.tick_params(labelsize=9)

    # --- 5. Draw Grid Background ---
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(rows - 0.5, -0.5)
    ax.set_aspect('equal')
    ax.set_facecolor('#FAFAFA')

    # --- 6. Draw Obstacles with Better Styling ---
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == OBSTACLE:
                rect = mpatches.Rectangle(
                    (c - 0.5, r - 0.5), 1, 1,
                    linewidth=0.5,
                    edgecolor='#1A252F',
                    facecolor=COLOR_OBS,
                    alpha=0.95
                )
                ax.add_patch(rect)

    # --- 7. Draw Path with Professional Styling ---
    y_coords = [p[0] for p in path]
    x_coords = [p[1] for p in path]

    # Path line with glow effect
    ax.plot(x_coords, y_coords,
            color=COLOR_PATH,
            linewidth=3.5,
            alpha=0.85,
            solid_capstyle='round',
            solid_joinstyle='round',
            zorder=8)

    # Add subtle glow
    ax.plot(x_coords, y_coords,
            color=COLOR_PATH,
            linewidth=6,
            alpha=0.15,
            solid_capstyle='round',
            zorder=7)

    # Start marker
    ax.scatter([x_coords[0]], [y_coords[0]],
               color=COLOR_START,
               s=300,
               marker='o',
               edgecolors='white',
               linewidth=2.5,
               zorder=10,
               alpha=0.95)

    # Goal marker
    ax.scatter([x_coords[-1]], [y_coords[-1]],
               color=COLOR_GOAL,
               marker='*',
               s=450,
               edgecolors='white',
               linewidth=2.5,
               zorder=10,
               alpha=0.95)

    # --- 8. Grid Styling ---
    # Set grid at cell boundaries (offset by 0.5)
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=False)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=False)
    ax.grid(which='major', color=COLOR_GRID, linewidth=0.5, alpha=0.7, zorder=1)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    # Add frame
    for spine in ax.spines.values():
        spine.set_edgecolor('#BDC3C7')
        spine.set_linewidth(1.5)

    # --- 9. Title and Info ---
    clean_name = output_file.split("/")[-1].replace(".png", "").replace("_", " ").title()
    path_len = len(path)

    # Adjust title positions based on aspect ratio with better spacing
    if aspect_ratio > 2.5:  # Very wide - needs more vertical separation
        title_y = 0.96
        subtitle_y = 0.89
        title_size = 15
        subtitle_size = 9
    elif aspect_ratio < 0.5:  # Very tall
        title_y = 0.97
        subtitle_y = 0.935
        title_size = 16
        subtitle_size = 10
    else:  # Normal
        title_y = 0.965
        subtitle_y = 0.915
        title_size = 16
        subtitle_size = 10

    # Main title
    fig.suptitle(
        f"{clean_name}",
        fontsize=title_size,
        fontweight='600',
        color=COLOR_TEXT,
        y=title_y,
        family='sans-serif'
    )

    # Subtitle with stats
    subtitle = f"Path Length: {path_len} steps  |  Grid Size: {cols}×{rows}"
    fig.text(
        0.5, subtitle_y,
        subtitle,
        fontsize=subtitle_size,
        color='#7F8C8D',
        ha='center',
        family='sans-serif',
        weight='normal'
    )

    # --- 10. Professional Legend ---
    legend_elements = [
        mpatches.Patch(color=COLOR_START, label='Start', edgecolor='white', linewidth=1),
        mpatches.Patch(color=COLOR_GOAL, label='Goal', edgecolor='white', linewidth=1),
        mpatches.Patch(color=COLOR_OBS, label='Obstacle', edgecolor='#1A252F', linewidth=0.5),
        plt.Line2D([0], [0], color=COLOR_PATH, lw=3, label='Planned Path'),
    ]

    # Adjust legend position based on aspect ratio
    if aspect_ratio > 2.5:  # Very wide - legend needs more space
        legend_y = -0.12
        legend_fontsize = 8
    else:
        legend_y = -0.08
        legend_fontsize = 9

    legend = ax.legend(
        handles=legend_elements,
        loc='upper center',
        bbox_to_anchor=(0.5, legend_y),
        ncol=4,
        fontsize=legend_fontsize,
        frameon=True,
        shadow=False,
        facecolor='white',
        edgecolor='#BDC3C7',
        framealpha=0.95,
        columnspacing=1.5,
        handletextpad=0.5
    )
    legend.get_frame().set_linewidth(1.5)

    # --- 11. Save with High Quality ---
    try:
        plt.savefig(
            output_file,
            dpi=300,
            bbox_inches='tight',
            pad_inches=0.2,
            facecolor=COLOR_BG,
            edgecolor='none'
        )
    except Exception as e:
        print(f"Error saving PNG: {e}")

    plt.close()