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

Images were calibrated in Fiji using a reference distance measured in the Virtual Human Embryo viewer (565 µm across the tissue width in the same section); the corresponding pixel distance (~500 pixels for a representative slice) was measured in Fiji and used to set the pixel-to-micrometer scale prior to all area and shape measurements.



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

Found that 717 microns maps to ~500 pixels in Fiji.

The yolk sac cavity was manually outlined using the Freehand Selection tool in Fiji, tracing the inner lumenal boundary.

Measurements for Stage 5c are stored in `data/measurements/carnegie_CS5c_yolkSac.csv`. Across the ten selected sections, yolk sac cavity cross-sectional area ranged from approximately 1.01×10⁵ to 1.17×10⁵ µm².

