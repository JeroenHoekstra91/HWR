from settings import *
from util.sliding_window import *
from util.gradient import *
from util.visualization import *
from cnn.cnn import CNN
from ngrams.ngrams import Ngrams

image = cv2.imread(image_file)
cnn = CNN(cnn_model)

confidence_map, character_map = slide_window(image,
	cnn, 
	window_size=window_size,
	step_size=step_size,
	topN=topN,
	visualize=visualize_sliding_window,
	sliding_window_delay=sliding_window_delay)

window_groups, filtered_window_groups = [],[]
for i in range(len(confidence_map)):
	print "CONFIDENCE_LEVEL: %d" % (i + 1)
	
	smoothed_confidence_map = smooth(confidence_map[i],
		rounds=smoothing_rounds)
	extrema = get_local_extrema(confidence_map[i],
		min_value=extreme_min_value, 
		peak_estimation_threshold=extreme_peak_estimation_threshold)
	filtered_extrema = filter_extrema(extrema, character_map[i])

	window_groups.append(get_window_groups(filtered_extrema,
		character_map[i],
		window_size=window_size,
		step_size=step_size,
		min_group_size=min_group_size,
		max_pixel_distance=max_pixel_distance,
		max_windows=max_windows))
	filtered_window_groups.append(filter_window_groups(window_groups[i],
		window_size=window_size,
		min_character_distance=min_character_distance))

	for group in filtered_window_groups[i]:
		print "Character %d" % (filtered_window_groups[i].index(group) + 1)
		print_character_confidence(group, confidence_map[i], character_map[i])
	if len(filtered_window_groups[i]) == 0:
		print "\tNo characters determined"