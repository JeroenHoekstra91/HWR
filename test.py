from localmaxima import *
from transcript import *
# image = cv2.imread("data/examples/segmented1Bet.png")
# image = cv2.imread("data/words/Word#0_Line#2_Parchment#17.png")
image = cv2.imread("data/words/EDITED.png")
    # HE-RESH/DALET
# image = cv2.imread("data/words/Word#0_Line#3_Parchment#13.png")
    # HE-BET-BET-WAW-HET-GIMEL-
# analyze_word_segment(image, visualize=True)
confidence_map, character_map = analyze_word_segment(image, visualize=False)

extremes = get_local_extrema(confidence_map[0])
filtered_extremes = filter_extremes(extremes, character_map[0])

window_groups = get_window_groups(filtered_extremes)
filtered_groups = filter_groups(window_groups)

for group in filtered_groups:
	print "Character %d" % (filtered_groups.index(group))
	print_character_confidence(group, confidence_map[0], character_map[0])