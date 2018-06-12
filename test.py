from transcript import *
# image = cv2.imread("data/examples/segmented1Bet.png")
# image = cv2.imread("data/words/Word#0_Line#2_Parchment#17.png")
image = cv2.imread("data/words/EDITED.png")
    # HE-RESH/DALET
# image = cv2.imread("data/words/Word#0_Line#3_Parchment#13.png")
    # HE-BET-BET-WAW-HET-GIMEL-
# analyze_word_segment(image, visualize=True)
confidence_map, character_map = analyze_word_segment(image, visualize=False)
