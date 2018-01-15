#!/usr/bin/env python3
# coding: utf-8
#

import lifxlan

def init(config_values):
    global lifx, last_brightness, last_temperature
    last_brightness = 65535
    last_temperature = 4000
    lifx = lifxlan.LifxLAN()

def _translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return int( rightMin + (valueScaled * rightSpan) )

def set_both(brightness, temperature):
    brightness = max(_translate(brightness, 0.0, 1.0, 0, 65535),1)
    temperature = max(2500,temperature)
    try:
        lifx.set_color_all_lights([0,0,brightness,temperature],duration=400,rapid=True)
    except (lifxlan.errors.InvalidParameterException, lifxlan.errors.WorkflowException, TimeoutError):
        return False
    except Exception as e:
        print("LIFX: "+str(e),flush=True)
        exit()
    else:
        return True
def set_brightness(brightness):
    global last_brightness
    brightness = max(_translate(brightness, 0.0, 1.0, 0, 65535),1)
    try:
        lifx.set_color_all_lights([0,0,brightness,last_temperature],duration=400,rapid=True)
        last_brightness = brightness
    except (lifxlan.errors.InvalidParameterException, lifxlan.errors.WorkflowException, TimeoutError):
        return False
    except Exception as e:
        print("LIFX: "+str(e),flush=True)
        exit()
    else:
        return True
def set_temperature(temperature):
    global last_temperature
    temperature = max(2500,temperature)
    try:
        lifx.set_color_all_lights([0,0,last_brightness,temperature],duration=400,rapid=True)
        last_temperature = temperature
    except (lifxlan.errors.InvalidParameterException, lifxlan.errors.WorkflowException, TimeoutError):
        return False
    except Exception as e:
        print("LIFX: "+str(e),flush=True)
        exit()
    else:
        return True
