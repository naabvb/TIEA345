#!/usr/bin/python
# -*- coding: utf-8 -*-
# TIEA345 demo4
# lailpimi

# Ottaa kuvan ja tunnistaa siitä sitten kasvot

from picamera import PiCamera
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

kamera = PiCamera()

kamera.capture('/home/pi/T4.8_kuva.jpg') # Otetaan kuva

# Ladataan valmiiksi koulutetut tunnistimet kasvoille ja silmille
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml') 
eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')

img = cv.imread('T4.8_kuva.jpg') # Ladataan kuva
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Harmaaksi

# Havaitaan kasvot ja piirretään neliö
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

plt.imsave('T4.8_tulos.png',img) # Kuva johon havainnot on piirretty        
        