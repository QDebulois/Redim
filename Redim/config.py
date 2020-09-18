import json
from os import mkdir
from os.path import isdir, join


class Config():
    def sauvegarde(self, json_path, configuration):
        if not isdir(json_path):
            mkdir(json_path)
        with open(join(json_path, "config_redim"), "w") as f:
            json.dump(configuration, f)

    def lecture(self, json_path):
        with open(join(json_path, "config_redim"), "r") as f:
            configuration = json.load(f)
        return configuration
