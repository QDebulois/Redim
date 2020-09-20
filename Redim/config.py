"""Contient la gestion de l'enregistrement des choix de l'utilisateur
ainsi que la gestion de la supression des fichiers anciennement décompressés
par pyinstaller"""

from sys import platform
from os import mkdir, listdir, environ, getenv, system
from os.path import isdir, join, getmtime, isfile
from time import time
from shutil import rmtree
import json


class Config():
    """Gestion de l'enregistrement des choix de l'utilisateur"""
    def __init__(self):
        self.base_configuration = {
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
        """Création du dossier de sauvegarde pour le fichier de configuration
        et enregistrement des préférence de l'utilisateur
        """
        if not isdir(self.json_path):
            mkdir(self.json_path)
        with open(join(self.json_path, "config"), "w") as file_config:
            json.dump(configuration, file_config)
        print("\n[-] Modification enregistree.")

    def lecture(self):
        """Return le contenu du fichier de configuration, si aucun fichier
        n'éxiste, création d'un avec les valeurs par défaut
        """
        if not isfile(join(self.json_path, "config")):
            self.sauvegarde(self.base_configuration)
            return self.base_configuration
        with open(join(self.json_path, "config"), "r") as file_config:
            configuration = json.load(file_config)
        return configuration

    @staticmethod
    def nettoyage_pyinstaller():
        """Supression des fichiers anciennement décompressés par pyinstaller"""
        for i in listdir(environ["TMP"]):
            if i.startswith("_MEI")\
                and isdir(i)\
                    and (
                            int(getmtime(join(environ["TMP"], i)))
                            < (time() - 86400)):
                rmtree(join(environ["TMP"], i))

    @staticmethod
    def redimensionnement_fenetre():
        """Redimensionne la fenetre du CMD sous windows"""
        if platform != "linux":
            system("mode con: cols=70 lines=35")
