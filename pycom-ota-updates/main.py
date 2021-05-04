# This is a python script to demonstrate OTA Updates using 
# Asvin IoT platform 
# License: Apache 2.0

from urequests import *

# config file contains all account and user credentials 
import config


# import asvin platform functions
from asvin import asvinPlatform

# initialize the asvin platform funtions
platform = asvinPlatform()


# Read data every 1 min 
def blinkLED(color):
    pycom.rgbled(color) 
    time.sleep(0.5)
    pycom.rgbled(0x000000)
    time.sleep(0.5)
    pycom.rgbled(color)
    time.sleep(0.5)
    pycom.rgbled(0x000000)

while True:
    blinkLED(config.LED_blink_WIFI)
    connectwifi.reconnect()
    if platform.auth():
        # platform.checkRolloutSuccess()
        platform.registerDevice()
        if platform.checkRollout():
            if platform.getUpdate():
                platform.doUpdate()

    blinkLED(config.LED_SLEEP)
    machine.sleep(5000)