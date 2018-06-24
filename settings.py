import numpy as np

#### CNN SETTINGS ####
cnn_model = "cnn/models/ModelTrainedWithNoise.model"
topN = 3												# Use the top N character predictions
image_file = "data/words/EDITED.png"
image_padding = 5

#### N-GRAM SETTINGS ####
bayesian_model = "ngrams/models/bayes_classifier.p"
ngrams_likelihood_threshold = 0.0						# determines the minimal ngrams likelihood for filtering transcripts

#### SLIDING WINDOW SETTINGS ####
window_size = 50
step_size = 1
visualize_sliding_window = False
sliding_window_delay = 20								# determines the sliding window visualization speed

#### EXTREMA CALCULATION SETTINGS ####
smoothing_rounds = 0									# level of smoothing of the confidence map
extreme_min_value = lambda x: np.average(x) + x.std()	# minimal confidence score filter
visualize_extrema = False
extrema_file_path = "extrema/"							# determines where to store the extrema window images
plot_gradient = False
plot_confidence = False
plot_3d = False

#### GROUPING SETTINGS ####
min_group_size = 1
max_pixel_distance = 1									# determines what is considered a neighbouring window
max_windows = 450										# prevents the window grouping algorithm from stalling
min_character_distance = window_size/2					# determines when a window group is considered overlapping

#### OUTPUT_FILE ####
txt_output_filename = "Hebrew"