#!/bin/sh
sudo /etc/init.d/motion stop # Pysäytetään motion
sleep .5 
/usr/bin/raspistill -o /home/pi/motionkuvat/keskusta.jpg # Otetaan kuva
sudo /etc/init.d/motion start # Käynnistetään motion uudelleen
