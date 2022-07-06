from turtle import width
import cv2 as cv
import numpy as np

HEIGHT = 512
WIDTH = 256
running = True

img = np.zeros((WIDTH, HEIGHT, 3), np.uint8)


cv.rectangle(img, (64, 64), (128, 128), (220, 240, 20), 3)

cv.imshow("drawing", img)
cv.waitKey(0)
