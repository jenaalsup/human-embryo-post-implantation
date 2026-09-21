/*
 Batch segmentation for Day 12 images (4 z-slices).

 Opens each .tif from Desktop, runs the Day 12 segmentation pipeline with
 per-image thresholds, and saves:
   - aspect-ratio/masks/{name}-segmentations.tif  (for Python)

 Does NOT overwrite data/*-segmentation.csv (those have manual A/E/I labels).

 Run in Fiji: Plugins > Macros > Run...
*/

desktopDir = "/Users/jenaalsup/Desktop";
baseDir = "/Users/jenaalsup/Desktop/human-embryo-post-implantation/amnion-epiblast-positioning";
maskDir = baseDir + "/aspect-ratio/masks";

File.makeDirectory(maskDir);

names = newArray(
    "260916_Day12-Vasc_S9-Sec2_Z13",
    "260916_Day12-Vasc_S9-Sec2_Z26",
    "260916_Day12-Vasc_S9-Sec2_Z33",
    "260916_Day12-Vasc_S9-Sec3_Z23"
);
thresholds = newArray(45, 45, 70, 50);

setBatchMode(true);

for (i = 0; i < names.length; i++) {
    name = names[i];
    threshold = thresholds[i];

    print("Processing: " + name + " (threshold=" + threshold + ")");

    open(desktopDir + "/" + name + ".tif");

    run("Duplicate...", "duplicate channels=1 title=Segmentation");
    selectWindow("Segmentation");

    run("8-bit");
    run("Gaussian Blur...", "sigma=0.8");
    run("Despeckle");
    run("Close");

    setThreshold(threshold, 255);
    run("Convert to Mask");

    run("Median...", "radius=1");
    run("Options...", "iterations=1 count=1 black do=Open");
    run("Options...", "iterations=1 count=1 black do=Close");
    run("Watershed");

    run("Set Measurements...", "area centroid fit shape display redirect=None decimal=2");
    roiManager("reset");
    run("Analyze Particles...", "size=30-600 circularity=0.15-1.00 show=Masks display clear include add");

    maskPath = maskDir + "/" + name + "-segmentations.tif";
    saveAs("Tiff", maskPath);

    roiManager("reset");
    while (nImages > 0) {
        selectImage(1);
        close();
    }
}

setBatchMode(false);

print("Done. Masks: " + maskDir);
print("Then run: python batch-aspect-ratio.py");
