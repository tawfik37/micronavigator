import matplotlib.pyplot as plt
import numpy as np
import os


def create_comparison_charts(results, output_dir="evaluation_results"):
    """
    Creates professional comparison charts for all scenarios.

    Args:
        results: List of result dictionaries from PerformanceEvaluator
        output_dir: Directory to save the charts
    """
    if not results:
        print("No results to visualize")
        return

    # Filter successful results
    successful_results = [r for r in results if r['success']]

    if not successful_results:
        print("No successful scenarios to compare")
        return

    # Create comparison charts
    create_planning_time_chart(successful_results, output_dir)
    create_path_length_chart(successful_results, output_dir)
    create_nodes_explored_chart(successful_results, output_dir)
    create_combined_comparison(successful_results, output_dir)

    print(f"\nComparison charts saved to {output_dir}/")


def create_planning_time_chart(results, output_dir):
    """Creates a bar chart comparing planning times across scenarios."""
    scenarios = [r['scenario_name'] for r in results]
    times = [r['planning_time_ms'] for r in results]

    # Professional styling
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # Create bars
    bars = ax.bar(range(len(scenarios)), times, color='#27AE60', alpha=0.8, edgecolor='#1E8449', linewidth=1.5)

    # Add value labels on bars
    for i, (bar, time) in enumerate(zip(bars, times)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{time:.2f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#2C3E50')

    # Styling
    ax.set_xlabel('Scenario', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.set_ylabel('Planning Time (ms)', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.set_title('Planning Time Comparison - Lower is Better', fontsize=14, fontweight='bold', color='#2C3E50', pad=20)
    ax.set_xticks(range(len(scenarios)))
    ax.set_xticklabels([s.replace('Scenario ', '').replace(': ', '\n') for s in scenarios],
                       rotation=45, ha='right', fontsize=9)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    # Frame styling
    for spine in ax.spines.values():
        spine.set_edgecolor('#BDC3C7')
        spine.set_linewidth(1.5)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comparison_planning_time.png'), dpi=300, bbox_inches='tight')
    plt.close()


def create_path_length_chart(results, output_dir):
    """Creates a bar chart comparing path lengths across scenarios."""
    scenarios = [r['scenario_name'] for r in results]
    lengths = [r['path_length'] for r in results]

    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    bars = ax.bar(range(len(scenarios)), lengths, color='#3498DB', alpha=0.8, edgecolor='#2874A6', linewidth=1.5)

    # Add value labels
    for i, (bar, length) in enumerate(zip(bars, lengths)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{length}',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#2C3E50')

    ax.set_xlabel('Scenario', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.set_ylabel('Path Length (Steps)', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.set_title('Path Length Comparison - Lower is Better', fontsize=14, fontweight='bold', color='#2C3E50', pad=20)
    ax.set_xticks(range(len(scenarios)))
    ax.set_xticklabels([s.replace('Scenario ', '').replace(': ', '\n') for s in scenarios],
                       rotation=45, ha='right', fontsize=9)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_edgecolor('#BDC3C7')
        spine.set_linewidth(1.5)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comparison_path_length.png'), dpi=300, bbox_inches='tight')
    plt.close()


def create_nodes_explored_chart(results, output_dir):
    """Creates a bar chart comparing nodes explored across scenarios."""
    scenarios = [r['scenario_name'] for r in results]
    nodes = [r['nodes_explored'] for r in results]

    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    bars = ax.bar(range(len(scenarios)), nodes, color='#E74C3C', alpha=0.8, edgecolor='#C0392B', linewidth=1.5)

    # Add value labels
    for i, (bar, node_count) in enumerate(zip(bars, nodes)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{node_count}',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#2C3E50')

    ax.set_xlabel('Scenario', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.set_ylabel('Nodes Explored', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.set_title('Nodes Explored Comparison - Lower is Better', fontsize=14, fontweight='bold', color='#2C3E50', pad=20)
    ax.set_xticks(range(len(scenarios)))
    ax.set_xticklabels([s.replace('Scenario ', '').replace(': ', '\n') for s in scenarios],
                       rotation=45, ha='right', fontsize=9)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_edgecolor('#BDC3C7')
        spine.set_linewidth(1.5)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comparison_nodes_explored.png'), dpi=300, bbox_inches='tight')
    plt.close()


def create_combined_comparison(results, output_dir):
    """Creates a multi-panel comparison chart with all metrics."""
    scenarios = [r['scenario_name'] for r in results]
    times = [r['planning_time_ms'] for r in results]
    lengths = [r['path_length'] for r in results]
    nodes = [r['nodes_explored'] for r in results]

    # Clean scenario names for display
    clean_names = [s.replace('Scenario ', '').replace(': ', '\n') for s in scenarios]

    # Create figure with 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # Add main title
    fig.suptitle('Micronavigator Performance Comparison',
                 fontsize=18, fontweight='bold', color='#2C3E50', y=0.98)

    # Planning Time
    bars1 = ax1.bar(range(len(scenarios)), times, color='#27AE60', alpha=0.8, edgecolor='#1E8449', linewidth=1.5)
    for bar, time in zip(bars1, times):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height, f'{time:.2f}',
                ha='center', va='bottom', fontsize=8, fontweight='bold', color='#2C3E50')
    ax1.set_xlabel('Scenario', fontsize=11, fontweight='bold', color='#2C3E50')
    ax1.set_ylabel('Time (ms)', fontsize=11, fontweight='bold', color='#2C3E50')
    ax1.set_title('Planning Time (ms) - Lower is Better', fontsize=12, fontweight='bold', color='#2C3E50', pad=10)
    ax1.set_xticks(range(len(scenarios)))
    ax1.set_xticklabels(clean_names, rotation=45, ha='right', fontsize=8)
    ax1.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax1.set_axisbelow(True)

    # Path Length
    bars2 = ax2.bar(range(len(scenarios)), lengths, color='#3498DB', alpha=0.8, edgecolor='#2874A6', linewidth=1.5)
    for bar, length in zip(bars2, lengths):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height, f'{length}',
                ha='center', va='bottom', fontsize=8, fontweight='bold', color='#2C3E50')
    ax2.set_xlabel('Scenario', fontsize=11, fontweight='bold', color='#2C3E50')
    ax2.set_ylabel('Number of Steps', fontsize=11, fontweight='bold', color='#2C3E50')
    ax2.set_title('Path Length (Steps) - Lower is Better', fontsize=12, fontweight='bold', color='#2C3E50', pad=10)
    ax2.set_xticks(range(len(scenarios)))
    ax2.set_xticklabels(clean_names, rotation=45, ha='right', fontsize=8)
    ax2.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax2.set_axisbelow(True)

    # Nodes Explored
    bars3 = ax3.bar(range(len(scenarios)), nodes, color='#E74C3C', alpha=0.8, edgecolor='#C0392B', linewidth=1.5)
    for bar, node_count in zip(bars3, nodes):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height, f'{node_count}',
                ha='center', va='bottom', fontsize=8, fontweight='bold', color='#2C3E50')
    ax3.set_xlabel('Scenario', fontsize=11, fontweight='bold', color='#2C3E50')
    ax3.set_ylabel('Nodes Explored', fontsize=11, fontweight='bold', color='#2C3E50')
    ax3.set_title('Nodes Explored - Lower is Better', fontsize=12, fontweight='bold', color='#2C3E50', pad=10)
    ax3.set_xticks(range(len(scenarios)))
    ax3.set_xticklabels(clean_names, rotation=45, ha='right', fontsize=8)
    ax3.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax3.set_axisbelow(True)

    # Style all spines
    for ax in [ax1, ax2, ax3]:
        for spine in ax.spines.values():
            spine.set_edgecolor('#BDC3C7')
            spine.set_linewidth(1.5)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comparison_all_metrics.png'), dpi=300, bbox_inches='tight')
    plt.close()
