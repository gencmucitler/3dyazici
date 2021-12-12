#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import re

Role_Yazici =  21
Role_Aydinlatma =  20

GPIO.setmode(GPIO.BCM)

GPIO.setup(Role_Yazici , GPIO.OUT)
GPIO.setup(Role_Aydinlatma , GPIO.OUT)

GPIO.output(Role_Aydinlatma , GPIO.HIGH)
GPIO.output(Role_Yazici , GPIO.HIGH)

