#### CNN SETTINGS ####
cnn_model = "cnn/models/ModelTrainedWithNoise.model"
topN = 3									# Use the top N character predictions
image_file = "data/words/EDITED.png"

#### N-GRAM SETTINGS ####
bayesian_model = "ngrams/models/bayes_classifier.p"

#### SLIDING WINDOW SETTINGS ####
window_size = 50
step_size = 1
visualize_sliding_window = False

#### EXTREMA CALCULATION SETTINGS ####
smoothing_rounds = 0						# level of smoothing of the confidence map
extreme_min_value = 0						# minimal confidence score filter
extreme_peak_estimation_threshold = 0.001	# determines what is considered an extreme in the gradient

#### GROUPING SETTINGS ####
min_group_size = 1
max_pixel_distance = 1