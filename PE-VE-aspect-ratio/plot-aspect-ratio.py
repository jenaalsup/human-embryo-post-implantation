import numpy as np
from skimage.io import imread
from skimage.measure import regionprops, label
from scipy.ndimage import binary_fill_holes
from skimage.morphology import opening, disk

# -----------------------
# Load segmentation and original image
# -----------------------
labels = imread("segmentations_without_shadow.tif")
original = imread("16S3_VE+INT+PE.tif")

# Print image info to understand structure
print(f"Original image shape: {original.shape}")
print(f"Original image dtype: {original.dtype}")
print(f"Original image min/max: {original.min()}/{original.max()}")

# Remap channels to match Fiji display: Yellow, Green, Red
# Channel 1 in Fiji = Yellow (displayed as R+G)
# Channel 2 in Fiji = Green (displayed as G)
# Channel 3 in Fiji = Red (displayed as R)
if original.ndim == 3 and original.shape[2] == 3:
    ch1 = original[:, :, 0].astype(float)  # Yellow channel
    ch2 = original[:, :, 1].astype(float)  # Green channel
    ch3 = original[:, :, 2].astype(float)  # Red channel
    
    # Composite display as Fiji shows it (all channels):
    original_display = np.zeros_like(original, dtype=float)
    original_display[:, :, 0] = ch1 + ch3  # Red = yellow + red channels
    original_display[:, :, 1] = ch1 + ch2  # Green = yellow + green channels
    original_display[:, :, 2] = 0           # Blue = none (no blue in yellow/green/red)
    
    # Clip to prevent overflow and convert back
    original_display = np.clip(original_display, 0, 255)
    original = original_display.astype(np.uint8)
    
    # Create version without red channel for overlay backgrounds
    original_no_red = np.zeros_like(original, dtype=float)
    original_no_red[:, :, 0] = ch1  # Red = yellow channel only (no red nuclei)
    original_no_red[:, :, 1] = ch1 + ch2  # Green = yellow + green channels
    original_no_red[:, :, 2] = 0  # Blue = none
    original_no_red = np.clip(original_no_red, 0, 255).astype(np.uint8)

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

# Create colored label images with RGBA (includes alpha channel)
colored_linear = np.zeros((*labels.shape, 4))
colored_log = np.zeros((*labels.shape, 4))
for i, p in enumerate(props):
    color_linear = cmap(norm_linear[i])  # RGBA
    color_log = cmap(norm_log[i])  # RGBA
    colored_linear[labels == p.label] = color_linear
    colored_log[labels == p.label] = color_log


# ============================
# FIGURE 1: Original and overlays (both scales)
# ============================
fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 20))

# Row 1: Original and Linear scale
ax1.imshow(original)
ax1.set_title("Original")
ax1.axis("off")

ax2.imshow(original_no_red)
ax2.imshow(colored_linear)
ax2.set_title("Linear scale")
ax2.axis("off")
sm1 = cm.ScalarMappable(cmap=cmap)
sm1.set_array(aspect_ratios)
fig1.colorbar(sm1, ax=ax2, label="Aspect Ratio")

# Row 2: Original and Log scale
ax3.imshow(original)
ax3.set_title("Original")
ax3.axis("off")

ax4.imshow(original_no_red)
ax4.imshow(colored_log)
ax4.set_title("Log scale")
ax4.axis("off")
sm2 = cm.ScalarMappable(cmap=cmap, norm=LogNorm(vmin=ar_min, vmax=ar_max))
sm2.set_array(aspect_ratios)
fig1.colorbar(sm2, ax=ax4, label="Aspect Ratio")

plt.show()

# ============================
# Export linear scale overlay with legend and title
# ============================
fig_export, ax_export = plt.subplots(figsize=(8, 10))
ax_export.imshow(original_no_red)
ax_export.imshow(colored_linear)
ax_export.set_title("Aspect Ratio")
ax_export.axis("off")
sm_export = cm.ScalarMappable(cmap=cmap)
sm_export.set_array(aspect_ratios)
fig_export.colorbar(sm_export, ax=ax_export, label="Aspect Ratio")
plt.tight_layout()
fig_export.savefig("aspect_ratio_linear_overlay.png", dpi=300, bbox_inches='tight')
print("Saved high-resolution image: aspect_ratio_linear_overlay.png")
plt.close(fig_export)


# ============================
# FIGURE 2: Color + major axis
# ============================
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 10))
ax.imshow(original_no_red)
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
