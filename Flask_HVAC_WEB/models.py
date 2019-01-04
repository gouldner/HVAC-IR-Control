import json

class AvailableCommands:
    def __init__(self):
        self.climate_modes = []
        self.isee_modes = []
        self.powerful_modes = []
        self.vanne_horizontal_modes = []
        self.fan_modes = []
        self.vanne_vertical_modes = []
        self.area_modes = []
        self.min_temp = -1
        self.max_temp = -1

class HvacCommandResponse:
    def __init__(self, success, command, decoded):
        self.success = success
        self.command = command
        self.decoded_command = decoded

class HvacCommand:
    def __init__(self):
        self.climate_mode = "Cold"
        self.isee_mode = "ISeeOn"
        self.powerful_mode = "PowerfulOff"
        self.vanne_horizontal_mode = "NotSet"
        self.fan_mode = "Auto"
        self.vanne_vertical_mode = "Auto"
        self.area_mode = "NotSet"
        self.temperature = 21
        self.start_time = None
        self.end_time = None
    
    def from_json(self, data):
        self.climate_mode = data["climate_mode"]
        self.isee_mode = data["isee_mode"]
        self.powerful_mode = data["powerful_mode"]
        self.vanne_horizontal_mode = data["vanne_horizontal_mode"]
        self.fan_mode = data["fan_mode"]
        self.vanne_vertical_mode = data["vanne_vertical_mode"]
        self.area_mode = data["area_mode"]
        self.temperature = data["temperature"]
        self.start_time = data["start_time"]
        self.end_time = data["end_time"]

    def to_json(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=4, separators=(',', ': '))
