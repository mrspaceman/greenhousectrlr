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

pump_1 = None


def lastWatered():
    return utils.getMetadata("lastWatered")


def run():
    print("Hello, ")
