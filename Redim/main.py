#!/usr/bin/python

from os import system, listdir, environ, getenv
from os.path import join, isfile, isdir, getmtime
from sys import platform, exit
from time import time
from shutil import rmtree
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget
from ui import Ui
from config import Config
from convertisseur import Redim



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
    config = Config()

    while True:
        redim = Redim(formats_acceptes)
        ui = Ui(configuration, formats_acceptes)
        if not isfile(join(json_path, "config_redim")):
            config.sauvegarde(json_path, configuration)
        else:
            print(json_path)
            configuration = config.lecture(json_path)
        if platform != "linux":
            config.nettoyage_pyinstaller()
        ui.affichage_banner()
        ui.affichage_menu()
        choix = input("[>] Choix (numero) : ")

        while True:
            ui.reset_screen()
            ui.affichage_banner()

            if choix.strip() == "1":
                dossier = QFileDialog.getExistingDirectory(
                        widget,
                        "Dossier a travailler."
                        )
                redim.start(dossier, configuration["largeur1"], configuration["hauteur1"],
                            tuple(configuration["background_color"]), configuration["format_final"])
                redim.start(dossier, configuration["largeur2"], configuration["hauteur2"],
                            tuple(configuration["background_color"]), configuration["format_final"])
                ui.affichage_fin()
                break
            elif choix.strip() == "5":
                ui.reset_screen()
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
                config.sauvegarde(json_path, configuration)
                print("\n[-] Modification effectue.")
                ui.affichage_fin()
                break
            elif choix.strip() == "6":
                ui.reset_screen()
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
                config.sauvegarde(json_path, configuration)
                print("\n[-] Modification effectue.")
                ui.affichage_fin()
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
                        config.sauvegarde(json_path, configuration)
                        print("\n[-] Modification effectue.")
                    else:
                        print(">>>ERREUR<<< Choix invalide.")
                        ui.affichage_fin()
                        break
                except:
                    print(">>>ERREUR<<< Choix invalide.")
                ui.affichage_fin()
                break
            elif choix.strip() == "8":
                ui.reset_screen()
                print("\n[-] Reset des parametres.")
                configuration["largeur1"] = 500
                configuration["hauteur1"] = 350
                configuration["largeur2"] = 900
                configuration["hauteur2"] = 900
                configuration["background_color"] = [255, 255, 255]
                configuration["format_final"] = ".webp"
                config.sauvegarde(json_path, configuration)
                print("\n[-] Modification effectue.")
                ui.affichage_fin()
                break
            elif choix.strip() == "9":
                if platform != "linux":
                    system("cls")
                else:
                    system("clear")
                exit(0)
            else:
                print("\n[-] Reponse invalide .")
                ui.affichage_fin()
                break


if __name__ == "__main__":
    main()
