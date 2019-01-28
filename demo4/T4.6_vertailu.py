#!/usr/bin/python
# -*- coding: utf-8 -*-
# TIEA345 demo4
# lailpimi
# Vertailuun aikalailla kopioitu OpenCV dokumentaatiosta

import numpy as np
import cv2
import matplotlib.pyplot as plt

img1 = cv2.imread('T4.6_kuva1.jpg',0) # queryImage
img2 = cv2.imread('T4.6_kuva2.jpg',0) # trainImage

# Initiate ORB detector
orb = cv2.ORB_create()

# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# Match descriptors.
matches = bf.match(des1,des2)
# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

# Piirretään vain ekat 20 matchia että saa selvää
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:20],None,flags=2)

plt.imsave('T4.6_tulos.png',img3) # Kuva johon havainnot on piirretty