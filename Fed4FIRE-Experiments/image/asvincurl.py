import threading
import random
import string
import time
import sys
import os
from influxdb import InfluxDBClient, SeriesHelper
import warnings
from urllib3.exceptions import SNIMissingWarning, InsecurePlatformWarning
import datetime
from requests import post

print(sys.version)
warnings.simplefilter('ignore', SNIMissingWarning)
warnings.simplefilter('ignore', InsecurePlatformWarning)

try:
    amount_threads = int(sys.argv[1])
    # Accept "prod" or "stage". If nothing or wrong value is given then assign server to staging
    if sys.argv[2] == "prod":
        server = "prod"
    else:
        server = "stage"
except (ValueError, IndexError):
    amount_threads = 1
    server = "stage"

print("Amount of threads:", amount_threads)
print("Server:", server)

influx_host = os.environ.get('INFLUX_HOST')
dbname = os.environ.get('INFLUX_DATABASE')
experiment = os.environ.get('EXPERIMENT_ID')
pod_name = os.environ.get('POD_NAME')

client = InfluxDBClient(influx_host, database=dbname)
client.create_database(dbname)

print(influx_host, dbname, experiment, pod_name)

asvin_requests = 0
asvin_requests_lock = threading.Lock()
asvin_req_failure = 0
asvin_req_failure_lock = threading.Lock()
asvin_req_res_time = [0.0]

bcs_requests = 0
bcs_requests_lock = threading.Lock()
bcs_req_failure = 0
bcs_req_failure_lock = threading.Lock()
bcs_req_res_time = [0.0]

ipfs_requests = 0
ipfs_requests_lock = threading.Lock()
ipfs_req_failure = 0
ipfs_req_failure_lock = threading.Lock()
ipfs_req_res_time = [0.0]

update_success = 0
update_success_lock = threading.Lock()

# The details of url and keys for staging and production server
details = {
    "stage": {
        "urls": {
            "register": "https://vc-server/api/device/register",
            "check_rollout": "https://vc-server/api/device/next/rollout",
            "bcs_login": "https://bc-server/auth/login",
            "bcs_get_firmware": "https://bc-server/firmware/get",
            "ipfs_login": "https://ipfs-server/auth/login",
            "ipfs_download": "https://ipfs-server/firmware/download",
            "rollout_success": "https://vc-server/api/device/success/rollout"
        },
        "keys": {
            "customer_key": "INSERT-YOUR-CUSTOMER-KEY",
            "device_key": "INSERT-YOUR-DEVICE-KEY"
        }
    },
    "prod": {
        "urls": {
            "register": "https://vc-server/api/device/register",
            "check_rollout": "https://vc-server/api/device/next/rollout",
            "bcs_login": "https://vc-server/auth/login",
            "bcs_get_firmware": "https://bc-server/firmware/get",
            "ipfs_login": "https://ipfs-server/auth/login",
            "ipfs_download": "https://ipfs-server/firmware/download",
            "rollout_success": "https://vc-server/api/device/success/rollout"
        },
        "keys": {
            "customer_key": "INSERT-YOUR-CUSTOMER-KEY",
            "device_key": "INSERT-YOUR-DEVICE-KEY"
        }
    },
    "credentials": {
        "email": "email_id",
        "password": "password"
    }
}


class RequestsHelper(SeriesHelper):
    """Instantiate SeriesHelper to write points to the backend."""

    class Meta:
        """Meta class stores time series helper configuration."""

        # The client should be an instance of InfluxDBClient.
        client = client

        # The series name must be a string. Add dependent fields/tags
        # in curly brackets.
        series_name = 'requests'

        # Defines all the fields in this time series.
        fields = ['asvin_requests', 'bcs_requests', 'ipfs_requests', 'asvin_req_suc', 'asvin_req_fail', 'bcs_req_suc',
                  'bcs_req_fail', 'ipfs_req_suc', 'ipfs_req_fail', 'asvin_req_res_time', 'bcs_req_res_time',
                  'ipfs_req_res_time', 'update_suc']

        # Defines all the tags for the series.
        tags = ['server_name', 'experiment']

        # Defines the number of data points to store prior to writing
        # on the wire.
        bulk_size = 5

        # autocommit must be set to True when using bulk_size
        autocommit = True


def random_mac_generator():
    """Returns a completely random Mac Address"""
    mac = [random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0x7f),
           random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def random_name_generator():
    """Returns a 7-digit random name for the device (string+number) """
    chars = string.ascii_letters + string.digits
    size = 7
    return ''.join(random.choice(chars) for _ in range(size))


