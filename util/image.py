import numpy as np
import cv2

def pad_image(image, padding=5, window_size=50, step_size=1):
	top, bottom = 0, 0
	if len(image) < window_size + step_size:
		top = int(np.ceil((step_size + window_size - len(image)) / 2.0))
		bottom = top
	return cv2.copyMakeBorder(image, top, bottom, padding, padding, cv2.BORDER_CONSTANT, value=(255,255,255))