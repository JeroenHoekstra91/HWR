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

# def transcribe(image_file):
image = cv2.imread("data/MapStructure/Taw_Kaf_Yod_Alef.jpeg")
image = pad_image(image, padding=image_padding)
confidence_map, character_map = slide_window(image,
    cnn,
    window_size=window_size,
    step_size=step_size,
    topN=topN,
    visualize=visualize_sliding_window,
    sliding_window_delay=sliding_window_delay)

character_coordinates, filtered_character_coordinates, window_groups, transcripts = [], [], [], []
for i in range(len(confidence_map)):
    print "\nCONFIDENCE_LEVEL: %d\n" % (i + 1)

    # Calculates character positions using an image histogram.
    coordinates, filtered_coordinates = get_character_coordinates(image,
        character_map[i],
        threshold=histogram_threshold,
        window_size=window_size,
        step_size=step_size,
        plot_histogram=plot_histogram)
    character_coordinates.append(coordinates)
    filtered_character_coordinates.append(filtered_coordinates)
    if show_information_loss:
        print_information_loss(filtered_character_coordinates[i], confidence_map[i], confidence_map[i],
            operation_label="getting character coordinates")
    
    # Groups windows based on proximity and cnn determined label.
    window_groups.append([])
    for character_position in filtered_character_coordinates[i]:
        window_groups[i].append(get_window_groups(character_position,
            character_map[i],
            window_size=window_size,
            step_size=step_size,
            min_group_size=min_group_size,
            max_pixel_distance=max_pixel_distance,
            max_windows=max_windows))
    if show_information_loss:
        print_information_loss(window_groups[i], filtered_character_coordinates[i], confidence_map[i],
            operation_label="creating window groups")

    # Generate and filter possible transcripts.
    # transcripts.append(generate_transcripts(ngrams_model,
    #     window_groups[i],
    #     character_map[i],
    #     confidence_map[i],
    #     ngrams_depth=ngrams_depth,
    #     ngrams_weights=ngrams_weights))
#     filtered_transcripts.append(filter_transcripts(transcripts[i],
#         ngrams_likelihood_threshold=ngrams_likelihood_threshold))

#     if show_transcripts:
#         print_transcripts(filtered_transcripts[i])

# sort_by_relevance(filtered_transcripts, cnn_confidence_weight, ngrams_likelihood_weight)
# try: return filtered_transcripts[0][0]['word']
# except: return ""

# image_files = listdir(word_segment_images_directory)
# transcripts = []
# accuracy_sum = 0.0
# for image in image_files:
#     label = " ".join(".".join(image.split(".")[:-1]).split("_"))
#     transcript = transcribe(word_segment_images_directory + image)
#     accuracy = jellyfish.jaro_distance(
#         to_flat(label).decode('unicode-escape'),
#         to_flat(transcript).decode('unicode-escape'))
#     accuracy_sum += accuracy

#     transcripts.append({
#         "label": label,
#         "transcript": transcript,
#         "accuracy": accuracy
#         })

# print "average accuracy: " + str(accuracy_sum / len(image_files) * 100.0) + "%"