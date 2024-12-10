import json
from datetime import datetime
import requests
from properties import BackendProperties, SysemProperties


def isDaytime() -> bool:
    myobj = datetime.now()
    if (
        myobj.hour >= SysemProperties.daytime_hour_start
        and myobj.hour <= SysemProperties.daytime_hour_end
    ):
        return True
    return False


def getDatetimeAsString():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def logEvent(event, aDatetime, status):
    print("Event: " + event + "\tDate: " + aDatetime + "\tStatus: " + status + "\n")
    url = (
        "http://"
        + BackendProperties.api_host
        + ":"
        + BackendProperties.api_port
        + BackendProperties.events_endpoint
    )
    data = (
        '{  "eventType": "'
        + event
        + '",  "controlStatus": "'
        + status
        + '",  "datestamp": "'
        + aDatetime
        + '"    }'
    )
    myResponse = requests.post(url, data=data)
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
        print("failed to send event to server : " + url)
        myResponse.raise_for_status()
