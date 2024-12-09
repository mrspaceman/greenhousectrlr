#!/bin/bash

python3 -m venv env

source env/bin/activate

python3 -m pip install adafruit-circuitpython-dht

python3 ~/dht22/humidity.py


