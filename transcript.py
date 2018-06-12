import numpy as np
import cv2
from cnn.cnn import CNN

cnn = CNN('cnn/ModelTrainedWithNoise.model')
topN = 3

def analyze_word_segment(word_segment, window_size=50, step_size=2, visualize=False):
    segment_width = len(word_segment[0])
    segment_height = len(word_segment)

    window_size = np.min((window_size, segment_width, segment_height))
    window_x = 0
    window_y = 0

    x_iterations = int(np.ceil((segment_width - window_size) / (step_size * 1.0)))
    y_iterations = int(np.ceil((segment_height - window_size) / (step_size * 1.0)))

    confidence_map = [np.zeros((segment_height, segment_width)) for _ in range(topN)]
    character_map = [[['' for _ in range (segment_width)] for _ in range(segment_height)] for _ in range(topN)]

    # Slide window and analyze the character
    for i in range(y_iterations):
        for j in range(x_iterations):
            window = word_segment[window_y:(window_size + window_y), window_x:(window_size + window_x)]
            results = analyze_character(window, visualize=visualize)
            
            for k in range(len(results)):
            	xx = window_x + int(np.floor(window_size / 2.0)) - 1
            	yy = window_y + int(np.floor(window_size / 2.0)) - 1
            	confidence_map[k][yy, xx] = results[k][0]
            	character_map[k][yy][xx] = results[k][1][0]

            window_x += step_size    
        window_x = 0
        window_y += step_size

    if visualize:
        cv2.destroyAllWindows()

    return confidence_map, character_map


def analyze_character(window, visualize=False):
    if visualize:
        cv2.imshow("Test", window)
        cv2.waitKey(100)
    else:
        total, results = cnn.analyze_character(window)
        results = sorted(results.items(), reverse=True)[:topN]
        # perhaps threshold on total score?
        return results
