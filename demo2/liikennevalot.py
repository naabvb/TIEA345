#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TIEA345 demo2
# lailpimi

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

AUTO_PUNAINEN = 4 # Asetetaan pinnit
AUTO_KELTAINEN = 17
AUTO_VIHREA = 27

JALANKULKIJA_PUNAINEN = 16
JALANKULKIJA_KELTAINEN = 21
JALANKULKIJA_VIHREA = 20

NAPPI = 19
LIIKETUNNISTIN = 25

def main():
    alustaPinnit()
    alustaValot() # Pistetään autoille vihreä käyntiin
    try: 
        while True:
            if GPIO.input(NAPPI) == 1: # Jos nappia painettiin
                print("Nappia painettiin")
                nappiPainettu()
                alustaValot() # Jalankulkija-osion jälkeen alustetaan taas autoille
            
            time.sleep(0.1)
            
    except KeyboardInterrupt: # CTRL-C pysäyttää ohjelman ja ajaa lopuksi GPIO.cleanup()
        print("loppu")
    GPIO.cleanup()

def nappiPainettu():
    GPIO.output(JALANKULKIJA_KELTAINEN, 1) # Sytytetään ilmoitusvalo
    
    if GPIO.input(LIIKETUNNISTIN) == 1: # Tarkistetaan havaitaanko liikettä
        print(u"Liikettä havaittu")
        time.sleep(6) # Venataan 4 sec jos havaitaan
    
    GPIO.output(AUTO_VIHREA, 0) # Vaihdetaan autoille punaiset valot
    GPIO.output(AUTO_KELTAINEN, 1)
    time.sleep(1)
    GPIO.output(AUTO_KELTAINEN, 0)
    GPIO.output(AUTO_PUNAINEN, 1)
    
    time.sleep(0.5) # Vaihdetaan jalankulkijalle vihreä ja sammutetaan ilmoitusvalo 
    GPIO.output(JALANKULKIJA_PUNAINEN, 0) 
    GPIO.output(JALANKULKIJA_KELTAINEN, 0)
    GPIO.output(JALANKULKIJA_VIHREA, 1)
    
    time.sleep(7) # Odotetaan 7 sec jonka jälkeen valot alustetaan taas autoille
    
# Asetetaan default-valot, jossa liikenteelle tulee vihreät valot. Tätä kutsutaan aina jalankulkijavalojen lopuksi    
def alustaValot():
    GPIO.output(JALANKULKIJA_VIHREA, 0) # Jalankulkijoille vihreä pois
    GPIO.output(JALANKULKIJA_KELTAINEN, 0) # Ilmoitusvalo jalankulkijalle pois
    GPIO.output(JALANKULKIJA_PUNAINEN, 1) # Punainen päälle
    
    GPIO.output(AUTO_VIHREA, 0) # Ensin vihreä pois
    GPIO.output(AUTO_PUNAINEN, 1) # Punainen päälle
    time.sleep(0.5) # Odotetaan puoli sekuntia
    GPIO.output(AUTO_KELTAINEN, 1) # Lisätään keltainen päälle
    time.sleep(0.5)
    GPIO.output(AUTO_PUNAINEN, 0)
    GPIO.output(AUTO_KELTAINEN, 0)
    GPIO.output(AUTO_VIHREA, 1) # Vihreä päälle, punainen ja keltainen pois
    
    
# Asetetaan GPIO tilat    
def alustaPinnit():
    GPIO.setup(AUTO_PUNAINEN, GPIO.OUT) # Alustukset
    GPIO.setup(AUTO_KELTAINEN, GPIO.OUT)
    GPIO.setup(AUTO_VIHREA, GPIO.OUT)
    GPIO.setup(JALANKULKIJA_PUNAINEN, GPIO.OUT)
    GPIO.setup(JALANKULKIJA_KELTAINEN, GPIO.OUT)
    GPIO.setup(JALANKULKIJA_VIHREA, GPIO.OUT)
    GPIO.setup(NAPPI, GPIO.IN)
    GPIO.setup(LIIKETUNNISTIN, GPIO.IN)

    
if __name__ == "__main__":
    main()