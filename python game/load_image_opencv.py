import argparse
import cv2
import pygame

# from photo_editor import screen
#
# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image")
# args = vars(ap.parse_args())
#
# # load the image from disk via "cv2.imread" and then grab the spatial
# # dimensions, including width, height, and number of channels
# image = cv2.imread(args["image"])
#
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# pygame_image = pygame.image.frombuffer(image.tobytes(), image.shape[:2][::-1], "RGB")
#
# screen.blit(pygame_image, (0, 0))
# (h, w, c) = image.shape[:3]
# # display the image width, height, and number of channels to our
# # terminal
# print("width: {} pixels".format(w))
# print("height: {}  pixels".format(h))
# print("channels: {}".format(c))
#
# # show the image and wait for a keypress
# cv2.imshow("Image", image)
# cv2.waitKey(0)
# # save the image back to disk (OpenCV handles converting image
# # filetypes automatically)
# cv2.imwrite("newimage.jpg", image)
# #
