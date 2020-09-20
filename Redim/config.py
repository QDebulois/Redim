from sys import platform
from os import mkdir, listdir, environ, getenv
from os.path import isdir, join, getmtime, isfile
from time import time
from shutil import rmtree
import json


class Config():
    def __init__(self):
        self._base_configuration = {
            "dimensions": [[500, 350], [900, 900]],
            "background": [255, 255, 255],
            "format_final": ".webp",
            "formats_acceptes": (
                "jpg",
                "jpeg",
                "png",
                "bmp",
                "gif",
                "webp"
            )
        }
        if platform != "linux":
            self.json_path = join(
                getenv("USERPROFILE"),
                "AppData",
                "Local",
                "Redim"
            )
        else:
            self.json_path = "."
        if platform != "linux":
            self.nettoyage_pyinstaller()

    def sauvegarde(self, configuration):
        if not isdir(self.json_path):
            mkdir(self.json_path)
        with open(join(self.json_path, "config"), "w") as f:
            json.dump(configuration, f)
        print("\n[-] Modification enregistree.")

    def lecture(self):
        if not isfile(join(self.json_path, "config")):
            self.sauvegarde(self._base_configuration)
            return self._base_configuration
        with open(join(self.json_path, "config"), "r") as f:
            configuration = json.load(f)
        return configuration

    def nettoyage_pyinstaller(self):
        for i in listdir(environ["TMP"]):
            if i.startswith("_MEI") and isdir(i) and (int(getmtime(join(environ["TMP"], i))) < (time() - 86400)):
                rmtree(join(environ["TMP"], i))
