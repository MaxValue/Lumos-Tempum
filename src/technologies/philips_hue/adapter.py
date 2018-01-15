#!/usr/bin/env python3
# coding: utf-8
#

import requests, json

def init(config_values):
    global BASEURL
    ipaddress = config_values.get("PHILIPS HUE", "ipaddress")
    username = config_values.get("PHILIPS HUE", "username")
    BASEURL = "http://{}/api/{}/".format(ipaddress, username)

def _translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return int( rightMin + (valueScaled * rightSpan) )

def kelvin_mired(kelvin):
    return 1000000 / kelvin

def set_power(powerstate):
    data = {"on":powerstate}
    _send_command(data)

def set_both(brightness, temperature):
    brightness = _translate(brightness, 0.0, 1.0, 0, 254)
    temperature = kelvin_mired(temperature)
    data = {"bri":brightness, "ct":temperature}
    _send_command(data)

def set_brightness(brightness):
    brightness = _translate(brightness, 0.0, 1.0, 0, 254)
    data = {"bri":brightness}
    _send_command(data)

def set_temperature(temperature):
    temperature = kelvin_mired(temperature)
    data = {"ct":temperature}
    _send_command(data)

def _send_command(data):
    try:
        result = requests.put(BASEURL+"groups/0/action",data=json.dumps(data))
    except (requests.exceptions.ConnectionError, TimeoutError):
        return False
    except Exception as e:
        print("HUE: "+str(e),flush=True)
        exit()
    else:
        return True
