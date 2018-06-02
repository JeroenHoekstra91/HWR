import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
ap.add_argument("-o", "--output", required=True,
	help="path to output split dataset")
ap.add_argument("-p", "--percentage", required=True,
	help="percentage of data to split")
args = vars(ap.parse_args())

print "Splitting %s%% of the data found in %s\n" % (args["percentage"], args["dataset"])

split = int(round(1/(int(args["percentage"])/100.0)))
i = 0
moved = 0

for root, dirs, files in os.walk(args["dataset"]):
    for name in files:
        if i % split == 0:
        	imagePath = os.path.join(root, name)
        	outputdir = os.path.join(args["output"], os.path.sep.join(imagePath.split(os.path.sep)[1:-1]))
        	outputImagePath = os.path.join(outputdir, imagePath.split(os.path.sep)[-1])
        	print "moving %s -> %s" % (imagePath, outputImagePath)

        	if not os.path.exists(outputdir):
        		os.makedirs(outputdir)
        	os.rename(imagePath, outputImagePath)
        	moved += 1
        i += 1

print "\nmoved %d out of %d files" % (moved, i)
print "intended to move %s%% -> actually moved %d%%" % (args["percentage"], ((moved*100.0)/i))