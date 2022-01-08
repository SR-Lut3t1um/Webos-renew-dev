#!/usr/bin/env python3
"""
Simple script to reneable devmode on a LG WEBOS tv
"""

import argparse
import subprocess
import json

from wakeonlan import send_magic_packet
from time import sleep
from ipaddress import ip_address
from re import sub
from pywebostv.connection import WebOSClient
from pywebostv.controls import SystemControl
from os.path import realpath

def get_ip_by_mac(mac: str):
    count = 0
    cmd = 'arp -a'
    while count <= 5:
        returned_output = sub(' +', ' ', subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT).decode("utf-8"))
        parse = returned_output.split('\n')

        for line in parse:
            line = line.strip().split(' ')
            
            mac_index = 1
            ip_index = 0

            if ("(" in line[1]): # we are on unix
                mac_index = 3
                ip_index = 1
                line[ip_index] = line[ip_index].replace("(", "").replace(")", "")

            if (len(line) > 2 and mac.lower() in line[mac_index].lower()):
                tv_ip = str(ip_address(line[ip_index]))
                return tv_ip
        
        print("could not get IP address sending WoL")
        send_magic_packet(mac)
        sleep(30)
    print("could not find tv")
    exit(1)

def get_tv_name(ip, ares):
    cmd = "ares-extend-dev --device-list"
    try:
        returned_output = sub(' +', ' ', subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT, cwd=ares).decode("utf-8"))
    except:
        print("could not find SDK. please provide the sdk location using --ares")
        exit(1)
    for line in returned_output.split("\n"):
        if ip in line:
            return line.split(" ")[0]

if __name__ ==  "__main__":
    parser = argparse.ArgumentParser(description='Simple script to reenable devmode on a LG WEBOS tv')
    parser.add_argument("--mac", type=str, help="Mac address of tv. Make sure only one network interface is enabled. I reccomend to only use lan", required=True)
    parser.add_argument("--ares", type=str, help="If ares is not installed globally set the global path here", default=None)

    args = parser.parse_args()

    ip = get_ip_by_mac(args.mac)
    tv = get_tv_name(ip, args.ares)
    client = WebOSClient(ip)
    store = {}

    # load web api keys (if existent)
    try: 
        with open('auth.json') as json_file:
            store = json.load(json_file)
    except:
        print("could not find WEBOS auth file creating new")

    cmd = "ares-extend-dev --device " + tv
    print(subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT, cwd=args.ares).decode("utf-8")) 

    client.connect()
    
    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV")
        elif status == WebOSClient.REGISTERED:
            print("connected to api")

    system = SystemControl(client)
    system.power_off()

    with open('auth.json', 'w') as auth:
        json.dump(store, auth)