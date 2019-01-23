#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TIEA345 demo3
# lailpimi

# Nopea koodi sensoridatan tulostamiseen

import sys
import Adafruit_DHT

while True:

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
