from settings import *
from util.sliding_window import *
from util.gradient import *
from util.visualization import *
from cnn.cnn import CNN

image = cv2.imread(image_file)
cnn = CNN(cnn_model)

confidence_map, character_map = slide_window(image,
	cnn, 
	window_size=window_size,
	step_size=step_size,
	visualize=visualize_sliding_window)

smoothed_confidence_map = smooth(confidence_map[0], rounds=smoothing_rounds)
extrema = get_local_extrema(confidence_map[0],
	min_value=extreme_min_value, 
	peak_estimation_threshold=extreme_peak_estimation_threshold)
filtered_extrema = filter_extrema(extrema, character_map[0])

window_groups = get_window_groups(filtered_extrema,
	window_size=window_size,
	step_size=step_size,
	min_group_size=min_group_size,
	max_pixel_distance=max_pixel_distance)
filtered_window_groups = filter_window_groups(window_groups,
	window_size=window_size)

for group in filtered_window_groups:
	print "Character %d" % (filtered_window_groups.index(group))
	print_character_confidence(group, confidence_map[0], character_map[0])