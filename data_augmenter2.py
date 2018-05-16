import argparse
import os
from imgaug import augmenters as iaa
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
args = vars(ap.parse_args())

imagePaths = []
for root, dirs, files in os.walk(args["dataset"]):
    for name in files:
        imagePaths.append(os.path.join(root, name))

print len(imagePaths)

# ----------------------------------
# State indices
SALT_AND_PEPPER = 0
GAUSSIAN_NOISE = 1
SHEAR = 2

MIN_STATE   = [0  , 0  , -16]
INTERVAL    = [0.1, 0.1, 1]
MAX_STATE   = [0.4, 0.4, 16]

STATE = list(MIN_STATE)
print STATE
ORIGINAL_IMAGE = [0]*len(MIN_STATE)

def increment_state():
    i = 0;
    while i < len(STATE):
        if STATE[i] == MAX_STATE[i]:
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
            continue;

        seq = iaa.Sequential([
            iaa.Affine(shear=(STATE[SHEAR]),
                       cval=(255)),
            iaa.AdditiveGaussianNoise(scale=255*STATE[GAUSSIAN_NOISE]),
            iaa.SaltAndPepper(p=STATE[SALT_AND_PEPPER])
        ])

        images_aug = seq.augment_image(image)

        cv2.imwrite("images/Pe-final/test"+str(j)+"-S"+str(STATE[SHEAR])+"-GN"+str(STATE[GAUSSIAN_NOISE])+
                    "-SP"+str(STATE[SALT_AND_PEPPER])+".png", images_aug)

        if(STATE == MAX_STATE):
            STATE = list(MIN_STATE)
            break
        else:
            increment_state()

    j = j+1