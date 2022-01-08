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

def get_ip_by_mac(mac):
    count = 0
    cmd = 'arp -a | findstr \"' + mac +  '\"'
    while count < 5:
        try:
            returned_output = sub(' +', ' ', subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT).decode("utf-8"))
            parse = returned_output.split(' ')
            return str(ip_address(parse[1]))
        except:
            send_magic_packet(mac)
            sleep(30)
            count += 1
    print("could not find ip of TV")
    exit(1)

def get_tv_name(ip, ares):
    cmd = "ares-extend-dev --device-list"
    returned_output = sub(' +', ' ', subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT, cwd=ares).decode("utf-8"))
    for line in returned_output.split("\n"):
        if ip in line:
            return line.split(" ")[0]

if __name__ ==  "__main__":
    parser = argparse.ArgumentParser(description='Simple script to reenable devmode on a LG WEBOS tv')
    parser.add_argument("--mac", help="Mac address of tv. Make sure only one network interface is enabled. I reccomend to only use lan", required=True)
    parser.add_argument("--ares", help="If ares is not installed globally set the global path here", default=None)

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

    print("wating for tv to turn on")
    sleep(30)
    cmd = "ares-extend-dev --device " + tv
    print(subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT, cwd=args.ares).decode("utf-8")) 

    client.connect()
    
    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV")
        elif status == WebOSClient.REGISTERED:
            print("Registration successful")

    system = SystemControl(client)
    system.power_off()

    with open('auth.json', 'w') as auth:
        json.dump(store, auth)