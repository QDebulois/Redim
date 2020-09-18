#!/usr/bin/python

from os import system, listdir, environ, getenv
from os.path import join, isfile, isdir, getmtime
from sys import platform, exit
from time import time
from shutil import rmtree
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget
from config import Config
from convertisseur import Redim


def nettoyage_pyinstaller():
    for i in listdir(environ["TMP"]):
        if i.startswith("_MEI") and isdir(i) and (int(getmtime(join(environ["TMP"], i))) < (time() - 86400)):
            rmtree(join(environ["TMP"], i))


def main():
    configuration = {
            "largeur1": 500,
            "hauteur1": 350,
            "largeur2": 900,
            "hauteur2": 900,
            "background_color": [255, 255, 255],
            "format_final": ".webp"
            }
    formats_acceptes = ("jpg", "jpeg", "png", "bmp", "gif", "webp")
    if platform != "linux":
        json_path = join(getenv("USERPROFILE"), "AppData", "Local", "Redim")
    else:
        json_path = "."
    app = QApplication([])
    widget = QWidget()
    while True:
        redim = Redim(formats_acceptes)
        if not isfile(join(json_path, "config_redim")):
            Config.sauvegarde(json_path, configuration)
        else:
            configuration = Config.lecture(json_path)
        if platform != "linux":
            redim.nettoyage_pyinstaller()
        choix = input("[>] Choix (numero) : ")
        while True:
            reset_screen(banner)
            if choix.strip() == "1":
                dossier = QFileDialog.getExistingDirectory(
                        widget,
                        "Dossier a travailler."
                        )
                print("\n[-] travail pour", configuration["largeur1"], "x", configuration["hauteur1"], "px :")
                redim.start(dossier, configuration["largeur1"], configuration["hauteur1"],
                            tuple(configuration["background_color"]), configuration["format_final"])
                print("\n[-] travail pour", configuration["largeur2"], "x", configuration["hauteur2"], "px :")
                redim.start(dossier, configuration["largeur2"], configuration["hauteur2"],
                            tuple(configuration["background_color"]), configuration["format_final"])
                input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                break
            elif choix.strip() == "5":
                reset_screen(banner)
                dimensions = [0, 0, 0, 0]
                for pos, i in enumerate(dimensions):
                    if pos == 0:
                        print("\n[-] Taille 1:")
                    elif pos == 2:
                        print("\n[-] Taille 2:")
                    while True:
                        texte = ["    [>] Largeur : ", "    [>] Hauteur : "]
                        dimensions[pos] = input(texte[pos % 2])
                        try:
                            dimensions[pos] = int(dimensions[pos].strip())
                            break
                        except:
                            print("    >>>ERREUR<<< Valeur incorrecte.")
                configuration["largeur1"] = dimensions[0]
                configuration["hauteur1"] = dimensions[1]
                configuration["largeur2"] = dimensions[2]
                configuration["hauteur2"] = dimensions[3]
                Config.sauvegarde(json_path, configuration)
                print("\n[-] Modification effectue.")
                input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                break
            elif choix.strip() == "6":
                reset_screen(banner)
                nouveau_background_color = [0, 0, 0]
                print("\n[-] Modification de la couleur du background (Valeur RGB 0-255):\n")
                for pos, i in enumerate(configuration["background_color"]):
                    while True:
                        texte = ["    [>] Valeur Rouge: ", "    [>] Valeur Vert: ", "    [>] Valeur Bleu: "]
                        nouveau_background_color[pos] = input(texte[pos])
                        try:
                            nouveau_background_color[pos] = int(nouveau_background_color[pos].strip())
                            if nouveau_background_color[pos] >= 0 and nouveau_background_color[pos] < 256:
                                break
                            else:
                                print("    >>>ERREUR<<< Valeur incorrecte.")
                        except:
                            print("    >>>ERREUR<<< Valeur incorrecte.")
                configuration["background_color"] = nouveau_background_color
                Config.sauvegarde(json_path, configuration)
                print("\n[-] Modification effectue.")
                input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                break
            elif choix.strip() == "7":
                print("\n[-] Modification du format de sortie:\n")
                nombre = 1
                for i in formats_acceptes:
                    nombre_choix = "(" + str(nombre) + ") ->"
                    print("   ", nombre_choix, i)
                    nombre += 1
                nouveau_format = input("\n[>] Choix (numero) : ")
                try:
                    nouveau_format = int(nouveau_format.strip())
                    if nouveau_format > 0:
                        configuration["format_final"] = "." + formats_acceptes[nouveau_format - 1]
                        Config.sauvegarde(json_path, configuration)
                        print("\n[-] Modification effectue.")
                    else:
                        print(">>>ERREUR<<< Choix invalide.")
                        input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                        break
                except:
                    print(">>>ERREUR<<< Choix invalide.")
                input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                break
            elif choix.strip() == "8":
                reset_screen(banner)
                print("\n[-] Reset des parametres.")
                configuration["largeur1"] = 500
                configuration["hauteur1"] = 350
                configuration["largeur2"] = 900
                configuration["hauteur2"] = 900
                configuration["background_color"] = [255, 255, 255]
                configuration["format_final"] = ".webp"
                Config.sauvegarde(json_path, configuration)
                print("\n[-] Modification effectue.")
                input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                break
            elif choix.strip() == "9":
                if platform != "linux":
                    system("cls")
                else:
                    system("clear")
                exit(0)
            else:
                print("\n[-] Reponse invalide .")
                input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                break


if __name__ == "__main__":
    main()
