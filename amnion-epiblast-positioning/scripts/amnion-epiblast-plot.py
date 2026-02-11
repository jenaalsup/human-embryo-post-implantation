#!/usr/bin/env python3
"""
Simple plot of amnion vs epiblast nuclei.
Blue = Amnion, Orange = Epiblast
"""

import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Files to process
INPUT_FILES = [
    "17s1z20-segmentation.csv",
    "18s1z14-segmentation.csv",
    "18s2z9-segmentation.csv"
]

def plot_classification(input_csv):
    """Create plot for a single segmentation file."""
    
    # Generate output filename
    output = input_csv.replace('-segmentation.csv', '-amnion-epiblast-plot.png')
    
    # Read nuclei
    nuclei = []
    with open(input_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            nuclei.append({
                'id': len(nuclei) + 1,
                'x': float(row['X']),
                'y': float(row['Y']),
                'is_amnion': row['IsAmnion'].strip().upper() == 'Y'
            })
    
    # Separate by type
    amnion = [n for n in nuclei if n['is_amnion']]
    epiblast = [n for n in nuclei if not n['is_amnion']]
    
    # Calculate center
    center_x = sum(n['x'] for n in nuclei) / len(nuclei)
    center_y = sum(n['y'] for n in nuclei) / len(nuclei)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot amnion (blue)
    if amnion:
        ax.scatter([n['x'] for n in amnion], [n['y'] for n in amnion], 
                  c='#1E88E5', s=300, alpha=0.7, edgecolors='black', 
                  linewidth=2, label='Amnion', zorder=3)
        for n in amnion:
            ax.text(n['x'], n['y'], str(n['id']), fontsize=9, ha='center', 
                   va='center', color='white', fontweight='bold', zorder=4)
    
    # Plot epiblast (orange)
    if epiblast:
        ax.scatter([n['x'] for n in epiblast], [n['y'] for n in epiblast], 
                  c='#FF8C00', s=300, alpha=0.7, edgecolors='black', 
                  linewidth=2, label='Epiblast', zorder=3)
        for n in epiblast:
            ax.text(n['x'], n['y'], str(n['id']), fontsize=9, ha='center', 
                   va='center', color='white', fontweight='bold', zorder=4)
    
    # Plot center
    ax.scatter(center_x, center_y, c='lime', marker='X', s=500, 
              edgecolors='black', linewidth=3, label='Center', zorder=10)
    
    # Draw radial lines
    for n in nuclei:
        ax.plot([center_x, n['x']], [center_y, n['y']], 
               'k-', alpha=0.15, linewidth=0.8, zorder=1)
    
    # Format
    ax.set_xlabel('X (pixels)', fontsize=12)
    ax.set_ylabel('Y (pixels)', fontsize=12)
    ax.set_title(f'Amnion vs Epiblast Classification\n'
                f'Amnion: {len(amnion)} | Epiblast: {len(epiblast)}', 
                fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ {input_csv} -> {output}")
    print(f"  Amnion: {len(amnion)} | Epiblast: {len(epiblast)}")
    
    return len(amnion), len(epiblast)

# Process all files
print("Processing segmentation files...\n")
for csv_file in INPUT_FILES:
    try:
        plot_classification(csv_file)
    except FileNotFoundError:
        print(f"✗ {csv_file} not found, skipping...")
    except Exception as e:
        print(f"✗ Error processing {csv_file}: {e}")

print("\nDone!")
