from util.sliding_window import image_coordinate_to_map_coordinate
from util.visualization import draw_plot
import numpy as np

def get_image_histogram(image):
    histogram = np.zeros((1,len(image[0])))
    for i in range(len(image[0])):
        histogram[0,i] = np.sum(image[:,i]) / 3
    return histogram

def filter_histogram(histogram, threshold=None):
    if threshold == None:
        threshold = lambda x: np.average(x)-x.std()
    return np.where(histogram <= threshold(histogram))[1]

def get_character_coordinates(image, character_map, threshold=None, window_size=50, step_size=1,
    plot_histogram=False):

    histogram = get_image_histogram(image)
    if plot_histogram:
        draw_plot(histogram, threshold=threshold(histogram), title="Image Histogram")
    
    filtered_bins = filter_histogram(histogram, threshold=threshold)
    coordinates, filtered_coordinates = [], []
    prev_x = -100
    
    for i  in range(len(filtered_bins)):
        if _distance(prev_x, 0, filtered_bins[i], 0) > 1:
            filtered_coordinates.append([])
            coordinates.append([])
        prev_x = filtered_bins[i]

        for j in range(window_size / 2, len(image) - window_size / 2):
            coordinate = image_coordinate_to_map_coordinate(j, filtered_bins[i], 
                window_size=window_size, step_size=step_size)
            if character_map[coordinate[0]][coordinate[1]] != "Noise":
                filtered_coordinates[-1].append(coordinate)
            coordinates[-1].append(coordinate)
    return coordinates, filtered_coordinates

#### HELPER FUNCTIONS ####

def _distance(x, y, xx, yy):
    return pow(pow(x - xx, 2) + pow(y - yy, 2), .5)