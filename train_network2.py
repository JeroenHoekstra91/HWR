# set the matplotlib backend so figures can be saved in the background
import datetime

import matplotlib
from keras.utils import to_categorical
from sklearn.cross_validation import train_test_split

matplotlib.use("Agg")

# import the necessary packages
from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array
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
imagePaths = []
random.seed(42)

for root, dirs, files in os.walk(args["dataset"]):
    for name in files:
        imagePaths.append(os.path.join(root, name))

random.shuffle(imagePaths)
y_sample = []

for imagePath in imagePaths:
    label = imagePath.split(os.path.sep)[-2]
    y_sample.append(char_map[label])

# (trainX, testX, trainY, testY) = train_test_split(imagePaths,
#                                                   y_sample, test_size=0.25, random_state=42)

X_sample = np.array(imagePaths)
y_sample = np.array(y_sample)
y_sample = to_categorical(y_sample, num_classes=27)

def load_image(img_path, target_size=(28, 28)):
    image = cv2.imread(imagePath)
    image = cv2.resize(image, target_size)
    return img_to_array(image) #converts image to numpy array

def IMDB_WIKI(X_samples, y_samples, batch_size=100):
    batch_size = len(X_samples) / batch_size
    X_batches = np.split(X_samples, batch_size)
    y_batches = np.split(y_samples, batch_size)
    for b in range(len(X_batches)):
        x = np.array(map(load_image, X_batches[b]),dtype="float") / 255.0
        y = np.array(y_batches[b])
        yield x, y

# initialize the model
print("[INFO] compiling model...")
model = LeNet.build(width=28, height=28, depth=3, classes=27)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
              metrics=["accuracy"])

# train the network
print("[INFO] training network...")
generator = IMDB_WIKI(X_sample, y_sample, batch_size=176)
model.fit_generator(generator, epochs=1, steps_per_epoch=10, verbose=1)

# save the model to disk
print("[INFO] serializing network...")
model.save(args["model"])

print datetime.datetime.now().time()