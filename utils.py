import time
from datetime import datetime
from properties import BackendProperties, SysemProperties, HeatingProperties


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
