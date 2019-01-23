#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TIEA345 demo3
# lailpimi

# Ohjelma ottaa kuvan kun crontab käskee

import os
os.system("raspistill -o /home/pi/Kuvat/tasatuntikuva.jpg") # Asetetaan kansioon johon webpalvelin on linkattu
