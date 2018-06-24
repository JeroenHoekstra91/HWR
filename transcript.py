from settings import *
from util.sliding_window import *
from util.gradient import *
from util.visualization import *
from util.transcript import *
from util.image import *
from cnn.cnn import CNN
from ngrams.ngrams import Ngrams

image = cv2.imread(image_file)
cnn = CNN(cnn_model)
ngrams_model = Ngrams(bayesian_model)

if plot_3d:
    ylabel = "y"
    zlabel = "confidence"
else:
    ylabel = "confidence"
    zlabel = "z"

image = pad_image(image, padding=image_padding)
confidence_map, character_map = slide_window(image,
    cnn,
    window_size=window_size,
    step_size=step_size,
    topN=topN,
    visualize=visualize_sliding_window,
    sliding_window_delay=sliding_window_delay)

window_groups, sorted_window_groups, transcripts, filtered_transcripts = [], [], [], []
for i in range(len(confidence_map)):
    print "CONFIDENCE_LEVEL: %d" % (i + 1)

    # Smoothes and plots the confidence map.
    smoothed_confidence_map = smooth(confidence_map[i],
        rounds=smoothing_rounds)
    if plot_confidence:
        draw_plot(smoothed_confidence_map,
            threshold=extreme_min_value(smoothed_confidence_map),
            xlabel="x",
            ylabel=ylabel,
            zlabel=zlabel,
            title="Confidence Plot",
            threshold_label="minimal confidence",
            plot_3d=plot_3d)

    # Calculates and visualizes local extrema in the confidence map.
    extrema = get_local_extrema(smoothed_confidence_map,
        min_value=extreme_min_value(smoothed_confidence_map),
        plot_gradient=plot_gradient,
        plot_3d=plot_3d)
    print_information_loss(extrema, smoothed_confidence_map, confidence_map[i],
        operation_label="filtering on extrema")
    filtered_extrema = filter_extrema(extrema, character_map[i])
    print_information_loss(filtered_extrema, extrema, confidence_map[i],
        operation_label="filtering extrema on noise labels")
    if visualize_extrema:
        visualize_extrema_windows(filtered_extrema,
            image,
            character_map[i],
            out=extrema_file_path + "/conf_level_" + str(i) + "/",
            window_size=window_size,
            step_size=step_size)

    # Groups windows based on proximity and cnn determined label.
    window_groups.append(get_window_groups(filtered_extrema,
        character_map[i],
        window_size=window_size,
        step_size=step_size,
        min_group_size=min_group_size,
        max_pixel_distance=max_pixel_distance,
        max_windows=max_windows))
    print_information_loss(window_groups[i], filtered_extrema, confidence_map[i],
        operation_label="creating window groups")
    sorted_window_groups.append(sort_window_groups(window_groups[i],
        min_character_distance=min_character_distance))
    print_information_loss(sorted_window_groups[i], window_groups[i], confidence_map[i],
        operation_label="sorting window groups")

    # Generate and filter possible transcripts.
    transcripts.append(generate_transcripts(ngrams_model,
        sorted_window_groups[i],
        character_map[i],
        confidence_map[i]))
    filtered_transcripts.append(filter_transcripts(transcripts[i],
        ngrams_likelihood_threshold=ngrams_likelihood_threshold))

    for transcript in filtered_transcripts[i]:
        print transcript["word"] + " => " + str(transcript["cnn_confidence_sum"])

sort_by_relevance(filtered_transcripts, cnn_confidence_weight, ngrams_likelihood_weight)
write_to_file(filtered_transcripts[0][0]['word'])