from util.sliding_window import *
from util.visualization import draw_plot
import numpy as np

def get_image_histogram(image):
    histogram = np.zeros((1,len(image[0])))
    for i in range(len(image[0])):
        histogram[0,i] = np.sum(image[:,i]) / 3
    return histogram

def get_character_coordinates(image, character_map, confidence_map, threshold=None, min_confidence=0,
    window_size=50, step_size=1, plot_histogram=False):

    if threshold == None:
        threshold = lambda x: np.average(x)-x.std()

    histogram = get_image_histogram(image)
    if plot_histogram:
        draw_plot(histogram, threshold=threshold(histogram), title="Image Histogram")
    
    filtered_bins = _filter_histogram(histogram, threshold=threshold)
    coordinates, filtered_coordinates = [], []
    prev_x = -100
    
    for i  in range(len(filtered_bins)):
        if _distance(prev_x, 0, filtered_bins[i], 0) > 1:
            coordinates.append([])
            filtered_coordinates.append([])
        prev_x = filtered_bins[i]

        for j in range(window_size / 2, len(image) - window_size / 2):
            coordinate = image_coordinate_to_map_coordinate(j, filtered_bins[i], 
                window_size=window_size, step_size=step_size)
            coordinates[-1].append(coordinate)
            
            if get_confidence(coordinate, character_map, confidence_map) < min_confidence:
                continue    
            filtered_coordinates[-1].append(coordinate)
    return coordinates, filtered_coordinates

#### HELPER FUNCTIONS ####

def _filter_histogram(histogram, threshold=None):
    if threshold == None:
        threshold = lambda x: np.average(x)-x.std()
    return np.where(histogram <= threshold(histogram))[1]

def _distance(x, y, xx, yy):
    return pow(pow(x - xx, 2) + pow(y - yy, 2), .5)