import numpy as np
from skimage.io import imread
from skimage.measure import regionprops, label
from scipy.ndimage import binary_fill_holes
from skimage.morphology import opening, disk

# -----------------------
# Load segmentation
# -----------------------
labels = imread("segmentations_without_shadow.tif")

# -----------------------
# Clean the mask
# -----------------------
labels = binary_fill_holes(labels)
labels = opening(labels, disk(1))

# Label connected components
labels = label(labels)

# -----------------------
# Measure nuclei
# -----------------------
props = regionprops(labels)

aspect_ratios = []

for i, p in enumerate(props, start=1):
    ar = p.axis_major_length / p.axis_minor_length
    aspect_ratios.append(ar)
    print(f"Nucleus {i}: aspect ratio = {ar:.3f}")

# Optional: store results
aspect_ratios = np.array(aspect_ratios)


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm
from skimage.measure import regionprops

# --- Compute aspect ratios ---
props = regionprops(labels)

aspect_ratios = np.array([
    p.axis_major_length / p.axis_minor_length
    for p in props
])

# Normalize for colormap - linear scale
ar_min, ar_max = aspect_ratios.min(), aspect_ratios.max()
norm_linear = (aspect_ratios - ar_min) / (ar_max - ar_min)

# Normalize for colormap - log scale
log_ar = np.log(aspect_ratios)
log_min, log_max = log_ar.min(), log_ar.max()
norm_log = (log_ar - log_min) / (log_max - log_min)

cmap = plt.colormaps["coolwarm"]

# Create colored label images
colored_linear = np.zeros((*labels.shape, 3))
colored_log = np.zeros((*labels.shape, 3))
for i, p in enumerate(props):
    color_linear = cmap(norm_linear[i])[:3]
    color_log = cmap(norm_log[i])[:3]
    colored_linear[labels == p.label] = color_linear
    colored_log[labels == p.label] = color_log


# ============================
# FIGURE 1: Color only (both scales)
# ============================
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 10))

# Linear scale
ax1.imshow(colored_linear)
ax1.set_title("Linear scale")
ax1.axis("off")
sm1 = cm.ScalarMappable(cmap=cmap)
sm1.set_array(aspect_ratios)
fig1.colorbar(sm1, ax=ax1, label="Aspect Ratio")

# Log scale
ax2.imshow(colored_log)
ax2.set_title("Log scale")
ax2.axis("off")
sm2 = cm.ScalarMappable(cmap=cmap, norm=LogNorm(vmin=ar_min, vmax=ar_max))
sm2.set_array(aspect_ratios)
fig1.colorbar(sm2, ax=ax2, label="Aspect Ratio")

plt.show()


# ============================
# FIGURE 2: Color + major axis
# ============================
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 10))
ax.imshow(colored_log)
ax.set_title("Aspect ratio with major + minor axes (log scale)")
ax.axis("off")

for p in props:
    y0, x0 = p.centroid
    theta = p.orientation

    # Half lengths
    L = p.axis_major_length / 2
    l = p.axis_minor_length / 2

    # Major axis direction
    dx_major = np.sin(theta)
    dy_major = np.cos(theta)

    # Minor axis direction (perpendicular)
    dx_minor = np.cos(theta)
    dy_minor = -np.sin(theta)

    # Plot major axis (red)
    ax.plot(
        [x0 - L*dx_major, x0 + L*dx_major],
        [y0 - L*dy_major, y0 + L*dy_major],
        'r', linewidth=2
    )

    # Plot minor axis (cyan)
    ax.plot(
        [x0 - l*dx_minor, x0 + l*dx_minor],
        [y0 - l*dy_minor, y0 + l*dy_minor],
        'c', linewidth=2
    )

plt.show()
