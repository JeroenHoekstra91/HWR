import numpy as np
from scipy.signal import savgol_filter
from util.visualization import *


def get_local_extrema(matrix, min_value=0, peak_estimation_threshold=None, plot_gradient=False, plot_3d=False):
    gradient = compute_gradient(matrix)
    if peak_estimation_threshold == None:
        peak_estimation = np.average(gradient) - gradient.std()
    else:
        peak_estimation = peak_estimation_threshold(gradient)
    extrema = []

    max_y, max_x = np.where(gradient <= peak_estimation)
    for i in range(len(max_y)):
        if (matrix[max_y[i], max_x[i]] >= min_value):
            extrema.append((max_y[i], max_x[i]))

    if plot_gradient:
        if plot_3d:
            ylabel = "y"
            zlabel = "gradient"
        else:
            ylabel = "gradient"
            zlabel = "z"
        draw_plot(gradient,
                  threshold=peak_estimation,
                  xlabel="x",
                  ylabel=ylabel,
                  zlabel=zlabel,
                  title="Gradient Plot",
                  plot_3d=plot_3d)

    return extrema


def filter_extrema(extrema, character_map):
    filtered = list(extrema)
    for coor in extrema:
        # filter noise extrema
        if character_map[coor[0]][coor[1]] == "Noise":
            filtered.remove(coor)
    return filtered


def smooth(matrix, rounds=5):
    smoothed = matrix.copy()
    for _ in range(rounds):
        try:
            smoothed = savgol_filter(smoothed, 5, 2)
        except:
            pass
        try:
            smoothed = savgol_filter(smoothed, 5, 2, axis=0)
        except:
            pass
    return smoothed


#### HELPER FUNCTIONS ####

def compute_gradient(matrix):
    nabla = np.gradient(matrix)
    dy = np.abs(nabla[0])
    dx = np.abs(nabla[1])
    return dx + dy
