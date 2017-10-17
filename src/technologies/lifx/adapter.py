#!/usr/bin/env python3
# coding: utf-8
#

import lifxlan

def init(config_values):
    pass

def _translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return int( rightMin + (valueScaled * rightSpan) )

def set_both(brightness, temperature):
    brightness = max(_translate(brightness, 0.0, 1.0, 0, 65535),1)
    temperature = max(2500,temperature)
    try:
        lifx = lifxlan.LifxLAN()
        devices = lifx.get_lights()
        for d in devices:
            d.set_brightness(brightness)
            d.set_colortemp(temperature)
    except (lifxlan.errors.InvalidParameterException, lifxlan.errors.WorkflowException, TimeoutError):
        return False
    except Exception as e:
        print("LIFX: "+str(e),flush=True)
        exit()
    else:
        return True
def set_brightness(brightness):
    brightness = max(_translate(brightness, 0.0, 1.0, 0, 65535),1)
    try:
        lifx = lifxlan.LifxLAN()
        devices = lifx.get_lights()
        for d in devices:
            d.set_brightness(brightness)
    except (lifxlan.errors.InvalidParameterException, lifxlan.errors.WorkflowException, TimeoutError):
        return False
    except Exception as e:
        print("LIFX: "+str(e),flush=True)
        exit()
    else:
        return True
def set_temperature(temperature):
    temperature = max(2500,temperature)
    try:
        lifx = lifxlan.LifxLAN()
        devices = lifx.get_lights()
        for d in devices:
            d.set_colortemp(temperature)
    except (lifxlan.errors.InvalidParameterException, lifxlan.errors.WorkflowException, TimeoutError):
        return False
    except Exception as e:
        print("LIFX: "+str(e),flush=True)
        exit()
    else:
        return True
