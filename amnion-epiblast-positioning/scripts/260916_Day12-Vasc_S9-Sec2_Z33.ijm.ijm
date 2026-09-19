outputPath = "/Users/jenaalsup/Desktop/260916_Day12-Vasc_S9-Sec2_Z33.csv";

// duplicate and isolate DAPI channel
run("Duplicate...", "duplicate channels=1 title=Segmentation duplicate");
selectWindow("Segmentation");

// preprocessing
run("8-bit");
run("Gaussian Blur...", "sigma=0.8");
run("Despeckle");
run("Close");

// Threshold — return to your original fixed threshold
setThreshold(70, 255);
run("Convert to Mask");

// Morph cleanup — conservative
run("Median...", "radius=1");

run("Options...", "iterations=1 count=1 black do=Open");
run("Options...", "iterations=1 count=1 black do=Close");

// Gentle watershed prep: distance map but NO Find Maxima
run("Watershed");

// Analyze particles — slightly looser circularity
run("Set Measurements...", "area centroid fit shape display redirect=None decimal=2");
roiManager("reset");
run("Analyze Particles...", "size=30-600 circularity=0.15-1.00 show=Masks display clear include add"); run("Invert");
roiManager("Deselect");
roiManager("Show All with labels");

// save
saveAs("Results", outputPath);