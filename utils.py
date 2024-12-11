import json
from datetime import datetime
import requests
from properties import BackendProperties, SysemProperties
import socket
import os
import sqlite3


def initDb():
    db_is_new = not os.path.exists(SysemProperties.db_filename)
    conn = sqlite3.connect(SysemProperties.db_filename)

    if db_is_new:
        print("creating schema")
        with conn:
            conn.execute(
                "CREATE TABLE "
                + SysemProperties.db_tablename
                + "(key PRIMARY KEY, value, lastupdated)"
            )
    else:
        print("Database exists, assume schema does, too.")

    conn.close()


def getAllMetadata():
    conn = sqlite3.connect(SysemProperties.db_filename)
    conn.execute("SELECT * FROM " + SysemProperties.db_tablename)
    rows = conn.fetchall()
    for row in rows:
        print(row)
    conn.close()
    return rows


def getMetadata(key):
    conn = sqlite3.connect(SysemProperties.db_filename)
    cur = conn.cursor()
    cur.execute(
        "SELECT value FROM "
        + SysemProperties.db_tablename
        + " WHERE key = '"
        + key
        + "'"
    )
    rows = cur.fetchone()
    conn.close()
    if not rows or len(rows) == 0:
        return ""
    else:
        for row in rows:
            return row[0]


def setMetadata(key, value):
    print("setting [" + key + "=" + value + "]")
    conn = sqlite3.connect(SysemProperties.db_filename)
    with conn:
        conn.execute(
            "insert or replace into "
            + SysemProperties.db_tablename
            + "(key, value, lastupdated) VALUES ('"
            + key
            + "', '"
            + value
            + "', '"
            + getDatetimeAsString()
            + "')"
        )
    conn.close()


def isDaytime() -> bool:
    myobj = datetime.now()
    if (
        myobj.hour >= SysemProperties.daytime_hour_start
        and myobj.hour <= SysemProperties.daytime_hour_end
    ):
        return True
    return False


def getDatetimeAsString():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def getIpAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipAddr = s.getsockname()[0]
    s.close()
    return ipAddr


def logEvent(event, aDatetime, status):
    print(
        "Event: "
        + str(event)
        + "\tDate: "
        + aDatetime
        + "\tStatus: "
        + str(status)
        + "\n"
    )
    url = (
        "http://"
        + BackendProperties.api_host
        + ":"
        + str(BackendProperties.api_port)
        + BackendProperties.events_endpoint
    )
    data = (
        '{  "eventType": "'
        + str(event.name)
        + '",  "controlStatus": "'
        + str(status.name)
        + '",  "datestamp": "'
        + str(aDatetime)
        + '",  "ipAddress": "'
        + str(getIpAddress())
        + '" }'
    )
    try:
        print("Sending event to server [" + data + "]")
        headers = {"Content-type": "application/json"}
        myResponse = requests.post(
            url, headers=headers, data=data, auth=("andy", "testPasswd"), timeout=5
        )
        if myResponse.ok:
            print(myResponse.json())
            # Loading the response data into a dict variable
            # json.loads takes in only binary or string variables so using content to fetch binary content
            # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
            jData = json.loads(myResponse.content)
            print("The response contains {0} properties".format(len(jData)))
            print("\n")
            for key in jData:
                print(key + " : " + str(jData[key]))
        else:
            print("failed to send event to server : " + url + "[" + data + "]")
            myResponse.raise_for_status()

    except requests.Timeout as err:
        print(err.args[0])
