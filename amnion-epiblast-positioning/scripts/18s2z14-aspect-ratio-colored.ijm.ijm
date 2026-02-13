// -----------------------------
// Nuclear segmentation + color by aspect ratio
// Blue = round (low AR) -> Red = elongated (high AR)
// Saves measurements CSV and creates RGB image "AR_colored"
// -----------------------------

outputPath = "/Users/jenaalsup/Desktop/18s2z14-segmentation.csv";

// -----------------------------
run("Duplicate...", "duplicate channels=1 title=Segmentation");
selectWindow("Segmentation");

// -----------------------------
run("8-bit");

run("Gaussian Blur...", "sigma=0.8");
run("Despeckle");
run("Close");

// -----------------------------
setThreshold(75, 255);
run("Convert to Mask");

// -----------------------------
run("Dilate");

run("Options...", "iterations=1 count=1 black do=Open");
run("Options...", "iterations=1 count=1 black do=Close");

run("Median...", "radius=1");

run("Analyze Particles...", "size=0-24 show=Nothing clear");
run("Fill Holes");
run("Watershed");

// -----------------------------
run("Set Measurements...", "area centroid shape fit redirect=None decimal=2");

roiManager("reset");
run("Analyze Particles...", 
    "size=25-300 circularity=0.00-1.00 show=Nothing display clear include add");

roiManager("Deselect");

// -----------------------------
n = roiManager("count");

if (n == 0) {
    print("No ROIs found. Exiting.");
    exit();
}

// -----------------------------
aspectRatios = newArray(n);

minAR = 1e9;
maxAR = -1e9;

run("Clear Results");

for (i = 0; i < n; i++) {

    roiManager("select", i);
    run("Measure");

    idx = nResults - 1;

    major = getResult("Major", idx);
    minor = getResult("Minor", idx);

    if (minor > 0)
        ar = major / minor;
    else
        ar = 1.0;

    aspectRatios[i] = ar;

    if (ar < minAR) minAR = ar;
    if (ar > maxAR) maxAR = ar;
}

// -----------------------------
saveAs("Results", outputPath);

// -----------------------------
w = getWidth();
h = getHeight();

newImage("AR_colored", "RGB black", w, h, 1);
selectWindow("AR_colored");

// -----------------------------
sameRange = (maxAR <= minAR + 1e-12);

// -----------------------------
for (i = 0; i < n; i++) {

    if (sameRange)
        norm = 0.5;
    else {
        norm = (aspectRatios[i] - minAR) / (maxAR - minAR);
        if (norm < 0) norm = 0;
        if (norm > 1) norm = 1;
    }

	r = round(norm * 255);
	g = round((1 - norm) * 255);
	b = round(norm * 255);

    roiManager("select", i);
    setForegroundColor(r, g, b);
    roiManager("Fill");
}

// -----------------------------
// Legend
// -----------------------------
legendWidth = 20;
legendHeight = 200;

x0 = w - 40;
y0 = 20;

for (j = 0; j < legendHeight; j++) {

    normLegend = 1 - (j / legendHeight);
    
	r = round(normLegend * 255);
	g = round((1 - normLegend) * 255);
	b = round(normLegend * 255);

    setColor(r, g, b);
    drawLine(x0, y0 + j, x0 + legendWidth, y0 + j);
}

// -----------------------------
setColor(255, 255, 255);

drawString("High AR", x0 - 5, y0 - 5);
drawString("Low AR",  x0 - 5, y0 + legendHeight + 15);

// -----------------------------
roiManager("Set Color", "white");
roiManager("Set Line Width", 1);
roiManager("Show None");

selectWindow("AR_colored");
resetMinAndMax();

saveAs("Tiff", "/Users/jenaalsup/Desktop/18s2z14-AR_colored.tif");
