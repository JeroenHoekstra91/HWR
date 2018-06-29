from settings import *
from util.visualization import *
from util.transcript import *
from util.image import *
from util.histogram import *
from cnn.cnn import CNN
from ngrams.ngrams import Ngrams
from os import listdir
from util.character_map import *
import jellyfish

cnn = CNN(cnn_model)
ngrams_model = Ngrams(bayesian_model)

def transcribe(image_file, window_size):
    image = cv2.imread(image_file)
    image = pad_image(image, padding=image_padding)
    window_size = min((window_size, len(image), len(image[0])))

    # should have len(char_map.keys()) lengths!!!!
    confidence_map, character_map = slide_window(image,
        cnn,
        window_size=window_size,
        step_size=step_size,
        visualize=visualize_sliding_window,
        sliding_window_delay=sliding_window_delay)

    # Calculates character positions using an image histogram.
    character_coordinates, filtered_character_coordinates = get_character_coordinates(image,
        character_map,
        confidence_map,
        threshold=histogram_threshold,
        min_confidence=min_confidence,
        window_size=window_size,
        step_size=step_size,
        plot_histogram=plot_histogram)
    if show_information_loss:
        print_information_loss(filtered_character_coordinates, confidence_map[0], confidence_map[0],
            operation_label="getting character coordinates")
    if visualize_extrema:
        visualize_extrema_windows(filtered_character_coordinates,
            image, 
            character_map,
            out=extrema_file_path,
            window_size=window_size,
            step_size=step_size)

    # Groups windows based on proximity and cnn determined label.
    window_groups = []
    for character_position in filtered_character_coordinates:
        window_groups.append(get_window_groups(character_position,
            character_map,
            window_size=window_size,
            step_size=step_size,
            min_group_size=min_group_size,
            max_pixel_distance=max_pixel_distance,
            max_windows=max_windows))
    if show_information_loss:
        print_information_loss(window_groups, filtered_character_coordinates, confidence_map[0],
            operation_label="creating window groups")
    merged_window_groups = merge_window_groups_by_label(window_groups, character_map)
    if show_information_loss:
        print_information_loss(merged_window_groups, window_groups, confidence_map[0],
            operation_label="merging window groups")

    # Generate and filter possible transcripts.
    transcripts = generate_transcripts(ngrams_model,
        window_groups,
        character_map,
        confidence_map,
        ngrams_depth=ngrams_depth,
        ngrams_weights=ngrams_weights)
    filtered_transcripts = filter_transcripts(transcripts,
        ngrams_likelihood_threshold=ngrams_likelihood_threshold)

    if show_transcripts:
        print_transcripts(filtered_transcripts)

    sort_by_relevance(filtered_transcripts, cnn_confidence_weight, ngrams_likelihood_weight)
    try: return filtered_transcripts[0]['word']
    except: return ""

image_files = listdir(word_segment_images_directory)
transcripts = []
accuracy_sum = 0.0
for image in image_files:
    label = " ".join(".".join(image.split(".")[:-1]).split("_"))
    print "analyzing: " + label
    transcript = transcribe(word_segment_images_directory + image, window_size)
    accuracy = jellyfish.jaro_distance(
        to_flat(label).decode('unicode-escape'),
        to_flat(transcript).decode('unicode-escape'))
    accuracy_sum += accuracy

    print label
    print transcript
    print accuracy

    transcripts.append({
        "label": label,
        "transcript": transcript,
        "accuracy": accuracy
        })

print "average accuracy: " + str(accuracy_sum / len(image_files) * 100.0) + "%"