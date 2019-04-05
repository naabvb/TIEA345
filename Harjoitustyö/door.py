#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Ovi-sensorin toiminnot
# lailpimi

import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from multiprocessing import Process
import subprocess
import os 

time.sleep(5)

GPIO.setmode(GPIO.BCM) # Ovi pinnit
DOOR_SENSOR_PIN = 18
lahettaja = mqtt.Client()

# Oven kuuntelija, mikäli ovi aukeaa ja sitä vahditaan aloitetaan nauhoitus
def ovi_sensori():
    isOpen = None
    oldIsOpen = None 

    while True:
        oldIsOpen = isOpen 
        isOpen = GPIO.input(DOOR_SENSOR_PIN)

        if (isOpen and (isOpen != oldIsOpen)): # Jos ovi avattiin   
            
            lahettaja.connect("127.0.0.1")
            lahettaja.publish("haly","1") # Lähetetään lukijalle
            lahettaja.disconnect()
            os.system("sudo sh /home/pi/haly/startrec.sh")
            break
           
        time.sleep(0.1)

    return
    
thread = Process(target=ovi_sensori) # Ovi säie

# Säikeen resetointiin       
def reset():
    global thread
    thread = Process(target=ovi_sensori)


def on_connect(client, userdata, flags, rc):
     print("Connected With Result Code {}".format(rc))
     client.subscribe("halyovi")

def on_disconnect(client, userdata, rc):
        print("Disconnected From Broker")

def on_message(client, userdata, message):

        if message.payload.decode() == "0": # DISARM
            os.system("sudo sh /home/pi/haly/stoprec.sh") # Jos vastaanotetaan disarm, lopetetaan nauhoitus
        
        if message.payload.decode() == "1": # ARMED
            if thread.is_alive() == True:
                thread.terminate()
            reset()
            thread.start() # Aloitetaan ovea vahtiva säie
            

def main():
    init() # Setup pins
    
    broker_address = "192.168.0.180" # NFC/LCD istuu täällä
    client = mqtt.Client()
    
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker_address)
    client.loop_forever()


def init():
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)    
       
if __name__ == "__main__":
    main() 