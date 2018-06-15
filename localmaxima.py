import numpy as np
from scipy.signal import savgol_filter

"""
creates numpy grid with a two dimensional hyperbola (kind of a cone)

array([[ 3.6,  5. ,  6. ,  6.6,  6.8,  6.6,  6. ,  5. ,  3.6],
       [ 5. ,  6.4,  7.4,  8. ,  8.2,  8. ,  7.4,  6.4,  5. ],
       [ 6. ,  7.4,  8.4,  9. ,  9.2,  9. ,  8.4,  7.4,  6. ],
       [ 6.6,  8. ,  9. ,  9.6,  9.8,  9.6,  9. ,  8. ,  6.6],
       [ 6.8,  8.2,  9.2,  9.8, 10. ,  9.8,  9.2,  8.2,  6.8],
       [ 6.6,  8. ,  9. ,  9.6,  9.8,  9.6,  9. ,  8. ,  6.6],
       [ 6. ,  7.4,  8.4,  9. ,  9.2,  9. ,  8.4,  7.4,  6. ],
       [ 5. ,  6.4,  7.4,  8. ,  8.2,  8. ,  7.4,  6.4,  5. ],
       [ 3.6,  5. ,  6. ,  6.6,  6.8,  6.6,  6. ,  5. ,  3.6]])
"""
def create_grid(center=5, maximum=10, noise_level=0):
	matrix = np.zeros((9, 9))
	for i in range(9):
		for j in range(9):
			yy = j + 1
			xx = i + 1

			noise = np.random.random(1)[0] * noise_level
			distance = pow(pow(xx-center,2) + pow(yy-center,2) , .5)
			matrix[j, i] = (maximum - pow(distance, 2) * .2) + noise
	return matrix

def compute_gradient(matrix):
	nabla = np.gradient(matrix)
	dy = np.abs(nabla[0])
	dx = np.abs(nabla[1])
	return dx + dy

def smooth(matrix, rounds=5):
	smoothed = matrix.copy()
	for _ in range(rounds):
		smoothed = savgol_filter(smoothed,5,2)
		smoothed = savgol_filter(smoothed,5,2, axis=0)
	return smoothed

def get_local_extrema(matrix, threshold=0, peak_estimation_threshold=0.001):
	gradient = compute_gradient(matrix)
	extrema = []

	max_y, max_x = np.where(gradient <= peak_estimation_threshold)
	for i in range(len(max_y)):
		if(matrix[max_y[i], max_x[i]] >= threshold):
			extrema.append((max_y[i], max_x[i]))

	return extrema