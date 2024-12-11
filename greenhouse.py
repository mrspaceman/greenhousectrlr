# https://github.com/adafruit/Adafruit_CircuitPython_DHT

import platform
import utils

import heating
import lighting
import watering

platformName = platform.system()
print(platformName)

# try:
#     f = open('/home/andy/dht22/greenhouse.csv', 'a+')
#     if os.stat('/home/andy/dht22/greenhouse.csv').st_size == 0:
#         f.write('Date,Time,Temperature C, Temperature F,Humidity\r\n')
# except:
#     pass

utils.initDb()

while True:
    heating.run()
    lighting.run()
    watering.run()
