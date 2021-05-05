import ubinascii
import machine
import config
from urequests import *
import pycom
import time
import math
from OTA import OTA
import hmac
import uhashlib

class asvinPlatform():
    def __init__(self):
        self.firmware_id = 0
        self.cid = 0
        self.rolloutid = 0
        self.authToken = 0 
    
    def auth(self):
        # get HMAC auth token
        customer_key = config.customer_key.encode('utf-8')
        device_key = config.device_key
        # timestamp = math.floor(time.time())
        timestamp = time.time()
        payload = (str(timestamp) + device_key).encode('utf-8')
        hashkey = hmac.new(customer_key, payload, digestmod=uhashlib.sha256)
        device_signature = ubinascii.hexlify(hashkey.digest()).decode('utf-8')
        try:
            print("  Getting OAUTH Token  ")
            myobj = {}
            myobj["device_key"] = config.device_key 
            myobj["device_signature"] = device_signature
            myobj["timestamp"] = timestamp
            # print(myobj)
            headers = {"Content-Type": "application/json"}
            x = post(config.auth, json=myobj, headers=headers)
            # print(x.text)
            response = x.json()
            try:
                self.authToken = response["token"]
                print(" Auth Token: ", self.authToken)
                return True
            except:
                print("Failed to parse auth token")
                return False
            if x.status_code == 200 :
                print("Got OAUTH Token ")

        except Exception as e:
            print("Failed to get OAUTH Token: ", e)
            return False



    def checkRolloutSuccess(self):
    # Check if the previous rollout was successful if it exists 
        try:
            print("....Checking rollout success state....")
            if pycom.nvs_get("rolloutid"):
                print(pycom.nvs_get("rolloutid"))
                myobj = {}
                myobj["mac"] = ubinascii.hexlify(machine.unique_id(), ':').decode()
                myobj["firmware_version"] = "1.0.0"
                myobj["rollout_id"] = pycom.nvs_get("rolloutid")
                headers = {"Content-Type": "application/json", "x-access-token" : self.authToken }
                x = post(config.checkRolloutSuccess, json=myobj, headers=headers)
                # print(x.text)
                # firmware_version = x.json()
                # More work required 
            else:
                print("No rollout exists")
        except Exception as e:
            print("Failed to check rollout success: ", e)

    def registerDevice(self):
        # Register Device ! 
        try:
            print("  Registering device  ")
            myobj = {}
            myobj["mac"] = ubinascii.hexlify(machine.unique_id(),':').decode()
            myobj["firmware_version"] = "1.0.0"
            headers = {"Content-Type": "application/json", "x-access-token" : self.authToken}
            x = post(config.register, json=myobj, headers=headers)
            # print(x.text)
            firmware_version = x.json()
            try:
                pycom.nvs_set("fwversion", firmware_version["firmware_version"])
                print("Fw version value set !")
            except:
                pycom.nvs_set("fwversion", "0")
                print("Failed to set firmware version")
            if x.status_code == 200 :
                print("Device Registered")

        except Exception as e:
            print("failed to register device: ", e)

        
    def checkRollout(self):
        try:
            print("......Checking for rollouts............")
            # check device next rollout 
            myobj = {}
            myobj["mac"] = ubinascii.hexlify(machine.unique_id(),':').decode()
            myobj["firmware_version"] = "1.0.0"
            headers = {"Content-Type": "application/json", "x-access-token" : self.authToken }
            x = post(config.checkRollout, json=myobj, headers=headers)
            if x.status_code == 200 :
                print(x.text)
                next_rollout = x.json()
                if "rollout_id" in next_rollout:
                    print(" rollout ID exists ")
                    pycom.nvs_set("rolloutid", next_rollout["rollout_id"])
                    self.rolloutid = next_rollout["rollout_id"]
                    self.firmware_id = next_rollout["firmware_id"]
                    print("....Rollout ID set....")
                    return True
                else:
                    print(" --- No new Rollout avaliable ----")
                    return False
        except Exception as e:
            print("Check Rollout failed: ", e)

    def getUpdate(self):
        try:
            # get CID from Block chain server 
            headers = {"Content-Type": "application/json", "x-access-token" : self.authToken }
            firmware_id = {"id": self.firmware_id}
            x = post(config.bc_GetFirmware, json=firmware_id, headers = headers)
            # print(x.text)
            response = x.json()
            self.cid = response["cid"]
            print("cid:  ", self.cid)
            if x.status_code == 200:
                print("Got CID from blockchain server")
                return True
                
        except Exception as e:
            print(" ---- Error in Deploying Rollout  ---- ", e)
            return False
    def doUpdate(self):
        try:
            headers = {"Content-Type": "application/json", "x-access-token" : self.authToken }
            cid = {"cid": self.cid}
            firmware = post(config.ipfs_Download, json=cid, headers = headers)
            ota = OTA(firmware, config.ipfs_Download, self.cid, self.authToken)
            ota.update()

        except Exception as e:
            print("Update Failed: ", e)