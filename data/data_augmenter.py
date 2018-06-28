import argparse
import os

import numpy
from imgaug import augmenters as iaa
import cv2
import datetime

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
args = vars(ap.parse_args())

print datetime.datetime.now().time()

imagePaths = []
for root, dirs, files in os.walk(args["dataset"]):
    for name in files:
        imagePaths.append(os.path.join(root, name))

# ----------------------------------
# State indices
DAMAGE = 0
SCALE = 1
SHEAR = 2

MIN_STATE   = [0, 0.5, -10]
INTERVAL    = [0.05, 0.1, 5]
MAX_STATE   = [0.20, 1, 10]

STATE = list(MIN_STATE)
ORIGINAL_IMAGE = [0]*len(MIN_STATE)

def increment_state():
    i = 0
    while i < len(STATE):
        if round(STATE[i], 1) == MAX_STATE[i]:
            STATE[i] = MIN_STATE[i]
        else:
            STATE[i] = STATE[i] + INTERVAL[i]
            break
        i = i + 1

# loop over the input images
j = 0
for imagePath in imagePaths:
    # load the image, pre-process it, and store it in the data list
    image = cv2.imread(imagePath)

    while(True):
        if STATE == ORIGINAL_IMAGE:
            increment_state()
            continue

        seq = iaa.Sequential([
            iaa.Affine(shear=(STATE[SHEAR]), cval=(255)),
            iaa.Scale(STATE[SCALE]),
            iaa.Invert(1),
            iaa.CoarseDropout(STATE[DAMAGE], size_percent=(0.02, 0.50)),
            iaa.Invert(1),
        ])

        images_aug = seq.augment_image(image)

        cv2.imwrite(os.path.split(imagePath)[0]+"/Augmented"+str(j)+"-S"+str(STATE[SHEAR])+"-SC"+str(STATE[SCALE])+
                    "-D"+str(STATE[DAMAGE])+".png", images_aug)

        state = numpy.around(STATE, decimals=2)
        STATE = [state[0], state[1], state[2]]
        if(STATE == MAX_STATE):
            STATE = list(MIN_STATE)
            break
        else:
            increment_state()

    j = j+1

print datetime.datetime.now().time()
