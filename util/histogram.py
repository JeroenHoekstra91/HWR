from util.sliding_window import image_coordinate_to_map_coordinate
import numpy as np

def get_image_histogram(image):
    histogram = np.zeros((1,len(image[0])))
    for i in range(len(image[0])):
        histogram[0,i] = np.sum(image[:,i]) / 3
    return histogram

def get_histogram_gradient(histogram):
    return abs(np.diff(histogram))

def filter_histogram(histogram, threshold=None):
    if threshold == None:
        threshold = lambda x: np.average(x)-x.std()
    return np.where(histogram <= threshold(histogram))[1]

def get_character_coordinates(image, threshold=None, window_size=50, step_size=1):
    histogram = get_image_histogram(image)
    filtered_bins = filter_histogram(histogram, threshold=threshold)
    coordinates = []
    
    for i  in range(len(filtered_bins)):
        for j in range(window_size / 2, len(image) - window_size / 2):
            coordinate = image_coordinate_to_map_coordinate(j, filtered_bins[i], 
                window_size=window_size, step_size=step_size)
            coordinates.append(coordinate)

    return coordinates

def filter_character_coordinates(character_coordinates, character_map):
    filtered = list(character_coordinates)
    for coor in character_coordinates:
        # filter noise coordinates
        if character_map[coor[0]][coor[1]] == "Noise":
            filtered.remove(coor)
    return filtered

