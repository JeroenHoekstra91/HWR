from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2


class CNN():
    model = None
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

    def __init__(self, model_path):
        print("[INFO] loading network...")
        self.model = load_model(model_path)

    def analyze_character(self, loaded_image):
        total = 0

        # image = cv2.imread(loaded_image)
        image = loaded_image
        image = cv2.resize(image, (28, 28))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)

        prediction = list(self.model.predict(image)[0])
        results = {}

        for i in range(len(prediction)):
            label = sorted(self.char_map.keys())[i]
            total += prediction[i]

            if prediction[i] in results.keys():
                results[prediction[i]].append(label)
            else:
                results[prediction[i]] = [label]

        return total, results