class WorkerThread(threading.Thread):
    def __init__(self, name, mac, thread_no):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = name
        self.mac = mac
        self.thread_no = thread_no
        self.newfirmwareid = "0"
        self.newfirmwareversion = "0"
        self.newrollout_id = "0"
        self.cid = "0"
        self.body = {}
        self.header = {}

    def run(self):
        print("Thread -", self.thread_no, ": run thread")
        self.body = {
            "mac": self.mac,
            "firmware_version": "1.0",
            "customer_key": details[server]["keys"]["customer_key"],
            "device_key": details[server]["keys"]["device_key"],
            "name": self.name
        }
        self.header = {
            "Content-Type": "application/json"
        }
        print("Thread -", self.thread_no, ": Device details:", self.body)
        while True:
            try:
                print("Thread -", self.thread_no, ": Device name:", self.body["name"], " , Device firmware version:",
                      self.body["firmware_version"])
                if self.register_device():
                    if self.check_for_rollouts():
                        if self.get_cid():
                            if self.download_from_ipfs():
                                if self.send_success_status():
                                    print("Thread -", self.thread_no, ": Successfully updated with new firmware & sent "
                                                                      "the status to asvin platform")
            except:
                print("Thread -", self.thread_no, ": Unexpected error:", sys.exc_info()[0])
                pass
            sleep_time = random.randint(7000, 10500)
            print("Thread -", self.thread_no, ": Sleeping for", sleep_time, "seconds for next run of the thread")
            time.sleep(sleep_time)

    def register_device(self):
        """The function call the http request to asvin platform"""
        global asvin_requests, asvin_req_failure, asvin_req_res_time
        r = post(details[server]["urls"]["register"], json=self.body, headers=self.header)
        with asvin_requests_lock:
            asvin_requests += 1
            asvin_req_res_time.append(r.elapsed.total_seconds())
        # print("response:", r.data)
        try:
            if r.status_code == 200:
                print("Thread -", self.thread_no, ": Device is registered")
                print("Thread -", self.thread_no, ": Registration response time:", r.elapsed.total_seconds())
                response = r.json()
                self.body["firmware_version"] = response["firmware_version"]
                return 1
            else:
                with asvin_req_failure_lock:
                    asvin_req_failure += 1
                print("Thread -", self.thread_no, ": Device is not registered.. Please verify the device data or check "
                                                  "with administrator")
                return 0
        except:
            print("Thread -", self.thread_no, ": Something went wrong during device registration")

    def check_for_rollouts(self):
        """This function checks if there are any new rollouts available"""
        global asvin_requests, asvin_req_failure, asvin_req_res_time
        print("Thread -", self.thread_no, ": Checking for new rollouts")
        r = post(details[server]["urls"]["check_rollout"], json=self.body, headers=self.header)
        with asvin_requests_lock:
            asvin_requests += 1
            asvin_req_res_time.append(r.elapsed.total_seconds())
        if r.status_code == 200:
            responsedata = r.json()
            # print(responsedata)
            print("Thread -", self.thread_no, ": Rollout check response time:", r.elapsed.total_seconds())
            try:
                if "id" in responsedata:
                    self.newfirmwareid = responsedata["firmware_id"]
                    self.newfirmwareversion = responsedata["version"]
                    self.newrollout_id = responsedata["id"]
                    print("Thread -", self.thread_no, ": New firmware available:", self.newfirmwareid)
                    return 1
                else:
                    print("Thread -", self.thread_no, ": No new firmware update rollout available.")
                    return 0
            except:
                print("Thread -", self.thread_no, ": Error in Rollouts !!!")
                return 0
        else:
            with asvin_req_failure_lock:
                asvin_req_failure += 1
            return 0

    def get_cid(self):
        """This function fetches the CID from Block Chain Server"""
        global bcs_requests, bcs_req_failure, bcs_req_res_time
        print("Thread -", self.thread_no, ": 1. Login to Blockchain server")
        bcs_login = {"email": details["credentials"]["email"], "password": details["credentials"]["password"]}
        r = post(details[server]["urls"]["bcs_login"], json=bcs_login, headers=self.header)
        with bcs_requests_lock:
            bcs_requests += 1
            bcs_req_res_time.append(r.elapsed.total_seconds())
        # print(r.json())
        if r.status_code == 200:
            print("Thread -", self.thread_no, ": Logged into the Block Chain Server")
            bcs_token = r.json()
            print("Thread -", self.thread_no, ": BCS Login response time:", r.elapsed.total_seconds())
            print("Thread -", self.thread_no, ": 2. Get the CID from BCS")
            firmware_id = {"id": self.newfirmwareid}
            headers = {"Content-Type": "application/json", "x-access-token": bcs_token["token"]}
            r = post(details[server]["urls"]["bcs_get_firmware"], json=firmware_id, headers=headers)
            with bcs_requests_lock:
                bcs_requests += 1
                bcs_req_res_time.append(r.elapsed.total_seconds())
            # print(r.data)
            if r.status_code == 200:
                print("Thread -", self.thread_no, ": Received CID from BCS")
                responsedata = r.json()
                print("Thread -", self.thread_no, ": BCS get CID response time:", r.elapsed.total_seconds())
                self.cid = {"cid": responsedata["Firmware"]["cid"]}
                # print(cid)
                return 1
            else:
                with bcs_req_failure_lock:
                    bcs_req_failure += 1
                print("Thread -", self.thread_no, ": Error in fetching CID from Block Chain Server!!!")
        else:
            with bcs_req_failure_lock:
                bcs_req_failure += 1
            print("Thread -", self.thread_no, ": There was a problem while logging into the Block Chain Server!!!")
        return 0

    def download_from_ipfs(self):
        """ This function downloads the new firmware from IPFS server"""
        global ipfs_requests, ipfs_req_failure, ipfs_req_res_time
        print("Thread -", self.thread_no, ": 3. Login to IPFS Server")
        ipfs_login = {"email": details["credentials"]["email"], "password": details["credentials"]["password"]}
        r = post(details[server]["urls"]["ipfs_login"], json=ipfs_login, headers=self.header)
        with ipfs_requests_lock:
            ipfs_requests += 1
            ipfs_req_res_time.append(r.elapsed.total_seconds())
        # print(r.json())
        if r.status_code == 200:
            print("Thread -", self.thread_no, ": Logged in to IPFS Server")
            ipfs_token = r.json()
            print("Thread -", self.thread_no, ": IPFS Login response time:", r.elapsed.total_seconds())
            print("Thread -", self.thread_no, ": 4. Download the new firmware from IPFS Server")
            headers = {"Content-Type": "application/json", "x-access-token": ipfs_token["token"]}
            r = post(details[server]["urls"]["ipfs_download"], json=self.cid, headers=headers)
            with ipfs_requests_lock:
                ipfs_requests += 1
                ipfs_req_res_time.append(r.elapsed.total_seconds())
            if r.status_code == 200:
                print("Thread -", self.thread_no, ": Successfully downloaded the firmware.")
                firmware = r.text
                print("Thread -", self.thread_no, ": Download firmware response time:", r.elapsed.total_seconds())
                print("Thread -", self.thread_no, ":", firmware)
                time.sleep(10)
                print("Thread -", self.thread_no, ": updating ...")
                time.sleep(10)
                print("Thread -", self.thread_no, ": update successful")
                self.body["firmware_version"] = self.newfirmwareversion
                return 1
            else:
                with ipfs_req_failure_lock:
                    ipfs_req_failure += 1
                print("Thread -", self.thread_no, ": Error in downloading the firmware from IPFS Server!!!")
        else:
            with ipfs_req_failure_lock:
                ipfs_req_failure += 1
            print("Thread -", self.thread_no, ": There was a problem while logging into the IPFS Server!!!")
        return 0

    def send_success_status(self):
        """This function sends the success details to asvin platform"""
        global asvin_requests, asvin_req_failure, asvin_req_res_time, update_success
        body_success = {
            "mac": self.mac,
            "firmware_version": self.newfirmwareversion,
            "customer_key": details[server]["keys"]["customer_key"],
            "device_key": details[server]["keys"]["device_key"],
            "rollout_id": self.newrollout_id
        }
        # print(body_success)
        print("Thread -", self.thread_no, ": 5. Now send the update success details to the asvin platform")
        r = post(details[server]["urls"]["rollout_success"], json=body_success, headers=self.header)
        with asvin_requests_lock:
            asvin_requests += 1
            asvin_req_res_time.append(r.elapsed.total_seconds())
        # print(r.text)
        if r.status_code == 200:
            print("Thread -", self.thread_no, ": Send rollout success response time:", r.elapsed.total_seconds())
            with update_success_lock:
                update_success += 1
            return 1
        else:
            with asvin_req_failure_lock:
                asvin_req_failure += 1
            print("Thread -", self.thread_no, ": Problem in sending the update details to asvin platform!!!")
            return 0


