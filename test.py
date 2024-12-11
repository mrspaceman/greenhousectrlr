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
import sqlite3


# Create and fill the table.
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE lang(name, first_appeared)")
con.execute("CREATE TABLE sensorMetadata(key, value, lastupdated)")
data = [
    ("C++", 1985),
    ("Objective-C", 1984),
]
con.executemany("INSERT INTO lang(name, first_appeared) VALUES(?, ?)", data)

# Print the table contents
for row in con.execute("SELECT name, first_appeared FROM lang"):
    print(row)

print("I just deleted", con.execute("DELETE FROM lang").rowcount, "rows")

# close() is not a shortcut method and it's not called automatically;
# the connection object should be closed manually
con.close()
