#!/usr/bin/python

import json
from os import system, listdir, mkdir, environ, getenv
from os.path import join, isfile, isdir, getmtime
from sys import platform, exit
from time import time
from shutil import rmtree
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget
from config import *
from convertisseur import *


def nettoyage_pyinstaller(self):
    for i in listdir(environ["TMP"]):
        if i.startswith("_MEI") and isdir(i) and (int(getmtime(join(environ["TMP"], i))) < (time() - 86400)):
            rmtree(join(environ["TMP"], i))

def reset_screen(banner):
    if platform != "linux":
        system("cls")
    else:
        system("clear")
    print(*banner)

if __name__ == "__main__":
    largeur1 = 500
    hauteur1 = 350
    largeur2 = 900
    hauteur2 = 900
    background_color = [255, 255, 255]
    format_final = ".webp"
    formats_acceptes = ("jpg", "jpeg", "png", "bmp", "gif", "webp")
    json_path = join(getenv("USERPROFILE"), "AppData", "Local", "Redim")
    app = QApplication([])
    widget = QWidget()
    while True:
        redim = Redim(formats_acceptes)
        if not isfile(join(json_path, "config_redim")):
            config.sauvegarde(json_path, largeur1, hauteur1, largeur2, hauteur2, background_color, format_final)
        else:
            largeur1, hauteur1, largeur2, hauteur2, background_color, format_final = config.lecture(json_path)
        if platform != "linux":
            redim.nettoyage_pyinstaller()
        banner = (
                "\n  ____                 _                 ____   ____ \n",
                "|  _ \\ _ __ ___ _ __ (_)_   _ _ __ ___ |  _ \\ / ___|\n",
                "| |_) | '__/ _ \\ '_ \\| | | | | '_ ` _ \\| |_) | |    \n",
                "|  __/| | |  __/ | | | | |_| | | | | | |  __/| |___ \n",
                "|_|   |_|  \\___|_| |_|_|\\__,_|_| |_| |_|_|    \\____|\n",
                "\n######################################################\n",
                "\n[-] taille 1:", largeur1, "x", hauteur1, ", taille 2:", largeur2, "x", hauteur2,
                "\n[-] rgb background:", background_color,
                "\n[-] formats acceptes:", formats_acceptes,
                "\n[-] format de sortie:", format_final,
                "\n\n######################################################"
                )
        menu = (
                "\n[-] Que faire?\n",
                "\n   (1) -> Conversion (", largeur1, "x", hauteur1, "px et", largeur2, "x", hauteur2, "px)",
                "\n   (5) -> Modification des tailles",
                "\n   (6) -> Modification du RGB",
                "\n   (7) -> Modification du format de sortie",
                "\n   (8) -> Reset des parametres",
                "\n   (9) -> Quitter\n"
                )
        reset_screen(banner)
        print(*menu)
        choix = input("[>] Choix (numero) : ")
        while True:
            reset_screen(banner)
            if choix.strip() == "1":
                dossier = QFileDialog.getExistingDirectory(
                        widget,
                        "Dossier a travailler."
                        )
                print("\n[-] travail pour", largeur1, "x", hauteur1, "px :")
                redim.start(dossier, largeur1, hauteur1, tuple(background_color), format_final)
                print("\n[-] travail pour", largeur2, "x", hauteur2, "px :")
                redim.start(dossier, largeur2, hauteur2, tuple(background_color), format_final)
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
                largeur1 = dimensions[0]
                hauteur1 = dimensions[1]
                largeur2 = dimensions[2]
                hauteur2 = dimensions[3]
                config.sauvegarde(json_path, largeur1, hauteur1, largeur2, hauteur2, background_color, format_final)
                print("\n[-] Modification effectue.")
                input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                break
            elif choix.strip() == "6":
                reset_screen(banner)
                nouveau_background_color = [0, 0, 0]
                print("\n[-] Modification de la couleur du background (Valeur RGB 0-255):\n")
                for pos, i in enumerate(background_color):
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
                background_color = nouveau_background_color
                config.sauvegarde(json_path, largeur1, hauteur1, largeur2, hauteur2, background_color, format_final)
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
                        format_final = "." + formats_acceptes[nouveau_format - 1]
                        config.sauvegarde(json_path, largeur1, hauteur1, largeur2, hauteur2, background_color, format_final)
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
                largeur1 = 500
                hauteur1 = 350
                largeur2 = 900
                hauteur2 = 900
                background_color = [255, 255, 255]
                format_final = ".webp"
                config.sauvegarde(json_path, largeur1, hauteur1, largeur2, hauteur2, background_color, format_final)
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
