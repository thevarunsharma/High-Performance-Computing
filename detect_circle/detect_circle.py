import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

original_image = cv2.imread(sys.argv[1])
original_image[original_image < 128] = 0
original_image[original_image >=128] = 255

def get_diff(img1, img2):
    diff = np.abs(img1 - img2).mean()
    return diff <= 0.1

def run_sliding_window(img, radius):
    ref = np.ones((2*radius, 2*radius, 3), 'uint8')*255
    ref = cv2.circle(ref, (radius, radius), radius, (0, 0, 0), 1)
    H, W, _ = img.shape
    for h in range(H-2*radius+1):
        for w in range(W-2*radius+1):
            patch = img[h:h + 2*radius, w:w + 2*radius]
            if get_diff(patch, ref):
                return (h + radius, w + radius)
    return None

def detect_circle(img):
    H, W, _ = img.shape
    for r in reversed(range(1, min(W, H)+1)):
        print("Running for radius %d..."%r)
        op = run_sliding_window(img, r)
        if op is not None:
            return (*op, r)
    return None

circle_loc = detect_circle(original_image)
if circle_loc is None:
    print("No circle detected")
else:
    print("Circle located at (%d, %d) with radius %d"%circle_loc)
