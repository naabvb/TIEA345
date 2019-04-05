#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NFC-lukija/MQTT-loop
# lailpimi

import RPi.GPIO as GPIO
import SimpleMFRC522
import paho.mqtt.client as mqtt
import os
import time

# MQTT funktiot
def on_connect(client, userdata, flags, rc):
     print("Connected With Result Code {}".format(rc))
     client.subscribe("haly")

def on_disconnect(client, userdata, rc):
        print("Disconnected From Broker")

# Silmukka jota ajetaan kun hälytys on DISARMED ja odotetaan että hälytys viritetään uudestaan sallitulla nfc-lätkällä        
def arm_loop():
    lahettaja.connect("127.0.0.1")
    lahettaja.publish("halylcd","999") # Nollataan näyttö
    lahettaja.disconnect()
    while True:
        try:
            id, text = reader.read()
            if id == 453484577718 and text.strip() == "15081996": # Jos sallittu lätkä
                lahettaja.connect("127.0.0.1")
                lahettaja.publish("halylcd","2") # 2 tarkoittaa arming eli näytetään ajastin eri jutuilla
                lahettaja.disconnect()
                time.sleep(15) # Odotetaan 15 sec ja käsketään sitten ovi vahtimaan
                lahettaja.connect("127.0.0.1")
                lahettaja.publish("halyovi","1")
                lahettaja.disconnect()
                return                    
        except:
            continue
    time.sleep(0.1)
        
# Kun saadaan MQTT-viesti        
def on_message(client, userdata, message):
        # INIT
        if message.payload.decode() == "999":
            arm_loop() # JOS INIT mennään suoraan arm_loop
        
        # Jos ovi aukeaa ja häly (Tätä viestiä ei lähetetä jos häly deactivated)
        if message.payload.decode() == "1":
            lahettaja.connect("127.0.0.1")
            lahettaja.publish("halylcd","1")
            lahettaja.disconnect()
            # Aloitetaan NFC-lukijan kuuntelu silmukassa + ajastin
            while True:
                try:
                    id, text = reader.read()
                    
                    if id == 453484577718 and text.strip() == "15081996": # Jos sallittu lätkä. Kovakoodattu vain esimerkin vuoksi
                        lahettaja.connect("127.0.0.1")
                        lahettaja.publish("halylcd","0") # Näyttö nollataan
                        lahettaja.publish("halyovi","0") # Ovisensori nollataan + nauhoitus lopetetaan
                        lahettaja.disconnect()
                        
                        time.sleep(5) # Odotetaan 5 sec, että vältytään mahdolliselta virhe armilta
                        arm_loop() # Aloitetaan silmukka jossa vahditaan mikäli järjestelmä halutaan virittää
                                             
                        break;
                except:
                    continue   
                time.sleep(0.5)    
                
              
broker_address = "192.168.0.160" # Ovi sensori/kamera
reader = SimpleMFRC522.SimpleMFRC522()
client = mqtt.Client() # Vastaanottaja
lahettaja = mqtt.Client() # Lähetin
lahettaja.connect("127.0.0.1")
lahettaja.publish("halylcd","999") # INIT näytölle, lähetetään localhostina MQTT
lahettaja.disconnect()

arm_loop() # Aloitetaan INIT jälkeen ARM-loop. Laitteisto aloittaa siis defaulttina DISARMED

# MQTT funktiot
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(broker_address)
client.loop_forever()

