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
SHEAR = 0
SALT_AND_PEPPER = 1
GAUSSIAN_NOISE = 2

MIN_STATE   = [0,   0  , -16]
INTERVAL    = [0.2, 0.2, 1]
MAX_STATE   = [0.6, 0.6, 16]

STATE = [0,0,0]
ORIGINAL_IMAGE = [0,0,0]

def reset_state():
    STATE = list(MIN_STATE)

def increment_state():
    i = 0;
    while i < len(STATE):
        if STATE[i] == MAX_STATE[i]:
            STATE[i] = 0
        else:
            STATE[i] = STATE[i] + INTERVAL[i]
            break
        i = i + 1

# loop over the input images
j = 0
reset_state()
for imagePath in imagePaths:
    # load the image, pre-process it, and store it in the data list
    image = cv2.imread(imagePath)

    while(True):
        if STATE == ORIGINAL_IMAGE:
            break;

        seq = iaa.Sequential([
            iaa.Affine(shear=(STATE[SHEAR]-17),
                       cval=(255)),
            # iaa.AdditiveGaussianNoise(0, STATE[GAUSSIAN_NOISE]/100),

        ])

        images_aug = seq.augment_image(image)

        # cv2.imwrite("images/Pe-final/test"+str(j)+"-S"+str(STATE[SHEAR])+"-GN"+str(STATE[GAUSSIAN_NOISE])+
        #             "-SP"+str(STATE[SALT_AND_PEPPER])+".png", images_aug)

        cv2.imwrite("images/Pe-final/test" + str(j) + "-S" + str(STATE[SHEAR]) + ".png", images_aug)
        if(STATE == MAX_STATE):
            reset_state()
            break
        else:
            increment_state()

    j = j+1