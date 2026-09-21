#!/usr/bin/env python
"""Batch aspect-ratio plots for all four Day 12 images."""

import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import cm
    from scipy.ndimage import binary_fill_holes
    from skimage.io import imread
    from skimage.measure import label, regionprops
    from skimage.morphology import disk, opening
except ModuleNotFoundError:
    sys.exit(
        "Missing dependencies. Use your conda Python (not Homebrew python3):\n"
        "  python batch-aspect-ratio.py"
    )

SCRIPT_DIR = Path(__file__).resolve().parent
MASK_DIR = SCRIPT_DIR / "masks"
OUTPUT_DIR = SCRIPT_DIR / "outputs"

DAY12_NAMES = [
    "260916_Day12-Vasc_S9-Sec2_Z13",
    "260916_Day12-Vasc_S9-Sec2_Z26",
    "260916_Day12-Vasc_S9-Sec2_Z33",
    "260916_Day12-Vasc_S9-Sec3_Z23",
]


def load_labeled_mask(mask_path):
    mask = imread(mask_path)
    mask = mask > 0
    mask = binary_fill_holes(mask)
    mask = opening(mask, disk(1))
    return label(mask)


def save_aspect_ratio_figure(mask_path, output_dir, basename):
    labels = load_labeled_mask(mask_path)
    props = regionprops(labels)
    aspect_ratios = np.array([
        p.axis_major_length / p.axis_minor_length
        for p in props
    ])

    if len(aspect_ratios) == 0:
        raise ValueError(f"No nuclei found in {mask_path}")

    ar_min, ar_max = aspect_ratios.min(), aspect_ratios.max()
    if ar_max > ar_min:
        norm = (aspect_ratios - ar_min) / (ar_max - ar_min)
    else:
        norm = np.full(len(aspect_ratios), 0.5)

    cmap = plt.colormaps["coolwarm"]
    colored = np.zeros((*labels.shape, 3))
    for i, p in enumerate(props):
        colored[labels == p.label] = cmap(norm[i])[:3]

    for i, ar in enumerate(aspect_ratios, start=1):
        print(f"{basename} nucleus {i}: aspect ratio = {ar:.3f}")

    fig, ax = plt.subplots(figsize=(6, 10))
    ax.imshow(colored)
    ax.set_title("Nuclei colored by aspect ratio")
    ax.axis("off")
    sm = cm.ScalarMappable(cmap=cmap)
    sm.set_array(aspect_ratios)
    fig.colorbar(sm, ax=ax, label="Aspect Ratio")

    png_path = output_dir / f"{basename}-aspect-ratio.png"
    eps_path = output_dir / f"{basename}-aspect-ratio.eps"
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    fig.savefig(eps_path, format="eps", bbox_inches="tight")
    plt.close(fig)

    print(f"Saved {png_path.name} and {eps_path.name} -> {output_dir}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for name in DAY12_NAMES:
        mask_path = MASK_DIR / f"{name}-segmentations.tif"
        if not mask_path.exists():
            raise FileNotFoundError(
                f"Missing mask: {mask_path}\n"
                "Run segment-day12-batch.ijm.ijm in Fiji first."
            )
        save_aspect_ratio_figure(mask_path, OUTPUT_DIR, name)


if __name__ == "__main__":
    main()
