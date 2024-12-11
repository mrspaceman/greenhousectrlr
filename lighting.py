import time
import adafruit_dht
import board
import platform
import requests
from properties import (
    BackendProperties,
    SysemProperties,
    Event,
    ControlStatus,
    LightingProperties,
)
import json
import utils

dht_device = None


def init():
    print("lighting init() ")
    dht_device = adafruit_dht.DHT22(board.D17)
    # dht11_device = adafruit_dht.DHT11(board.D17)


def lightingIsOn():
    return utils.getMetadata("lighting") == "on"


def run():
    global lightsOn
    if utils.isDaytime() and not lightingIsOn():
        print("lighting on")
        utils.setMetadata("lighting", "on")
        utils.logEvent(Event.LIGHTING, utils.getDatetimeAsString(), ControlStatus.ON)
    elif not utils.isDaytime() and lightingIsOn():
        print("lighting off")
        utils.setMetadata("lighting", "off")
        utils.logEvent(Event.LIGHTING, utils.getDatetimeAsString(), ControlStatus.OFF)
