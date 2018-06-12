import numpy as np
import cv2
from cnn.cnn import CNN

transcript = []
cnn = CNN('cnn/ModelTrainedWithNoise.model')
file = open("output.txt", "w")

def analyze_word_segment(word_segment, window_size=50, step_size=2, visualize=False):
    segment_height = len(word_segment)
    segment_width = len(word_segment[0])

    window_size = np.min((window_size, segment_width, segment_height))
    window_x = 0
    window_y = 0

    x_iterations = int(np.ceil((segment_width - window_size) / (step_size * 1.0)))
    y_iterations = int(np.ceil((segment_height - window_size) / (step_size * 1.0)))

    confidence_map = np.zeros_like(word_segment)

    # Slide window and analyze the character
    for i in range(y_iterations):
        # transcript[i] = ""
        for j in range(x_iterations):
            window = word_segment[window_y:(window_size + window_y), window_x:(window_size + window_x)]
            analyze_character(window, visualize=visualize)
            window_x += step_size
        window_x = 0
        window_y += step_size
        file.write("\n")

    file.close()

    if visualize:
        cv2.destroyAllWindows()


def analyze_character(window, visualize=False):
    if visualize:
        cv2.imshow("Test", window)
        cv2.waitKey(100)
    else:
        total, results = cnn.analyze_character(window)
        results = sorted(results.items(), reverse=True)
        file.write(str(total)+str(results)+"\n")

# Do something interesting with the character image
