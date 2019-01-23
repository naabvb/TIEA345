#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TIEA345 demo3
# lailpimi

# Koodi sensoridatan viemiseksi google sheetsiin. Aikalailla kopio Adafruitin malliohjelmasta. Lähettää nyt dataa 10 sekunnin välein

import json
import sys
import time
import datetime

import Adafruit_DHT
import gspread
from oauth2client.service_account import ServiceAccountCredentials

DHT_TYPE = Adafruit_DHT.DHT11 # Sensorin tyyppi
DHT_PIN  =  4

GDOCS_OAUTH_JSON = 'tiea345-lailpimi-7d39f6d1543d.json'
GDOCS_SPREADSHEET_NAME = 'raspidata'

FREQUENCY_SECONDS      = 10 # Aika havaintojen välillä

def login_open_sheet(oauth_key_file, spreadsheet):
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1
        return worksheet
    except Exception as ex:
        print('Google sheet login failed with error:', ex)
        sys.exit(1)

        
print('Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
print('Press Ctrl-C to quit.')
worksheet = None
while True:
    # Login if necessary.
    if worksheet is None:
        worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

    # Attempt to get sensor reading.
    humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)

    # Skip to the next reading if a valid measurement couldn't be taken.
    # This might happen if the CPU is under a lot of load and the sensor
    # can't be reliably read (timing is critical to read the sensor).
    if humidity is None or temp is None:
        time.sleep(2)
        continue

    print('Temperature: {0:0.1f} C'.format(temp))
    print('Humidity:    {0:0.1f} %'.format(humidity))

    # Append the data in the spreadsheet, including a timestamp
    try:
        worksheet.append_row((datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), str(temp) + ' C', str(humidity) + ' %')) # Antoi append erroria ilman muunnoksia
    except:
        # Error appending data, most likely because credentials are stale.
        # Null out the worksheet so a login is performed at the top of the loop.
        print('Append error, logging in again')
        worksheet = None
        time.sleep(FREQUENCY_SECONDS)
        continue

    # Wait FREQUENCY_SECONDS before continuing
    print('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))
    time.sleep(FREQUENCY_SECONDS)        