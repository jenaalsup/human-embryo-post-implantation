# Data and Analysis for Human Embryo Post-Implantation Project

## Yolk Sac Geometry w/ Carnegie Virtual Human Embryo Data

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

## Primitive vs Visceral Endoderm Nuclear Morphology

Nuclear aspect ratios (major axis / minor axis) were measured to distinguish primitive endoderm (elongated) from visceral endoderm (cuboidal) within the red channel of `16S3_VE+INT+PE.tif`.

The original image contains three channels: yellow (epiblast), green (trophoblast), and red (both primitive and visceral endoderm nuclei).

Nuclei were segmented from the red channel (`segmentations.tif`), manually curated to remove artifacts (`remove-shadow-nucleus.py` → `segmentations_without_shadow.tif`), and aspect ratios were computed for each nucleus.

`plot-aspect-ratio.py` generates a color-coded overlay (`aspect_ratio_linear_overlay.png`) where nuclei are colored by aspect ratio (blue = low/cuboidal, red = high/elongated). The overlay is shown on the yellow and green background only.

