#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

import socket
import ujson
import pycom
import os
import machine


class OTA():
    
    def __init__(self, firmware, host, cid, token, destinationPath=None):
        self.host = host
        self.token = token
        self.cid = cid
        self.destinationPath = destinationPath
        self.fW = firmware
    
    def update(self):
        # Download new files and verify hashes
        # Upto 5 retries
        for _ in range(5):
            try:
                self.get_file()
                break
            except Exception as e:
                print(e)
                msg = "Error downloading `{}` retrying..."
                print(msg.format(self.host))
        else:
            raise Exception("Failed to download `{}`".format(self.host))

        # Backup old files only once all files have been successfully downloaded
        self.backup_file()

        # Rename new files to proper name
        new_path = "{}.new".format(self.destinationPath)
        dest_path = self.destinationPath
        os.rename(new_path, dest_path)
        
        # Reboot the device to run the new decode
        print("........Rebooting.............")
        machine.reset()

    def get_file(self):
        self.get_data(self.host)


    def backup_file(self):
        print("Backing up files")
        bak_path = "{}.bak".format(self.destinationPath)
        dest_path = self.destinationPath

        # Delete previous backup if it exists
        try:
            os.remove(bak_path)
        except OSError:
            pass  
    
    def _http_post(self, path, host, cid):     
        print("path", path)
        print("Host", host)
        print("Reached Post")
        headers = 'POST /{path} HTTP/1.1\r\nHost: {host}\r\nx-access-token: {token}\r\nContent-Type: application/json\r\nContent-Length: {contentlength}\r\n\r\n'
        body = {"cid": "{}".format(cid)}
        body_bytes = ujson.dumps(body)
        contentlength = len(body_bytes)
        header_bytes = headers.format(path=str(path), host=str(host), token=self.token, contentlength = contentlength)
        payload = bytes(header_bytes + body_bytes, 'utf8')
        print("post Requests ----->", payload)
        return payload

    def get_data(self, url, firmware=False):
        print("GET-DATA")
        
        # Connect to server
        try:
            proto, dummy, host, path = url.split("/", 3)
        except ValueError:
            proto, dummy, host = url.split("/", 2)
            path = ""
        if proto == "http:":
            port = 80
        elif proto == "https:":
            import ussl
            port = 443
        else:
            raise ValueError("Unsupported protocol: " + proto)

        ai = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)
        ai = ai[0]
        print("Requesting: {}".format(path))
        s = socket.socket(ai[0], ai[1], ai[2])
        s.connect(ai[-1])
        s = ussl.wrap_socket(s, server_hostname=host)

        # Request File
        s.sendall(self._http_post(path, host, cid=self.cid))
        try:
            content = bytearray()
            fp = None
            if firmware:
                pycom.ota_start()

            # Get data from server
            result = s.recv(100)
            start_writing = False
            while (len(result) > 0):
                # Ignore the HTTP headers
                if not start_writing:
                    if "\r\n\r\n" in result:
                        print("result: ", result)
                        start_writing = True
                        result = result.decode().split("\r\n\r\n")[1].encode()
                        filepath = result.decode().split("version")[0].encode()
                        self.destinationPath = '/flash/config.py'
                        print("File Path --> ", self.destinationPath)
                        dest_path = "{}.new".format(self.destinationPath)
                        fp = open(dest_path, 'wb')
        

                if start_writing:
                    if firmware:
                        pycom.ota_write(result)
                    elif fp is None:
                        content.extend(result)
                    else:
                        fp.write(result)

                result = s.recv(100)
                
            s.close()

            if fp is not None:
                fp.close()
            if firmware:
                pycom.ota_finish()

        except Exception as e:
             print("Error", e)

      
