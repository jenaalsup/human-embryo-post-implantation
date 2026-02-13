#!/usr/bin/env python3
"""
Simple plot of amnion, intermediate, and epiblast nuclei.
Blue = Amnion, Purple = Intermediate, Orange = Epiblast
"""

import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Get directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')

# Files to process
INPUT_FILES = [
    os.path.join(DATA_DIR, "17s1z20-segmentation.csv"),
    os.path.join(DATA_DIR, "18s1z14-segmentation.csv"),
    os.path.join(DATA_DIR, "18s2z9-segmentation.csv")
]

def plot_classification(input_csv):
    """Create plot for a single segmentation file."""
    
    # Generate output filename (save one folder up from data/)
    basename = os.path.basename(input_csv).replace('-segmentation.csv', '-amnion-epiblast-plot.png')
    parent_dir = os.path.dirname(os.path.dirname(input_csv))
    output = os.path.join(parent_dir, basename)
    
    # Read nuclei
    nuclei = []
    with open(input_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            nuclei.append({
                'id': len(nuclei) + 1,
                'x': float(row['X']),
                'y': float(row['Y']),
                'type': row['EpiblastAmnionIntermediate'].strip().upper()
            })
    
    # Separate by type
    amnion = [n for n in nuclei if n['type'] == 'A']
    intermediate = [n for n in nuclei if n['type'] == 'I']
    epiblast = [n for n in nuclei if n['type'] == 'E']
    
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
    
    # Plot intermediate (purple)
    if intermediate:
        ax.scatter([n['x'] for n in intermediate], [n['y'] for n in intermediate], 
                  c='#9C27B0', s=300, alpha=0.7, edgecolors='black', 
                  linewidth=2, label='Intermediate', zorder=3)
        for n in intermediate:
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
    ax.set_title(f'Cell Classification\n'
                f'Amnion: {len(amnion)} | Intermediate: {len(intermediate)} | Epiblast: {len(epiblast)}', 
                fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.savefig(output.replace('.png', '.eps'), format='eps', bbox_inches='tight')
    plt.close()
    
    print(f"✓ {os.path.basename(input_csv)} -> {os.path.basename(output)}")
    print(f"  Amnion: {len(amnion)} | Intermediate: {len(intermediate)} | Epiblast: {len(epiblast)}")
    
    return len(amnion), len(intermediate), len(epiblast)

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
