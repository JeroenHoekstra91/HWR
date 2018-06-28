# set the matplotlib backend so figures can be saved in the background
import datetime
import matplotlib

matplotlib.use("Agg")

# import the necessary packages
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from networks.lenet import LeNet
import numpy as np
import argparse
import random
import cv2
import os

char_map = {
    "Alef": 0,
    "Ayin": 1,
    "Bet": 2,
    "Dalet": 3,
    "Gimel": 4,
    "He": 5,
    "Het": 6,
    "Kaf": 7,
    "Kaf-final": 8,
    "Lamed": 9,
    "Mem": 10,
    "Mem-medial": 11,
    "Noise": 12,
    "Nun-final": 13,
    "Nun-medial": 14,
    "Pe": 15,
    "Pe-final": 16,
    "Qof": 17,
    "Resh": 18,
    "Samekh": 19,
    "Shin": 20,
    "Taw": 21,
    "Tet": 22,
    "Tsadi-final": 23,
    "Tsadi-medial": 24,
    "Waw": 25,
    "Yod": 26,
    "Zayin": 27,
}

print datetime.datetime.now().time()

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
ap.add_argument("-m", "--model", required=True,
	help="path to output model")
args = vars(ap.parse_args())

EPOCHS = 5
INIT_LR = 1e-3

# load images
print("[INFO] loading images...")
allLabel = []

imagePaths = []
random.seed(42)

for root, dirs, files in os.walk(args["dataset"]):
    for name in files:
        imagePaths.append(os.path.join(root, name))

random.shuffle(imagePaths)

for imagePath in imagePaths:
    label = imagePath.split(os.path.sep)[-2]
    allLabel.append(char_map[label])

# (trainX, testX, trainY, testY) = train_test_split(imagePaths, allLabel, test_size=0.0, random_state=42)
trainX = imagePaths
trainY = allLabel

print len(trainX)

for i in range(1, 150):
    if len(trainX) % i == 0 and len(trainX) / i <= 100000:
        print i
        BS = len(trainX) / i
        print BS
        break


# testData = []
# testLabel = []
# for imagePath in testX:
#     # load the image, pre-process it, and store it in the data list
#     image = cv2.imread(imagePath)
#     image = cv2.resize(image, (28, 28))
#     image = img_to_array(image)
#     testData.append(image)
#
#     label = imagePath.split(os.path.sep)[-2]
#     testLabel.append(char_map[label])
#
# testData = np.array(testData, dtype="float") / 255.0
# testLabel = np.array(testLabel)
# testLabel = to_categorical(testLabel, num_classes=28)


def get_train_data(STEP):
    trainData = []

    for i in range(BS*STEP,BS*STEP+BS):
        image = cv2.imread(trainX[i])
        image = cv2.resize(image, (28, 28))
        image = img_to_array(image)
        trainData.append(image)

    trainData = np.array(trainData, dtype="float") / 255.0

    return trainData

def get_train_label(STEP):
    trainLabel = []

    for i in range(BS*STEP,BS*STEP+BS):
        trainLabel.append(trainY[i])

    trainLabel = np.array(trainLabel)
    trainLabel = to_categorical(trainLabel, num_classes=28)

    return trainLabel

# initialize the model
print("[INFO] compiling model...")
model = LeNet.build(width=28, height=28, depth=3, classes=28)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
              metrics=["accuracy"])

# train the network
print("[INFO] training network...")

for i in range(len(trainX)/BS):
    # model.fit(get_train_data(i), get_train_label(i), validation_data=(testData, testLabel), initial_epoch=i,
    #           epochs=5, verbose=1)
    model.fit(get_train_data(i), get_train_label(i), initial_epoch=i,
              epochs=i + 1, verbose=1)

# save the model to disk
print("[INFO] serializing network...")
model.save(args["model"])

print datetime.datetime.now().time()
