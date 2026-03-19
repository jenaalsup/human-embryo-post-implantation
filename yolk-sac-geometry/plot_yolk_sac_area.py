#!/usr/bin/env python3
"""
Plot yolk sac area across developmental stages.
"""

import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Read Carnegie data
carnegie_data = {'CS 5b': [], 'CS 5c': []}
with open('carnegie/data/carnegie-yolk-sac-area-combined.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        stage = row['Stage']
        area = float(row['Area'])
        if stage == '5b':
            carnegie_data['CS 5b'].append(area)
        elif stage == '5c':
            carnegie_data['CS 5c'].append(area)

# Read experimental data
exp_data = {'Day 10': [], 'Day 12': []}
with open('experimental/data/experimental-yolk-sac-area.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        day = int(row['Day'])
        area = float(row['Area'])
        if day == 10:
            exp_data['Day 10'].append(area)
        elif day == 12:
            exp_data['Day 12'].append(area)

# Combine all data
all_groups = ['CS 5b', 'CS 5c', 'Day 10', 'Day 12']
all_data = [carnegie_data['CS 5b'], carnegie_data['CS 5c'], 
            exp_data['Day 10'], exp_data['Day 12']]
colors = ['#1E88E5', '#42A5F5', '#FF6F00', '#FFA726']  # Blue shades, orange shades

# Print summary
print("Data summary:")
for group, data in zip(all_groups, all_data):
    print(f"  {group}: n={len(data)}, mean={sum(data)/len(data):.1f} µm²")

# PLOT 1: Box plot only
fig, ax = plt.subplots(figsize=(8, 7))

bp = ax.boxplot(all_data, tick_labels=all_groups, patch_artist=True,
                widths=0.4, showfliers=True,
                boxprops=dict(facecolor='white', edgecolor='black', linewidth=2),
                medianprops=dict(color='red', linewidth=2),
                whiskerprops=dict(color='black', linewidth=1.5),
                capprops=dict(color='black', linewidth=1.5),
                flierprops=dict(marker='o', markerfacecolor='black', markersize=6, alpha=0.5))

ax.set_ylabel('Yolk Sac Area (µm²)', fontsize=16, fontweight='bold')
ax.set_xlabel('Developmental Stage', fontsize=16, fontweight='bold')
ax.set_title('Yolk Sac Cavity Area Across Developmental Stages', fontsize=16, fontweight='bold')
ax.tick_params(axis='both', labelsize=14)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add sample sizes
for i, (group, n) in enumerate(zip(all_groups, [len(d) for d in all_data])):
    ax.text(i+1, ax.get_ylim()[0] * 0.98, f'n={n}', ha='center', fontsize=12, style='italic')

plt.tight_layout()
plt.savefig('yolk-sac-area-boxplot.png', dpi=300, bbox_inches='tight')
plt.savefig('yolk-sac-area-boxplot.eps', format='eps', bbox_inches='tight')
print("\n✓ Box plot saved: yolk-sac-area-boxplot.png and .eps")

# PLOT 2: Scatter plot only
fig, ax = plt.subplots(figsize=(10, 8))

for i, (data, color, group) in enumerate(zip(all_data, colors, all_groups)):
    x = [i + 1] * len(data)
    ax.scatter(x, data, c=color, s=150, alpha=0.7, edgecolors='black', 
              linewidth=1, label=group, zorder=3)

ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(all_groups)
ax.set_ylabel('Yolk Sac Area (µm²)', fontsize=14, fontweight='bold')
ax.set_xlabel('Developmental Stage', fontsize=14, fontweight='bold')
ax.set_title('Yolk Sac Cavity Area Across Developmental Stages', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)
ax.legend(fontsize=11, loc='upper left')

plt.tight_layout()
plt.savefig('yolk-sac-area-scatter.png', dpi=300, bbox_inches='tight')
plt.savefig('yolk-sac-area-scatter.eps', format='eps', bbox_inches='tight')
print("✓ Scatter plot saved: yolk-sac-area-scatter.png and .eps")
