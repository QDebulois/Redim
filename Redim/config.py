"""Contient la gestion de l'enregistrement des choix de l'utilisateur
ainsi que la gestion de la supression des fichiers anciennement décompressés
par pyinstaller"""

from os import mkdir, listdir, environ, getenv, system
from os.path import isdir, join, getmtime, isfile
from time import time
from shutil import rmtree
import sys
import json
import logging
import traceback


class Config():
    """Gestion de l'enregistrement des choix de l'utilisateur
    """
    def __init__(self):
        self.base_configuration = {
            "version": 1.0,
            "dimensions": [[500, 350], [800, 800]],
            "background": [255, 255, 255],
            "transparence": False,
            "formats_acceptes": (
                "webp",
                "png",
                "jpg",
                "jpeg",
                "bmp",
                "gif"
            ),
            "formats_possibles": (
                "webp",
                "png",
                "jpg"
            ),
            "format_choisi": ""
        }
        self.user_profile = getenv("USERPROFILE")
        if sys.platform != "linux":
            self.json_path = join(
                self.user_profile,
                "AppData",
                "Local",
                "Redim"
            )
        else:
            self.json_path = "."
        if sys.platform != "linux":
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

    def reset(self):
        """Suppression et réenregistrement de la configuration par défaut si
        le dossier de configuration existe
        """
        if isdir(self.json_path):
            rmtree(self.json_path)
            self.sauvegarde(self.base_configuration)

    @staticmethod
    def excepthook(type, value, error_traceback):
        """Système de journalisation en cas de plantage.
        """
        logging.error(
            "\nType: " + type.__name__ + "\n"
            + "Info: " + str(value) + "\n\n"
            + "".join(traceback.format_tb(error_traceback))
            + "\n==============================="
        )
        print(
            "\nTraceback:\n\n"
            + "Type: " + type.__name__ + "\n"
            + "Info: " + str(value) + "\n\n"
            + "".join(traceback.format_tb(error_traceback)) + "\n"
        )
        sys.exit(1)

    @staticmethod
    def nettoyage_pyinstaller():
        """Supression des fichiers anciennement décompressés par pyinstaller
        """
        for i in listdir(environ["TMP"]):
            if i.startswith("_MEI")\
                and isdir(i)\
                    and (
                            int(getmtime(join(environ["TMP"], i)))
                            < (time() - 86400)):
                rmtree(join(environ["TMP"], i))

    @staticmethod
    def redimensionnement_fenetre():
        """Redimensionne la fenetre du CMD sous windows
        """
        if sys.platform != "linux":
            system("mode con: cols=70 lines=35")
