import numpy as np
from skimage.io import imread, imsave
from skimage.measure import label

# -----------------------
# Load original labels
# -----------------------
labels = imread("segmentations.tif")

# -----------------------
# Remove one label
# -----------------------
label_to_remove = 2   # NOTE: label 2 is the shadow

labels_clean = labels.copy()
labels_clean[labels_clean == label_to_remove] = 0

# Relabel to keep labels contiguous (1,2,3,...)
labels_clean = label(labels_clean > 0)

# -----------------------
# Save new TIFF
# -----------------------
imsave(
    f"segmentations_removed_label{label_to_remove}.tif",
    labels_clean.astype(np.uint16)
)

print(f"Saved segmentations_removed_label{label_to_remove}.tif")