threads = []

for thread_number in range(amount_threads):
    device_mac = random_mac_generator()
    # print("Random mac address: ", device_mac)
    device_name = random_name_generator()
    # print("Random device name:", device_name)
    t = WorkerThread(device_name, device_mac, thread_number)  # "ABC", "0C:79:54:02:BA:FD"
    threads.append(t)
    wait_time = random.randint(45, 75)
    print("Waiting for", wait_time, "seconds before starting the thread")
    time.sleep(wait_time)
    t.start()

# Check if there remain threads active, otherwise exit with failure
while threading.active_count() > 1:
    with asvin_requests_lock and bcs_requests_lock and ipfs_requests_lock:
        with asvin_req_failure_lock and bcs_req_failure_lock and ipfs_req_failure_lock:
            RequestsHelper(server_name=pod_name, asvin_requests=asvin_requests,
                           asvin_req_suc=(asvin_requests - asvin_req_failure), asvin_req_fail=asvin_req_failure,
                           bcs_requests=bcs_requests, bcs_req_suc=(bcs_requests - bcs_req_failure),
                           bcs_req_fail=bcs_req_failure, ipfs_requests=ipfs_requests,
                           ipfs_req_suc=(ipfs_requests - ipfs_req_failure), ipfs_req_fail=ipfs_req_failure,
                           asvin_req_res_time=asvin_req_res_time[-1], bcs_req_res_time=bcs_req_res_time[-1],
                           ipfs_req_res_time=ipfs_req_res_time[-1], update_suc=update_success, experiment=experiment)
            if asvin_requests > 0 or bcs_requests > 0 or ipfs_requests > 0:
                now = datetime.datetime.now()
                # print("date and time : ", (now.strftime("%Y-%m-%d %H:%M:%S")))
                print("Date and Time : ", (now.strftime("%Y-%m-%d %H:%M:%S")), "asvin_requests:", asvin_requests,
                      ", bcs_requests:", bcs_requests, ", ipfs_requests:", ipfs_requests)
                print("asvin_req_success: ", (asvin_requests - asvin_req_failure), ", asvin_req_failure: ",
                      asvin_req_failure)
                print("bcs_req_success:   ", (bcs_requests - bcs_req_failure), ", bcs_req_failure:   ", bcs_req_failure)
                print("ipfs_req_success:  ", (ipfs_requests - ipfs_req_failure), ", ipfs_req_failure:  ",
                      ipfs_req_failure)
                print("asvin resp time:", *asvin_req_res_time, sep="  ")
                print("bcs resp time:", *bcs_req_res_time, sep="  ")
                print("ipfs resp time:", *ipfs_req_res_time, sep="  ")
                print("Successful updates:", update_success)
            update_success = 0
            asvin_req_res_time = [0.0]
            bcs_req_res_time = [0.0]
            ipfs_req_res_time = [0.0]
            asvin_req_failure = 0
            bcs_req_failure = 0
            ipfs_req_failure = 0
        ipfs_requests = 0
        bcs_requests = 0
        asvin_requests = 0
    time.sleep(900)

# flush remaining data
# RequestsHelper(server_name=pod_name, asvin_requests=asvin_requests, bcs_requests=bcs_requests,
#               ipfs_requests=ipfs_requests, experiment=experiment)
RequestsHelper(server_name=pod_name, asvin_requests=asvin_requests, asvin_req_suc=(asvin_requests - asvin_req_failure),
               asvin_req_fail=asvin_req_failure, bcs_requests=bcs_requests, bcs_req_suc=(bcs_requests - bcs_req_failure),
               bcs_req_fail=bcs_req_failure, ipfs_requests=ipfs_requests, ipfs_req_suc=(ipfs_requests - ipfs_req_failure),
               ipfs_req_fail=ipfs_req_failure, asvin_req_res_time=asvin_req_res_time[-1],
               bcs_req_res_time=bcs_req_res_time[-1], ipfs_req_res_time=ipfs_req_res_time[-1],
               update_suc=update_success, experiment=experiment)
RequestsHelper.commit()

# In the unlikely event that all threads crashed, let Kuberenetes schedule a new pod
sys.exit(1)
