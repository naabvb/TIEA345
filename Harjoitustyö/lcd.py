#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LCD-näytön toiminnot
# lailpimi

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
import telegram_send
import Adafruit_CharLCD as LCD
from multiprocessing import Process

# Näytön pinnit
lcd_rs = 21
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2

# Näytön koko
lcd_columns = 16
lcd_rows = 2

# Luodaan näyttö-objekti
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

def on_connect(client, userdata, flags, rc):
     print("Connected With Result Code {}".format(rc))
     client.subscribe("halylcd") # Kuunnellaan näytön omaa topikkia

def on_disconnect(client, userdata, rc):
        print("Disconnected From Broker")

# Ensimmäinen ajastin, jota käytetään mikäli hälytys triggeröityy oven auetessa        
def sekkari():
    timer = 30
    while True:
        lcd.clear()
        lcd.message('DISARM IN:\n' +str(timer))
        timer = timer -1
        if timer == 0:
            lcd.clear()
            lcd.message('ALARM!')
            telegram_send.send(messages=["🚨 HÄLYTYS! 🚨"], conf="/etc/telegram-send.conf") # Jos ei disarmattu 30 sekunnin kuluessa, lähetetään hälytys
            break
        time.sleep(1)

# Toinen ajastin hälytyksen virittämiseen        
def sekkari2():
    timer = 15
    while True:
        lcd.clear()
        lcd.message('ARMED IN:\n' +str(timer))
        timer = timer -1
        if timer == 0:
            lcd.clear()
            lcd.message('ARMED')
            break
        time.sleep(1)        
        
thread = Process(target=sekkari) # Globaalit ajastin säikeille
thread2 = Process(target=sekkari2)   

# Säikeiden resetointi-funktio
def reset(s):
    if s == 1:
        global thread
        thread = Process(target=sekkari)
    if s == 2:
        global thread2
        thread2 = Process(target=sekkari2)
   
# Kun vastaanotetaan MQTT-viesti        
def on_message(client, userdata, message):
        
        if message.payload.decode() == "999": # INIT
            lcd.clear()
            lcd.message('DISARMED')
        
        if message.payload.decode() == "1": # ALARM TRIGGERED
            if thread2.is_alive() == True:
                thread2.terminate()
            reset(2)
            thread.start()

        if message.payload.decode() == "0": # DISARM
            if thread.is_alive() == True:
                thread.terminate()
            reset(1)
            lcd.clear()
            lcd.message('ALARM DISARMED')
            
        if message.payload.decode() == "2": # ARM TIMER
            if thread2.is_alive() == True:
                thread2.terminate()
            reset(2)
            thread2.start()
            
def main():
    broker_address = "127.0.0.1" # localhost kuuntelija, lcd vastaanottaa viestejä vain nfc-lukijalta
    client = mqtt.Client()
    lcd.clear()
    lcd.message('DISARMED')

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker_address)
    client.loop_forever()


if __name__ == "__main__":
    main()  