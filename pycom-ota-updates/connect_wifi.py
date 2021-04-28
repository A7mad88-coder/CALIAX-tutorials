from network import WLAN 
import time
import pycom 
import machine
import config

class ConnectWIFI:
    def __init__(self):
        self.wlan = WLAN(mode=WLAN.STA)
        
    def connectwifi(self):
        if self.isConnected():
            print("Wifi Connected")
        else:
            self.SSID = config.wifissid
            self.PASSWORD = config.wifipassword
            timeout = time.time() + 10
            self.wlan.connect(self.SSID, auth=(WLAN.WPA, self.PASSWORD), channel = 9)
            while not self.wlan.isconnected():
                if time.time() > timeout:
                    pycom.rgbled(config.LED_ERROR)
                    time.sleep(0.5)
                    pycom.rgbled(config.LED_ERROR)
                    machine.reset()
                print(".", end="")
                pycom.rgbled(config.LED_blink_WIFI)
                time.sleep(0.5)
                pycom.rgbled(0x000000)
                time.sleep(0.5)
                machine.idle() # save power while waiting
            print('.........WiFi connected........')
            print("Wifi Config --> ", self.wlan.ifconfig())
    
    def isConnected(self):
        if self.wlan.isconnected():
            return True
        else:
            return False
    def deinit(self):
        print('Deinitializing wifi radio')
        self.wlan.deinit()

    def disconnect(self):
        print("disconnecting wifi")
        self.wlan.disconnect()

    def reconnect(self):
        if self.isConnected():
            print("wifi connected")
        else:
            print("Trying to reconnect")
            self.__init__()
            self.connectwifi()