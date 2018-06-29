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

def transcribe(image_file):
    image = cv2.imread(image_file)
    image = pad_image(image, padding=image_padding)
    confidence_map, character_map = slide_window(image,
        cnn,
        window_size=window_size,
        step_size=step_size,
        topN=topN,
        visualize=visualize_sliding_window,
        sliding_window_delay=sliding_window_delay)

    filtered_character_coordinates = []
    window_groups, sorted_window_groups, transcripts, filtered_transcripts = [], [], [], []
    for i in range(len(confidence_map)):
        print "\nCONFIDENCE_LEVEL: %d\n" % (i + 1)

        # Calculates character positions using an image histogram.
        character_coordinates.append(get_character_coordinates(image,
            window_size=window_size,
            step_size=step_size))
        if show_information_loss:
            print_information_loss(character_coordinates, confidence_map[i], confidence_map[i],
                operation_label="getting character coordinates")
        filtered_character_coordinates.append(filter_character_coordinates(character_coordinates,
            character_map[i]))
        if show_information_loss:
            print_information_loss(filtered_character_coordinates, character_coordinates, confidence_map[i],
                operation_label="filtering character coordinates")
        if visualize_extrema:
            visualize_extrema_windows(filtered_character_coordinates,
                image,
                character_map[i],
                out=extrema_file_path,
                window_size=window_size,
                step_size=step_size)

        # Groups windows based on proximity and cnn determined label.
        window_groups.append(get_window_groups(filtered_character_coordinates,
            character_map[i],
            window_size=window_size,
            step_size=step_size,
            min_group_size=min_group_size,
            max_pixel_distance=max_pixel_distance,
            max_windows=max_windows))
        if show_information_loss:
            print_information_loss(window_groups[i], character_coordinates, confidence_map[i],
                operation_label="creating window groups")
        sorted_window_groups.append(sort_window_groups(window_groups[i],
            min_character_distance=min_character_distance))
        if show_information_loss:
            print_information_loss(sorted_window_groups[i], window_groups[i], confidence_map[i],
                operation_label="sorting window groups")

        # Generate and filter possible transcripts.
        transcripts.append(generate_transcripts(ngrams_model,
            sorted_window_groups[i],
            character_map[i],
            confidence_map[i],
            ngrams_depth=ngrams_depth,
            ngrams_weights=ngrams_weights))
        filtered_transcripts.append(filter_transcripts(transcripts[i],
            ngrams_likelihood_threshold=ngrams_likelihood_threshold))

        if show_transcripts:
            print_transcripts(filtered_transcripts[i])

    sort_by_relevance(filtered_transcripts, cnn_confidence_weight, ngrams_likelihood_weight)
    try: return filtered_transcripts[0][0]['word']
    except: return ""

image_files = listdir(word_segment_images_directory)
transcripts = []
accuracy_sum = 0.0
for image in image_files:
    label = " ".join(".".join(image.split(".")[:-1]).split("_"))
    transcript = transcribe(word_segment_images_directory + image)
    accuracy = jellyfish.jaro_distance(
        to_flat(label).decode('unicode-escape'),
        to_flat(transcript).decode('unicode-escape'))
    accuracy_sum += accuracy

    transcripts.append({
        "label": label,
        "transcript": transcript,
        "accuracy": accuracy
        })

print "average accuracy: " + str(accuracy_sum / len(image_files) * 100.0) + "%"