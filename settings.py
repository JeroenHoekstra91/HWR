import numpy as np

#### MISC #####
show_information_loss = False
show_transcripts = False
output_pipeline1 = "pipeline1-output-wordsegments/"
output_pipeline2 = "pipeline2-output-transcripts/"

#### CNN SETTINGS ####
cnn_model = "cnn/models/ModelTrainedWithNoise.model"
cnn_confidence_weight = 1
image_padding = 5

#### N-GRAM SETTINGS ####
bayesian_model = "ngrams/models/bayes_classifier.p"
ngrams_depth = 2
ngrams_likelihood_threshold = 0.0                               # determines the minimal ngrams likelihood for filtering transcripts
ngrams_likelihood_weight = 1
ngrams_weights = [.4,.6]

#### SLIDING WINDOW SETTINGS ####
window_size = 35
step_size = 1
visualize_sliding_window = False
sliding_window_delay = 20                                       # determines the sliding window visualization speed

#### HISTOGRAM SETTINGS ####
histogram_threshold = lambda x: np.average(x) - x.std()
min_confidence = 0
visualize_extrema = False
extrema_file_path = "extrema/"                                  # determines where to store the extrema window images
plot_histogram = False

#### GROUPING SETTINGS ####
min_group_size = 1
max_pixel_distance = 1                                          # determines what is considered a neighbouring window
max_windows = 500                                               # prevents the window grouping algorithm from stalling
