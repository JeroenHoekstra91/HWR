import cv2

def pad_image(image, padding=5):
	return cv2.copyMakeBorder(image, 0, 0, padding, padding, cv2.BORDER_CONSTANT, value=(255,255,255))