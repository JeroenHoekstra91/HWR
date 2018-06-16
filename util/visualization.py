import numpy as np
import cv2
import matplotlib.pyplot as plt

def draw_extrema(extrema, image, character_map, out="extrema/", window_size=50, step_size=1):
	for coor in extrema:
		font = cv2.FONT_HERSHEY_SIMPLEX
		label = character_map[coor[0]][coor[1]]
		image_extreme = image.copy()
		image_coor = _map_coordinate_to_image_coordinate(coor[0], coor[1],
			window_size=window_size, step_size=step_size)
		filename = out + label + "(" + str(image_coor[1]) + ", " + str(image_coor[0]) + ").png"

		xx = int(image_coor[1] - window_size/2.0)
		yy = int(image_coor[0] - window_size/2.0)
		
		cv2.rectangle(image_extreme,(xx,yy),(xx+window_size,yy+window_size),(0,0,255),1)
		cv2.putText(image_extreme, label, (1,len(image)-5), font, .5,(0,0,255),1,cv2.LINE_AA)
		cv2.imwrite(filename, image_extreme)

def draw_plot(matrix, threshold=None):
	line_type = ('b-', 'g--', 'm-.', 'c:')
	for i in range(4):
		y = len(matrix)/4*i
		plt.plot(matrix[y,:], line_type[i])

	if threshold != None:
		t = np.ones((len(matrix[0]),)) * threshold
		plt.plot(t, 'r--')

	plt.show()

def print_character_confidence(extrema, confidence_map, character_map):
	d = _get_character_confidence(extrema, confidence_map, character_map)
	for key in d.keys():
		print key + "]"
		print "\tavg: " + str(np.average(d[key]))
		print "\tmin: " + str(np.min(d[key]))
		print "\tmax: " + str(np.max(d[key]))
		print "\tcount: " + str(len(d[key])) + " instances"

#### HELPER FUNCTIONS ####

def _get_character_confidence(extrema, confidence_map, character_map):
	character_confidence = {}
	for coor in extrema:
		char = character_map[coor[0]][coor[1]]
		confidence = confidence_map[coor[0], coor[1]]
		if char in character_confidence.keys():
			character_confidence[char].append(confidence)
		else:
			character_confidence[char] = [confidence]
	return character_confidence