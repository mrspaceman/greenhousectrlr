from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import socket


class Event(Enum):
    LIGHTING = "LIGHTING"
    HEATING = "HEATING"
    WATERING = "WATERING"
    VENTILATION = "VENTILATION"
    OTHER = "OTHER"


class ControlStatus(Enum):
    ON = "ON"
    OFF = "OFF"
    UNKNOWN = "UNKNOWN"


@dataclass
class SysemProperties:
    """Properties of the whole system."""

    hostname = socket.gethostname()
    fqdn = socket.getfqdn()
    name = "greenhouse_controller"
    version = "0.1.0"
    sleep_minutes = 30
    sleep_minutes_lighting = 30
    sleep_minutes_heating = 30
    daytime_hour_start = 7
    daytime_hour_end = 18
    minimum_day_temp = 22.0
    maximum_day_temp = 28.0
    minimum_night_temp = 16.0
    maximum_night_temp = 19.0
    watering_start_time = "06:00"
    watering_duration = 2

    def isDaytime(self) -> bool:
        myobj = datetime.now()
        if (
            myobj.hour >= self.daytime_hour_start
            and myobj.hour <= self.daytime_hour_end
        ):
            return True
        return False


@dataclass
class HeatingProperties:
    pin_sensor_temperature_1 = 11
    pin_sensor_temperature_2 = 11
    daytime_min_temp = 24
    daytime_max_temp = 28
    nighttime_min_temp = 18
    nighttime_max_temp = 21
    pin_control_heat_mat_1 = 11
    pin_control_heat_mat_2 = 27


@dataclass
class LightingProperties:
    pin_sensor_light_1 = 11
    pin_sensor_light_2 = 11
    pin_control_lights_1 = 11
    pin_control_lights_2 = 27


@dataclass
class WateringProperties:
    pin_sensor_soil_1 = 11
    pin_sensor_soil_2 = 11
    pin_control_pump_1 = 11
    pin_control_pump_2 = 27
    pin_control_pump_3 = 27


@dataclass
class BackendProperties:
    """Properties of the backend API."""

    api_host = "192.168.2.12"
    api_port = 8899
    events_endpoint = "/api/events"
    heating_endpoint = "/api/heating"
    lighting_endpoint = "/api/lighting"
    watering_endpoint = "/api/watering"
