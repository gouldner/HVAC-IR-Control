#!/usr/bin/python
from hvac_ircontrol.ir_sender import LogLevel
from hvac_ircontrol.mitsubishi import Mitsubishi, ClimateMode, FanMode, VanneVerticalMode, VanneHorizontalMode, ISeeMode, AreaMode, PowerfulMode, Constants
from models import *
import inspect
import json
from collections import namedtuple
import datetime
import traceback
import os

path = "/hvac/last_config.json"


def list_config(app):
    res = AvailableCommands()
    res.climate_modes = __list_attributes(ClimateMode)
    res.isee_modes = __list_attributes(ISeeMode)
    res.powerful_modes = __list_attributes(PowerfulMode)
    res.vanne_horizontal_modes = __list_attributes(VanneHorizontalMode)
    res.fan_modes = __list_attributes(FanMode)
    res.vanne_vertical_modes = __list_attributes(VanneVerticalMode)
    res.area_modes = __list_attributes(AreaMode)
    res.min_temp = Constants.MinTemp
    res.max_temp = Constants.MaxTemp
    return res

def power_off(app):
    hvac = Mitsubishi(17, LogLevel.ErrorsOnly)
    hvac.power_off()
    return "It was powered OFF"

def last_command(app):
    command = HvacCommand()
    if os.path.isfile(path):
        with open(path, 'r') as content_file:
            data = json.loads(content_file.read())
            command.from_json(data)
    return command

def send_command(app, data):
    command = HvacCommand()
    command.from_json(data)
    return __send_command(app, command)

def send_last_command(app):
    return __send_command(app, last_command(app))

def __send_command(app, command):
    try:
        hvac = Mitsubishi(17, LogLevel.Minimal)
        args = dict(
            climate_mode=__get_value(ClimateMode, command.climate_mode),
            temperature=command.temperature,
            fan_mode=__get_value(FanMode, command.fan_mode),
            vanne_vertical_mode=__get_value(VanneVerticalMode, command.vanne_vertical_mode),
            vanne_horizontal_mode=__get_value(VanneHorizontalMode, command.vanne_horizontal_mode),
            isee_mode=__get_value(ISeeMode, command.isee_mode),
            area_mode=__get_value(AreaMode, command.area_mode),
            start_time = __get_time_value(command.start_time),
            end_time = __get_time_value(command.end_time),
            powerful=__get_value(PowerfulMode, command.powerful_mode))
        hvac.send_command(**args)

        cfg = open(path, "w")
        cfg.write(command.to_json())
        return HvacCommandResponse(True,command,args)
    except:
        app.logger.error("There was an error: {0}".format(traceback.format_exc()))
        return HvacCommandResponse(False,data,"There was an error: {0}".format(traceback.format_exc()))

def __list_attributes(my_type):
    return [a[0] for a in inspect.getmembers(my_type, lambda c:not(inspect.isroutine(c))) if not a[0].startswith('_')]

def __get_value(my_type, my_value):
    return [a[1] for a in inspect.getmembers(my_type, lambda c:not(inspect.isroutine(c))) if a[0] == my_value][0]

def __get_time_value(my_value):
    if my_value is None or my_value < 0 or my_value >= 24:
        return None
    
    return datetime.time(int(my_value)//1, int((my_value*100)%100))
