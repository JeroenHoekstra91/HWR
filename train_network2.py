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
    "Alef"  : 0,
    "Ayin"  : 1,
    "Bet"   : 2,
    "Dalet" : 3,
    "Gimel" : 4,
    "He"    : 5,
    "Het": 6,
    "Kaf": 7,
    "Kaf-final": 8,
    "Lamed": 9,
    "Mem": 10,
    "Mem-medial": 11,
    "Nun-final": 12,
    "Nun-medial": 13,
    "Pe": 14,
    "Pe-final": 15,
    "Qof": 16,
    "Resh": 17,
    "Samekh": 18,
    "Shin": 19,
    "Taw": 20,
    "Tet": 21,
    "Tsadi-final": 22,
    "Tsadi-medial": 23,
    "Waw": 24,
    "Yod": 25,
    "Zayin": 26,
}

print datetime.datetime.now().time()

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
ap.add_argument("-m", "--model", required=True,
	help="path to output model")
args = vars(ap.parse_args())

EPOCHS = 25
INIT_LR = 1e-3
BS = 32

# load images
print("[INFO] loading images...")
trainData = []
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

(trainX, testX, trainY, testY) = train_test_split(imagePaths, allLabel, test_size=0.25, random_state=42)

print len(trainY), len(testY)

#UNCOMMENT FOR FIT_GENERATOR()
# trainLabel = []
# for imagePath in trainX:
#     label = imagePath.split(os.path.sep)[-2]
#     trainLabel.append(char_map[label])
#
# trainLabel = np.array(trainLabel)
# trainLabel = to_categorical(trainLabel, num_classes=27)
# trainX = np.array(trainX)
#
# testData = []
# testLabel = []
# for imagePath in testX:
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
# testLabel = to_categorical(testLabel, num_classes=27)
# # testX = np.array(testX)

# def load_image(img_path, target_size=(28, 28)):
#     image = cv2.imread(imagePath)
#     image = cv2.resize(image, target_size)
#     return img_to_array(image) #converts image to numpy array
#
# def IMDB_WIKI(X_samples, y_samples, batch_size=100):
#     while(True):
#         batch_size = len(X_samples) / batch_size
#         X_batches = np.split(X_samples, batch_size)
#         y_batches = np.split(y_samples, batch_size)
#         for b in range(len(X_batches)):
#             x = np.array(map(load_image, X_batches[b]),dtype="float") / 255.0
#             y = np.array(y_batches[b])
#             yield x, y
#             # yield X_batches[b], y_batches[b]
# UNCOMMENT FOR FIT_GENERATOR()

# UNCOMMENT FOR FIT()
trainLabel = []
for imagePath in trainX:
    # load the image, pre-process it, and store it in the data list
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (28, 28))
    image = img_to_array(image)
    trainData.append(image)

    label = imagePath.split(os.path.sep)[-2]
    trainLabel.append(char_map[label])

trainData = np.array(trainData, dtype="float") / 255.0
trainLabel = np.array(trainLabel)
trainLabel = to_categorical(trainLabel, num_classes=27)

testData = []
testLabel = []
for imagePath in testX:
    # load the image, pre-process it, and store it in the data list
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (28, 28))
    image = img_to_array(image)
    testData.append(image)

    label = imagePath.split(os.path.sep)[-2]
    testLabel.append(char_map[label])

testData = np.array(testData, dtype="float") / 255.0
testLabel = np.array(testLabel)
testLabel = to_categorical(testLabel, num_classes=27)
# UNCOMMENT FOR FIT()

# initialize the model
print("[INFO] compiling model...")
model = LeNet.build(width=28, height=28, depth=3, classes=27)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
              metrics=["accuracy"])

# train the network
print("[INFO] training network...")
# generator = IMDB_WIKI(trainX, trainLabel, batch_size=16)
# model.fit_generator(generator, validation_data=(testData, testLabel), epochs=100,
#                     steps_per_epoch=1, verbose=1, use_multiprocessing=True)
model.fit(trainData, trainLabel, validation_data=(testData, testLabel), epochs=5, verbose=1)

# save the model to disk
print("[INFO] serializing network...")
model.save(args["model"])

print datetime.datetime.now().time()












# valgenerator = IMDB_WIKI(testX, testLabel, batch_size=1864)
# model.fit_generator(generator, validation_data=valgenerator, validation_steps=8, epochs=1,
#                     steps_per_epoch=8, verbose=1, use_multiprocessing=True)
