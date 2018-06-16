from settings import *
from util.sliding_window import *
from util.gradient import *
from util.visualization import *
from cnn.cnn import CNN
from ngrams.ngrams import Ngrams

image = cv2.imread(image_file)
cnn = CNN(cnn_model)
if plot_3d:
	ylabel = "y"
	zlabel = "confidence"
else:
	ylabel = "confidence"
	zlabel = "z"


confidence_map, character_map = slide_window(image,
	cnn, 
	window_size=window_size,
	step_size=step_size,
	topN=topN,
	visualize=visualize_sliding_window,
	sliding_window_delay=sliding_window_delay)

window_groups, filtered_window_groups, transcript = [],[],[]
for i in range(len(confidence_map)):
	print "CONFIDENCE_LEVEL: %d" % (i + 1)
	transcript.append("")
	
	if plot_confidence:
		draw_plot(confidence_map[i], 
			threshold=extreme_min_value, 
			xlabel="x", 
			ylabel=ylabel,
			zlabel=zlabel, 
			title="Confidence Plot",
			threshold_label="minimal confidence",
			plot_3d=plot_3d)

	smoothed_confidence_map = smooth(confidence_map[i],
		rounds=smoothing_rounds)
	extrema = get_local_extrema(smoothed_confidence_map,
		min_value=extreme_min_value, 
		peak_estimation_threshold=extreme_peak_estimation_threshold,
		plot_gradient=plot_gradient,
		plot_3d=plot_3d)
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
		transcript[i] += character_map[i][group[0][0]][group[0][1]] + " "
		
		print "Character %d" % (filtered_window_groups[i].index(group) + 1)
		print_character_confidence(group, confidence_map[i], character_map[i])
	if len(filtered_window_groups[i]) == 0:
		print "\tNo characters determined"

	transcript[i] = transcript[i].strip()