import time
from datetime import datetime
import adafruit_dht
import board
import platform
import requests
from properties import (
    BackendProperties,
    SysemProperties,
    HeatingProperties,
    Event,
    ControlStatus,
)
import json
import utils

dht_device_temp_1 = None
dht_device_temp_2 = None
dht_device_heat_1 = None
dht_device_heat_2 = None
dht_device_heat_3 = None

heatingIsOn = False


def sendToBackend(temperature, humidity):
    url = (
        "http://"
        + BackendProperties.api_host
        + ":"
        + str(BackendProperties.api_port)
        + BackendProperties.heating_endpoint
    )
    data = (
        '{  "temperature": '
        + str(temperature)
        + ',  "humidity": '
        + str(humidity)
        + ',  "sensorId": "t001",  "sensorName": "temp ghouse 001",  "datestamp": "'
        + str(datetime.now)
        + '"}'
    )
    myResponse = requests.post(url, data=data, auth=("andy", "testPasswd"), timeout=5)
    if myResponse.ok:
        print("response: " + myResponse.json())
        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(myResponse.content)
        print("The response contains {0} properties".format(len(jData)))
        print("\n")
        for key in jData:
            print(key + " : " + jData[key])
    else:
        print("failed to send readings to server : " + url + "[" + data + "]")
        myResponse.raise_for_status()


def run():
    dht_device_temp_1 = adafruit_dht.DHT22(board.D17)  # pin 11 - GPIO 17
    try:
        temperature_c = dht_device_temp_1.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dht_device_temp_1.humidity

        print("Temp:{:.1f} C    Humidity: {}%".format(temperature_c, humidity))
        sendToBackend(str(temperature_c), str(humidity))

        if utils.isDaytime():
            if temperature_c < HeatingProperties.daytime_min_temp and not heatingIsOn:
                print("heating on")
                heatingIsOn = True
                utils.logEvent(Event.HEATING, datetime.now(), ControlStatus.ON)
            elif temperature_c > HeatingProperties.daytime_max_temp and heatingIsOn:
                print("heating off")
                heatingIsOn = False
                utils.logEvent(Event.HEATING, datetime.now(), ControlStatus.OFF)
        else:
            if temperature_c < HeatingProperties.nighttime_min_temp and not heatingIsOn:
                print("heating on")
                heatingIsOn = True
                utils.logEvent(Event.HEATING, datetime.now(), ControlStatus.ON)
            elif temperature_c > HeatingProperties.nighttime_max_temp and heatingIsOn:
                print("heating off")
                heatingIsOn = False
                utils.logEvent(Event.HEATING, datetime.now(), ControlStatus.OFF)

    except RuntimeError as err:
        print(err.args[0])

    print("heating tidy up dht sensor")
    dht_device_temp_1.exit()
