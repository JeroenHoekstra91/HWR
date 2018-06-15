import numpy as np
import cv2
from cnn.cnn import CNN
from localmaxima import *

cnn = CNN('cnn/ModelTrainedWithNoise.model')
topN = 3

def analyze_word_segment(word_segment, window_size=50, step_size=1, visualize=False):
	segment_width = len(word_segment[0])
	segment_height = len(word_segment)

	window_size = np.min((window_size, segment_width, segment_height))
	window_x = 0
	window_y = 0

	x_iterations = int(np.ceil((segment_width - window_size) / (step_size * 1.0))) + 1
	y_iterations = int(np.ceil((segment_height - window_size) / (step_size * 1.0))) + 1

	map_width = x_iterations
	map_height = y_iterations
	confidence_map = [np.zeros((map_height, map_width)) for _ in range(topN)]
	character_map = [[['' for _ in range (map_width)] for _ in range(map_height)] for _ in range(topN)]

	# Slide window and analyze the character
	for i in range(y_iterations):
		for j in range(x_iterations):
			window = word_segment[window_y:(window_size + window_y), window_x:(window_size + window_x)]
			results = analyze_character(window, visualize=visualize)
			
			for k in range(len(results)):
				xx = window_x / step_size
				yy = window_y / step_size				
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

	total, results = cnn.analyze_character(window)
	results = sorted(results.items(), reverse=True)[:topN]
	# perhaps threshold on total score?
	return results

def map_coordinate_to_image_coordinate(x, y, window_size=50, step_size=1):
	xx = x*step_size + window_size/2.0
	yy = y*step_size + window_size/2.0
	return xx, yy

def filter_extremes(extremes, character_map):
	filtered = list(extremes)
	for coor in extremes:
		# filter noise extremes
		if character_map[coor[0]][coor[1]] == "Noise":
			filtered.remove(coor)
	return filtered

def get_character_confidence(extremes, confidence_map, character_map):
	character_confidence = {}
	for coor in extremes:
		char = character_map[coor[0]][coor[1]]
		confidence = confidence_map[coor[0], coor[1]]
		if char in character_confidence.keys():
			character_confidence[char].append(confidence)
		else:
			character_confidence[char] = [confidence]
	return character_confidence

def print_character_confidence(extremes, confidence_map, character_map):
	d = get_character_confidence(extremes, confidence_map, character_map)
	for key in d.keys():
		print key + "]"
		print "\tavg: " + str(np.average(d[key]))
		print "\tmin: " + str(np.min(d[key]))
		print "\tmax: " + str(np.max(d[key]))
		print "\tcount: " + str(len(d[key]))

def draw_extremes(extremes, image, confidence_map, character_map, out="extremes/", window_size=50, step_size=1):
	for coor in extremes:
		font = cv2.FONT_HERSHEY_SIMPLEX
		label = character_map[coor[0]][coor[1]]
		image_extreme = image.copy()
		image_coor = map_coordinate_to_image_coordinate(coor[0], coor[1],
			window_size=window_size, step_size=step_size)
		filename = out + label + "(" + str(image_coor[1]) + ", " + str(image_coor[0]) + ").png"

		xx = int(image_coor[1] - window_size/2.0)
		yy = int(image_coor[0] - window_size/2.0)
		
		cv2.rectangle(image_extreme,(xx,yy),(xx+window_size,yy+window_size),(0,0,255),1)
		cv2.putText(image_extreme, label, (1,len(image)-5), font, .5,(0,0,255),1,cv2.LINE_AA)
		cv2.imwrite(filename, image_extreme)

#### WINDOW GROUPS ######################

def get_window_groups(extremes, window_size=50, step_size=1, min_group_size=1, max_pixel_distance=1):
	elements = len(extremes)
	m = np.zeros((elements, elements))
	max_distance = pow(pow(max_pixel_distance,2)*2,.5)

	# Create group grid.
	for i in range(elements):
		for j in range(elements):
			coor1 = map_coordinate_to_image_coordinate(extremes[i][0], extremes[i][1],
				window_size=window_size, step_size=step_size)
			coor2 = map_coordinate_to_image_coordinate(extremes[j][0], extremes[j][1],
				window_size=window_size, step_size=step_size)

			if distance(coor1[0], coor1[1], coor2[0], coor2[1]) < max_distance:
				members = np.where(m[j,:] == 1)[0]
				for member in members:
					m[i, member] = 1
					m[member, i] = 1
				m[i,j] = 1
				m[j,i] = 1

	# Create group list
	groups = []
	for i in range(elements):
		if m.shape[1] == 0:
			break
		if m[i, :].sum() < min_group_size:
			continue

		members = np.where(m[i, :] == 1)
		group = []

		for member in members[0]:
			group.append(extremes[member])

		m[:,members[0]] = 0
		groups.append(group)
	return groups
	
def print_group_labels(group, character_map):
	for member in group:
		print character_map[member[0]][member[1]]

def get_group_center(group):
	total = [0,0]
	for member in group:
		total[0] += member[0]
		total[1] += member[1]
	return total[0]/len(group), total[1]/len(group)

def filter_groups(groups, window_size=50):
	remove = []
	for group1 in groups:
		if group1 in remove:
			continue

		for  group2 in groups:
			if group1 == group2:
				continue
			center1 = get_group_center(group1)
			center2 = get_group_center(group2)

			if distance(0, center1[1], 0, center2[1]) < window_size/2:
				if len(group1) > len(group2):
					remove.append(group2)
				else:
					remove.append(group1)
	return [group for group in groups if group not in remove]