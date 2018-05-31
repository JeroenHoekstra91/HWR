from keras.preprocessing.image import img_to_array
from keras.models import load_model
import cv2
import numpy as np
import argparse
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

confusionmap = np.zeros((27, 27), dtype = np.uint8)

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
ap.add_argument("-m", "--model", required=True,
	help="path to output model")
args = vars(ap.parse_args())

imagePaths = []
for root, dirs, files in os.walk(args["dataset"]):
    for name in files:
        imagePaths.append(os.path.join(root, name))

labels = []
for imagePath in imagePaths:
    label = imagePath.split(os.path.sep)[-2]
    labels.append(label)

# load the trained convolutional neural network
print("[INFO] loading network...")
model = load_model(args["model"])

loss = 0.0
for i in range(len(imagePaths)):
	# load the image
	image = cv2.imread(imagePaths[i])

	# pre-process the image for classification
	image = cv2.resize(image, (28, 28))
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	# classify the input image
	prediction = list(model.predict(image)[0])
	argmax = np.argmax(prediction)
	predicted_label = char_map.keys()[char_map.values().index(argmax)]

	print("Should be: %s -> Predicted: %s" % (labels[i], predicted_label))

	confusionmap[char_map[labels[i]], argmax] += 1

	if not predicted_label == labels[i]:
		loss = loss + 1

print("\nSample size: %i" % (len(imagePaths)))
print("Total loss: %i" % (loss))
print("Accuracy: " + str(100 - loss/len(imagePaths)*100) + "%")
print("Loss:" + str(loss/len(imagePaths)*100) + "%")

print("\nConfusion Map:")
print(confusionmap)