import json
import subprocess
import os
import asyncio
import matplotlib.pyplot as plt
import numpy as np
import argparse

def read_last_json_element(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if data:
                last_element = data[-1]
                last_element['element_count'] = len(data) - 1
                return last_element
            else:
                return None

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def visualize(output_path):
    outputs = os.listdir(output_path)

    results = {}
    win_counts = {}

    for output in outputs:
        last_element = read_last_json_element(os.path.join(output_path, output))

        if last_element is None:
            continue

        # Get points for each player
        points = {}
        for index, player in enumerate(last_element['players']):
            points[f'player_{index}'] = player['points']

        # Determine the winner (player with highest points)
        max_points = -1
        winner = None
        for player_id, score in points.items():
            if score > max_points:
                max_points = score
                winner = player_id

        # Store the radius and increment win count for the winner
        radius = last_element['map']['radius']
        results.setdefault(radius, []).append(points)

        # Initialize win counts for this radius if not already done
        if radius not in win_counts:
            win_counts[radius] = {}
            for i in range(len(last_element['players'])):
                win_counts[radius][f'player_{i}'] = 0

        # Increment win count for the winner
        if winner:
            win_counts[radius][winner] += 1

    # Create a bar chart showing wins by radius for each player
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='#f8f9fa')
    ax.set_facecolor('#f0f0f5')

    # Sort radii for consistent visualization
    sorted_radii = sorted(win_counts.keys())

    # Set width of bars and positions
    bar_width = 0.2
    index = np.arange(len(sorted_radii) + 1)  # +1 for the total column

    # Calculate totals for each player across all radii
    total_wins = {f'player_{i}': 0 for i in range(3)}
    for radius in sorted_radii:
        for i in range(3):
            total_wins[f'player_{i}'] += win_counts[radius].get(f'player_{i}', 0)

    # Beautiful color palette
    colors = ['#3498db', '#2ecc71', '#e74c3c']

    # Create bars for each player
    for i in range(3):  # Assuming 3 players
        player_wins = [win_counts[radius].get(f'player_{i}', 0) for radius in sorted_radii]
        # Add the total for this player
        player_wins.append(total_wins[f'player_{i}'])

        ax.bar(index + i*bar_width, player_wins, bar_width,
               label=f'Player {i}', color=colors[i], alpha=0.8,
               edgecolor='white', linewidth=0.7)

        # Add text labels for zero wins to make them visible
        for j, wins in enumerate(player_wins):
            if wins == 0:
                ax.text(j + i*bar_width, 0.1, '0',
                        ha='center', va='bottom',
                        fontweight='bold', color='#d35400')
            else:
                ax.text(j + i*bar_width, wins, str(wins),
                        ha='center', va='bottom',
                        fontweight='bold', color='#2c3e50')

    # Labels and title
    ax.set_xlabel('Map Radius', fontsize=12, fontweight='bold', color='#2c3e50')
    ax.set_ylabel('Number of Wins', fontsize=12, fontweight='bold', color='#2c3e50')
    ax.set_title('Number of Wins by Player for Each Map Radius',
                fontsize=14, fontweight='bold', color='#2c3e50')
    ax.set_xticks(index + bar_width)

    # Add "Total" column
    x_labels = [str(r) for r in sorted_radii] + ['Total']
    ax.set_xticklabels(x_labels, fontweight='bold')

    # Highlight the total column with subtle background
    ax.axvspan(len(sorted_radii)-0.5, len(sorted_radii)+0.5, color='#ecf0f1', alpha=0.3)

    # Style the grid
    ax.grid(True, linestyle='--', alpha=0.3)

    # Style the legend
    ax.legend(frameon=True, fancybox=True, shadow=True, fontsize=10)

    # Style the spines
    for spine in ax.spines.values():
        spine.set_color('#bdc3c7')

    # Save the chart with higher DPI for better quality
    plt.tight_layout()
    plt.savefig('player_wins_by_radius.png', dpi=300)
    plt.close()

def parse_args():
    """Parse commmand line arguments"""
    parser = argparse.ArgumentParser(description="Evaluate bot on test map")
    parser.add_argument("--map", default="maps", help="Path to the map JSON folder")
    parser.add_argument("--agents", nargs=3, required=True, help="Paths to three agent executable")
    parser.add_argument("--output", default="./output/json", help="Output path for game logs")
    return parser.parse_args()

def run_test(map_path, map, agents, output_path):
    agents_str = " ".join(agents)
    cmd = f"python main.py --map {map_path}/{map} --agents {agents_str} --output {output_path}/{map[:-5]}.json"
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True
    )
    stdout, stderr = process.communicate()
    return stdout, stderr

def run_map_test(args_tuple):
    map_path, map_file, agents, output_path = args_tuple
    return run_test(map_path, map_file, agents, output_path)

def main(args):
    maps = os.listdir(args.map)

    from concurrent.futures import ThreadPoolExecutor

    # Create arguments for each map test
    map_args = [(args.map, map_file, args.agents, args.output) for map_file in maps]

    # Use ThreadPoolExecutor to run tests in parallel
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(run_map_test, map_args))

if __name__ == "__main__":
    args = parse_args()
    main(args)
    visualize(args.output)
