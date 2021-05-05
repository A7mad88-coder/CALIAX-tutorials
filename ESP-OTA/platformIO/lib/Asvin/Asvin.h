/**
 * asvin.h
 * @author Rohit Bohara
 * 
 * Copyright (c) 2019 asvin.io. All rights reserved. 
 */
#ifndef ASVIN_H_
#define ASVIN_H_

#include <Arduino.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include "ESP8266httpUpdate.h"
#include <WiFiClientSecureBearSSL.h>


#ifndef DEBUG_ASVIN_UPDATE
// #define DEBUG_ASVIN_UPDATE
#define DEBUG_ASVIN_UPDATE(...) Serial.printf( __VA_ARGS__ )
#endif

#ifndef DEBUG_ASVIN_UPDATE
 #define DEBUG_ASVIN_UPDATE(...)
#endif

// Use #define checkCert to verify server fingerprint
#define nocheckCert

class Asvin
{
    public:
        Asvin(void);
        ~Asvin(void);
        String RegisterDevice(const String mac, String currentFwVersion, String token, int& httpCode);
        String CheckRollout(const String mac, const String currentFwVersion, String token, int& httpCode);
        String authLogin(String device_key, String device_signature, long unsigned int timestamp, int& httpCode);
        String GetBlockchainCID(const String firmwareID, String token, int& httpCode);
        String CheckRolloutSuccess(const String mac, const String currentFwVersion, String token, const String rollout_id, int& httpCode);
        t_httpUpdate_return DownloadFirmware(String token, const String cid);
        

    private:
        const String registerURL = "https://app.vc.asvin.io/api/device/register";
        const String checkRollout = "https://app.vc.asvin.io/api/device/next/rollout";
        const String checkRolloutSuccess = "https://app.vc.asvin.io/api/device/success/rollout";
        const String authserver_login = "https://app.auth.asvin.io/auth/login";
        const String bc_GetFirmware = "https://app.besu.asvin.io/firmware/get";
        const String ipfs_Download = "https://app.ipfs.asvin.io/firmware/download";
        
    #ifdef checkCert 
        const char *fingerprint_register = "04 8F 26 8C F3 11 A6 5D 96 5B 4E 19 CD 4F F0 60 81 F2 EE D4";
        const char *fingerprint_bc = "7D 1D 86 64 81 3E BE EC E7 A2 9C 41 F8 BC 26 CA 90 86 E4 02"; 
        const char *fingerprint_ipfs = "2A 35 41 0E 97 9F 80 2C 20 2D 93 D6 17 2F 89 7F 10 E7 45 6E";
        const char *fingerprint_auth = "84 03 01 90 2A 92 50 7A 2D BA 73 76 64 88 1C BF 86 A5 E2 6E";
    #endif
};                                 
#endif
