#!/usr/bin/env python3
"""
Compare orientation angles between amnion and epiblast nuclei.
Box plot + scatter with Mann-Whitney U test.
"""

import csv
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Input files
INPUT_FILES = [
    "17s1z20-segmentation.csv",
    "18s1z14-segmentation.csv",
    "18s2z9-segmentation.csv"
]

OUTPUT = "amnion-vs-epiblast-orientation.png"

def calculate_orientation_angle(center_x, center_y, nucleus_x, nucleus_y, major_axis_angle):
    """Calculate orientation angle (0-90°) relative to radial direction."""
    # Radial angle
    dx = nucleus_x - center_x
    dy = nucleus_y - center_y
    radial = math.degrees(math.atan2(dy, dx)) % 180
    
    # Major axis angle normalized to 0-180
    major = major_axis_angle % 180
    
    # Orientation angle (0-90 range)
    diff = abs(radial - major)
    if diff > 90:
        diff = 180 - diff
    
    return diff

# Process all files
amnion_angles = []
epiblast_angles = []

print("Processing files...\n")

for csv_file in INPUT_FILES:
    # Read nuclei
    nuclei = []
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            nuclei.append({
                'x': float(row['X']),
                'y': float(row['Y']),
                'angle': float(row['Angle']),
                'is_amnion': row['IsAmnion'].strip().upper() == 'Y'
            })
    
    # Calculate center
    center_x = sum(n['x'] for n in nuclei) / len(nuclei)
    center_y = sum(n['y'] for n in nuclei) / len(nuclei)
    
    # Calculate orientation angles
    for n in nuclei:
        orientation = calculate_orientation_angle(center_x, center_y, n['x'], n['y'], n['angle'])
        
        if n['is_amnion']:
            amnion_angles.append(orientation)
        else:
            epiblast_angles.append(orientation)
    
    print(f"✓ {csv_file}: {len([n for n in nuclei if n['is_amnion']])} amnion, {len([n for n in nuclei if not n['is_amnion']])} epiblast")

# Statistical test (Welch's t-test - doesn't assume equal variance)
def welch_ttest(x, y):
    """Welch's t-test for two independent samples with unequal variances."""
    n1, n2 = len(x), len(y)
    mean1, mean2 = sum(x) / n1, sum(y) / n2
    var1 = sum((xi - mean1)**2 for xi in x) / (n1 - 1)
    var2 = sum((yi - mean2)**2 for yi in y) / (n2 - 1)
    
    # t statistic
    t = (mean1 - mean2) / math.sqrt(var1/n1 + var2/n2)
    
    # degrees of freedom (Welch-Satterthwaite)
    df = (var1/n1 + var2/n2)**2 / ((var1/n1)**2/(n1-1) + (var2/n2)**2/(n2-1))
    
    # Two-tailed p-value (approximate using normal distribution for large df)
    from math import erf
    p = 2 * (1 - 0.5 * (1 + erf(abs(t) / math.sqrt(2))))
    
    return t, df, p

t_stat, df, pvalue = welch_ttest(amnion_angles, epiblast_angles)

print(f"\n{'='*60}")
print("RESULTS")
print(f"{'='*60}")
print(f"Amnion: n={len(amnion_angles)}, mean={sum(amnion_angles)/len(amnion_angles):.1f}°, median={sorted(amnion_angles)[len(amnion_angles)//2]:.1f}°")
print(f"Epiblast: n={len(epiblast_angles)}, mean={sum(epiblast_angles)/len(epiblast_angles):.1f}°, median={sorted(epiblast_angles)[len(epiblast_angles)//2]:.1f}°")
print(f"\nWelch's t-test: t={t_stat:.3f}, df={df:.1f}, p={pvalue:.4f}")

statistic = t_stat

if pvalue < 0.001:
    sig = "***"
elif pvalue < 0.01:
    sig = "**"
elif pvalue < 0.05:
    sig = "*"
else:
    sig = "ns"

print(f"Significance: {sig}")

# Create plot
fig, ax = plt.subplots(figsize=(8, 10))

# Prepare data
data = [amnion_angles, epiblast_angles]
labels = ['Amnion', 'Epiblast']
colors = ['#1E88E5', '#FF8C00']

# Box plot
bp = ax.boxplot(data, tick_labels=labels, patch_artist=True,
                widths=0.6, showfliers=False,
                boxprops=dict(facecolor='white', edgecolor='black', linewidth=2),
                medianprops=dict(color='red', linewidth=2),
                whiskerprops=dict(color='black', linewidth=1.5),
                capprops=dict(color='black', linewidth=1.5))

# Overlay scatter points with jitter
for i, (angles, color) in enumerate(zip(data, colors)):
    x = [i + 1 + (0.1 * (j % 2 - 0.5)) for j in range(len(angles))]  # Add jitter
    ax.scatter(x, angles, c=color, s=80, alpha=0.6, edgecolors='black', linewidth=0.5, zorder=3)

# Add significance annotation
y_max = max(max(amnion_angles), max(epiblast_angles))
y_pos = y_max + 5

ax.plot([1, 1, 2, 2], [y_pos, y_pos+2, y_pos+2, y_pos], 'k-', linewidth=1.5)
ax.text(1.5, y_pos+3, sig, ha='center', va='bottom', fontsize=14, fontweight='bold')
ax.text(1.5, y_pos+6, f'p={pvalue:.4f}', ha='center', va='bottom', fontsize=10)

# Format
ax.set_ylabel('Orientation Angle (°)', fontsize=14, fontweight='bold')
ax.set_title('Nuclear Major Axis Orientation: Amnion vs Epiblast\n0° = Parallel to radius, 90° = Perpendicular to radius', 
            fontsize=13, fontweight='bold', pad=20)
ax.set_ylim(-5, y_pos + 15)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add sample sizes
for i, (label, n) in enumerate(zip(labels, [len(amnion_angles), len(epiblast_angles)])):
    ax.text(i+1, -3, f'n={n}', ha='center', fontsize=10, style='italic')

plt.tight_layout()
plt.savefig(OUTPUT, dpi=300, bbox_inches='tight')
print(f"\n✓ Plot saved: {OUTPUT}")

# Save raw data to CSV
raw_data = []
for angle in amnion_angles:
    raw_data.append({'cell_type': 'Amnion', 'orientation_angle': angle})
for angle in epiblast_angles:
    raw_data.append({'cell_type': 'Epiblast', 'orientation_angle': angle})

with open('amnion-vs-epiblast-raw-data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['cell_type', 'orientation_angle'])
    writer.writeheader()
    writer.writerows(raw_data)

print(f"✓ Raw data saved: amnion-vs-epiblast-raw-data.csv")
