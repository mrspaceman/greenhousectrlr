#!/bin/bash

if [ ! -d "./env" ]; then
    python3 -m venv env
    
    source env/bin/activate
        
    python3 -m pip install adafruit-circuitpython-dht
    # python3 -m pip install adafruit-circuitpython-lis3dh

    python3 -m pip install requests
else
    source env/bin/activate
fi

python3 ./greenhouse.py


