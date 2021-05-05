path="/flash/config.py"
version = "0.0.1"
"""
Asvin OTA Config File
"""

# firmware 
firmware_version="0.0.3"

# LED colors
LED_ERROR = 0xff0000 #RED
LED_blink_WIFI = 0x0000ff #Pink
LED_SLEEP = 0x0000ff #Blue

   
# Server URL's 
register= "https://app.vc.asvin.io/api/device/register"
checkRollout= "https://app.vc.asvin.io/api/device/next/rollout"
checkRolloutSuccess= "https://app.vc.asvin.io/api/device/success/rollout"
bc_GetFirmware= "https://app.besu.asvin.io/firmware/get"
ipfs_Download= "https://app.ipfs.asvin.io/firmware/download"
auth = "https://app.auth.asvin.io/auth/login"

        
# Asvin Credentials
customer_key=""
device_key = ""

# Wifi Credentials
wifissid= ""
wifipassword= ""
