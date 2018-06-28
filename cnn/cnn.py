from keras.preprocessing.image import img_to_array
from keras.models import load_model
from util.character_map import char_map
import numpy as np
import cv2

class CNN():
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
            label = sorted(char_map.keys())[i]
            total += prediction[i]

            if prediction[i] in results.keys():
                results[prediction[i]].append(label)
            else:
                results[prediction[i]] = [label]
                
        return total, results