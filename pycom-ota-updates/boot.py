from network import Bluetooth
from network import WLAN 
import time
import pycom
import machine 
import ujson
from machine import RTC
from machine import I2C

# import wifi lib
from connect_wifi import ConnectWIFI


# import config file
import config

# switch off pycom funtions on boot, add more after testing  
pycom.wifi_on_boot(False)
pycom.heartbeat_on_boot(False)
pycom.pybytes_on_boot(False)
pycom.wdt_on_boot(False)


print("Reset Cause: ", machine.reset_cause())

# external RTC with i2c address 104

# initialize RTC
rtc = RTC()

# Disable Blueooth Radio
ble = Bluetooth()
ble.deinit()

# Initialize wifi
connectwifi = ConnectWIFI()

# wakeup reason and logic ? 

def ext_rtc_sync():
    print("Syncing RTC .....")
    rtc_sync()
    try:
        print("Updating External RTC ...")
        ds3231.save_time()
        print("External RTC updated")
    except:
        print("Failed to set Local RTC time.. RTC disconnected")

def rtc_sync():
    # Connect using WiFi
    connectwifi.__init__()
    connectwifi.connectwifi()


    timeout = time.time() + 10
    while not rtc.synced():
        if time.time() > timeout:
            print("Cant set RTC ")
            break
        rtc.ntp_sync("de.pool.ntp.org")
        print(".", end="")
        time.sleep(0.5)
        machine.idle()  

#  sync time with external RTC
try:
    print("Syncing time using ntp")
    rtc_sync()
    print("RTC time", rtc.now())
except Exception as e:
    print('Cannot set time RTC: ', e)