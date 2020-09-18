import json
from time import time
from shutil import rmtree
from os import mkdir, listdir, environ
from os.path import isdir, join, getmtime


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

    def nettoyage_pyinstaller(self):
        for i in listdir(environ["TMP"]):
            if i.startswith("_MEI") and isdir(i) and (int(getmtime(join(environ["TMP"], i))) < (time() - 86400)):
                rmtree(join(environ["TMP"], i))
