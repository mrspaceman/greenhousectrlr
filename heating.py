
import time
import adafruit_dht
import board
import platform
import requests
from properties import BackendProperties, SysemProperties, HeatingProperties
import json
import utils

dht_device_temp_1 = None
dht_device_temp_2 = None
dht_device_heat_1 = None
dht_device_heat_2 = None
dht_device_heat_3 = None

def init():
  print("heating init() ")
  dht_device_temp_1 = adafruit_dht.DHT22(board.D17)
  # dht11_device = adafruit_dht.DHT11(board.D17)

def run(name):
    try:
        temperature_c = dht_device_temp_1.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dht_device_temp_1.humidity

        print("Temp:{:.1f} C    Humidity: {}%".format(temperature_c, humidity))
        sendToBackend(str(temperature_c), str(humidity))
        
        if (utils.isDaytime()):
            if (temperature_c < HeatingProperties.daytime_min_temp):
                print("heating on")
                # utils.logEvent(log, Event.HEATING, LocalDateTime.now(), ControlStatus.ON)
            elif (temperature_c > HeatingProperties.daytime_max_temp):
                print("heating off")
                # utils.logEvent(log, Event.HEATING, LocalDateTime.now(), ControlStatus.OFF)
        else:
            if (temperature_c < HeatingProperties.nighttime_min_temp):
                print("heating on")
                # utils.logEvent(log, Event.HEATING, LocalDateTime.now(), ControlStatus.ON)
            elif (temperature_c > HeatingProperties.nighttime_max_temp):
                print("heating off")
                # utils.logEvent(log, Event.HEATING, LocalDateTime.now(), ControlStatus.OFF)
                
    except RuntimeError as err:
        print(err.args[0])


def sendToBackend(temperature, humidity):
  url = 'http://' + BackendProperties.api_host +':' + BackendProperties.api_port + '/api/temperature'
  data = '''{
    "sensor_id": "t01",
    "datetime": "''' + utils.getDatetimeAsString() + '''",
    "sensor_type": "dht22",
    "sensor_value": {
      "temperature": ''' + temperature + ''',
      "humidity": ''' + humidity + '''
    }
  }'''
  myResponse = requests.post(url, data=data)
  if(myResponse.ok):
    print('response: ' + myResponse.json())
    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(myResponse.content)
    print("The response contains {0} properties".format(len(jData)))
    print("\n")
    for key in jData:
        print key + " : " + jData[key]
  else:
    print('failed to send readings to server : ' + url)
    myResponse.raise_for_status()
  