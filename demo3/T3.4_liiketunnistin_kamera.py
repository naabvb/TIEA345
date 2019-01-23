#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TIEA345 demo3
# lailpimi

# Ohjelma joka käskee ottamaan kuvan kun liikettä havaitaan

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

LIIKETUNNISTIN = 25
GPIO.setup(LIIKETUNNISTIN, GPIO.IN)

def main():

    try: 
        while True:
            if GPIO.input(LIIKETUNNISTIN) == 1: # Jos liikettä havaittiin
                print("OTETAAN KUVA")
                os.system("raspistill -o liiketunnistavakuva.jpg")

            time.sleep(1)
            
    except KeyboardInterrupt: # CTRL-C pysäyttää ohjelman ja ajaa lopuksi GPIO.cleanup()
        print("loppu")
    GPIO.cleanup()
    
    
if __name__ == "__main__":
    main()    