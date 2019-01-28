#!/usr/bin/python
# -*- coding: utf-8 -*-
# TIEA345 demo4
# lailpimi

# Tunnistaa kasvot ja silmät.

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# Ladataan valmiiksi koulutetut tunnistimet kasvoille ja silmille
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml') 
eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')

img = cv.imread('T4.7_naama.jpg') # Ladataan kuva
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Harmaaksi

# Havaitaan kasvot ja piirretään neliö
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

plt.imsave('T4.7_tulos.png',img) # Kuva johon havainnot on piirretty        
        