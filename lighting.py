import time
import adafruit_dht
import board
import platform
import requests
from properties import BackendProperties, SysemProperties, HeatingProperties
import json
import utils

dht_device = None
lightsOn = False


def init():
    print("lighting init() ")
    dht_device = adafruit_dht.DHT22(board.D17)
    # dht11_device = adafruit_dht.DHT11(board.D17)


def run():
    if utils.isDaytime() and not lightsOn:
        print("lighting on")
        lightsOn = True
        # utils.logEvent(Event.LIGHTING, LocalDateTime.now(), ControlStatus.ON)
    elif not utils.isDaytime() and lightsOn:
        print("lighting off")
        lightsOn = False
        # utils.logEvent(Event.LIGHTING, LocalDateTime.now(), ControlStatus.OFF)
