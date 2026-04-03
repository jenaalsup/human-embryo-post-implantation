# Data and Analysis for Human Embryo Post-Implantation Project

## Yolk Sac Geometry w/ Carnegie Virtual Human Embryo Data (/yolk-sac-geometry/carnegie)

10 sections used per stage (from one embryo)

### Stage 5b (~9 days post-fertilization)

* Total z-sections: 100
* Epiblast visible in slices: 41-55
* Selected slices (middle 10 w/ epiblast): 43-52 (inclusive)

Reference tissue width measured using the Virtual Human Embryo viewer for each selected section:
- Slice 43: 565 µm 
- Slice 44: 565 µm
- Slice 45: 565 µm
- Slice 46: 565 µm
- Slice 47: 565 µm
- Slice 48: 565 µm
- Slice 49: 565 µm
- Slice 50: 565 µm
- Slice 51: 565 µm
- Slice 52: 565 µm

All slices have a width of **565 µm**.

Images were calibrated in Fiji using a reference distance measured in the Virtual Human Embryo viewer (565 µm across the tissue width in the same section); the corresponding pixel distance (600 pixels for a representative slice) was measured in Fiji and used to set the pixel-to-micrometer scale prior to all area and shape measurements.

The yolk sac cavity was manually outlined using the Freehand Selection tool in Fiji, tracing the inner lumenal boundary.

Measurements for Stage 5b are stored in `data/carnegie-5b-yolk-sac-area.csv`. Across the ten selected sections, yolk sac cavity cross-sectional area ranged from approximately 6.5×10³ to 1.01×10⁴ µm².


### Stage 5c (~11 to 12 days post-fertilization)

* Total z-sections: 140
* Epiblast present in slices: 56-83
* Selected slices (middle 10 w/ epiblast): 65-74 (inclusive)

Reference tissue width measured using the Virtual Human Embryo viewer for each selected section:
- Slice 65: 717 µm 
- Slice 66: 716 µm
- Slice 67: 717 µm
- Slice 68: 717 µm
- Slice 69: 716 µm
- Slice 70: 717 µm
- Slice 71: 717 µm
- Slice 72: 717 µm
- Slice 73: 716 µm
- Slice 74: 717 µm

The modal reference width across selected sections was **717 µm** and was used for image calibration.

Images were calibrated in Fiji using a reference distance measured in the Virtual Human Embryo viewer (717 µm across the tissue width in the same section); the corresponding pixel distance (~500 pixels for a representative slice) was measured in Fiji and used to set the pixel-to-micrometer scale prior to all area and shape measurements.

The yolk sac cavity was manually outlined using the Freehand Selection tool in Fiji, tracing the inner lumenal boundary.

Measurements for Stage 5c are stored in `data/carnegie-5c-yolk-sac-area.csv`. Across the ten selected sections, yolk sac cavity cross-sectional area ranged from approximately 1.01×10⁵ to 1.17×10⁵ µm².

### Number of epiblast cells:
5b:
- Slice 43: 12
- Slice 44: 14
- Slice 45: 18
- Slice 46: 19
- Slice 47: 21
- Slice 48: 18
- Slice 49: 18
- Slice 50: 16
- Slice 51: 13
- Slice 52: 12

5c:
- Slice 65: 24
- Slice 66: 24
- Slice 67: 23
- Slice 68: 27
- Slice 69: 35
- Slice 70: 23
- Slice 71: 23
- Slice 72: 25
- Slice 73: 24
- Slice 74: 22


## Yolk Sac Geometry w/ Experimental Data (/yolk-sac-geometry/experimental)

### Day 12
Section 3 > Series 1 > epiblast visible from z-slices 4 to 37, use slices 18-22 (middle 5)
Section 2 > Series 10 > epiblast visible from z-slices 12 to 25, use slices 19-23 (middle 5)
Section 1 > Series 10 > 27 sections total, use slices 12-16 (middle 5)

### Day 10
- MAX_Composite_zstack.tif (one measurement)
- C5-E7_Slide16_Sec3_HYPO > epiblast visible from slices 1-21, use slices 9-13 (middle 5)
- C5-E7_Slide17_Sec1_HYPO > epiblast visible from slices 4-22, use slices 11-15 (middle 5)
- E9_Slide16_Sec3 > epiblast visible from slices 2-26, use slices 12-16 (middle 5)
- E9_Slide17_Sec1 > epiblast visible from slices 1-21, use slices 9-13 (middle 5)

## Primitive vs Visceral Endoderm Nuclear Morphology (/PE-VE-aspect-ratio)

Nuclear aspect ratios (major axis / minor axis) were measured to distinguish primitive endoderm (elongated) from visceral endoderm (cuboidal) within the red channel of `16S3_VE+INT+PE.tif`.

The original image contains three channels: yellow (epiblast), green (trophoblast), and red (both primitive and visceral endoderm nuclei).

Nuclei were segmented from the red channel (`segmentations.tif`), manually curated to remove artifacts (`remove-shadow-nucleus.py` → `segmentations_without_shadow.tif`), and aspect ratios were computed for each nucleus.

`plot-aspect-ratio.py` generates a color-coded overlay (`aspect_ratio_linear_overlay.png`) where nuclei are colored by aspect ratio (blue = low/cuboidal, red = high/elongated). The overlay is shown on the yellow and green background only.

## Orientation of Amnion vs Epiblast Nuclei (/amnion-epiblast-positioning)

Nuclear major axis orientation was analyzed to compare alignment relative to the radial direction (center → nucleus) in amnion vs epiblast cells.

Nuclei were segmented from DAPI channel (three images: 17s1 z20, 18s1 z14, 18s2 z9) using the Fiji macros in `/scripts`, then manually classified as amnion or epiblast. The orientation angle of each nucleus's major axis relative to its radial direction was calculated (0° = parallel, 90° = perpendicular).

`scripts/compare-orientation-angles.py` performs statistical comparison (Welch's t-test) and generates a box plot with scatter overlay. Amnion nuclei (n=40) are significantly more perpendicular to the radius (mean=47.4°) compared to epiblast nuclei (n=57, mean=36.9°; t=1.988, p=0.0468).

`amnion-epiblast-plot.py` generates spatial plots showing nucleus positions color-coded by cell type (blue=amnion, orange=epiblast) for each image.

Results stored in `cell-type-orientation.png` and `cell-type-orientation-raw-data.csv`.
