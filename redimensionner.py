#!/usr/bin/python

"""
Nécessite Pillow & PyQt5
"""

from os import system, listdir, mkdir, environ
from os.path import join, isfile, isdir, getmtime
from sys import platform, exit
from time import time
from shutil import rmtree
from PIL.Image import ANTIALIAS
from PIL.Image import new as image_new
from PIL.Image import open as image_open
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget


class Redim():
    def __init__(self, formats_acceptes):
        self.formats_acceptes = formats_acceptes

    def start(self, dossier, larg, haut, background_color, format_final):
        if dossier == "":
            print("    >>>ERREUR<<< : Aucun dossier selectionne.")
            return
        if isdir(dossier):
            liste_fichier, dossier_sauvegarde = self.listage_fichiers_et_dossiers(dossier, larg)
            self.main(liste_fichier, dossier_sauvegarde, larg, haut, background_color, format_final)
        else:
            print("    >>>ERREUR<<< : Le dossier n'existe plus.")

    def listage_fichiers_et_dossiers(self, dossier, larg):
        liste_fichier = []
        dossier_sauvegarde = join(dossier, str(larg))
        if not isdir(dossier_sauvegarde):
            mkdir(dossier_sauvegarde)
        for nom in listdir(dossier):
            if isfile(join(dossier, nom)):
                if join(dossier, nom).rsplit(".", 1)[-1] in self.formats_acceptes:
                    liste_fichier.append([join(dossier, nom), nom])
        return liste_fichier, dossier_sauvegarde

    def suppression_de_alpha(self, img, background_color):
        img = img.convert("RGBA")
        if img.mode in ("RGBA", "LA"):
            fond = image_new(img.mode[:-1], img.size, background_color)
            fond.paste(img, img.split()[-1])
            img = fond
        img.convert("RGB")
        return img

    def redimensionnement(self, img, larg, haut):
        if (img.size[0] >= larg) or (img.size[1] >= haut):
            img.thumbnail((larg, haut), ANTIALIAS)
        elif (img.size[0] / img.size[1]) <= (larg / haut):
            nouvelle_larg = int(haut * img.size[0] / img.size[1])
            img = img.resize((nouvelle_larg, haut), ANTIALIAS)
        else:
            nouvelle_haut = int(larg * img.size[1] / img.size[0] )
            img = img.resize((larg, nouvelle_haut), ANTIALIAS)
        return img

    def rennomage(self, origine_nom, larg, format_final):
        charcters_indesirable = ("(", ")", "[", "]", "{", "}","'", "#",
                "&","$","£", "¤", "€", "`", "^", "°", "¨",
                "@", "!", ",", "~", "%", ";", "µ", "§")
        charcters_underscore = (" ", "-")
        nouveau_nom = origine_nom
        for i in charcters_indesirable:
            nouveau_nom = nouveau_nom.replace(i, "")
        for i in charcters_underscore:
            nouveau_nom = nouveau_nom.replace(i, "_")
        return nouveau_nom + "_modif_" + str(larg) + format_final

    def main(self, liste_fichier, dossier_sauvegarde, larg, haut, background_color, format_final):
        for nom in liste_fichier:
            try:
                print("    [+] Travail sur :", nom[1])
                img = image_open(nom[0])
                print("        >> Taille initiale :", img.size[0] ,"x" ,img.size[1], "px")
                if nom[1].rsplit(".", 1)[-1] in ("png", "webp"):
                    img = self.suppression_de_alpha(img, background_color)
                img = self.redimensionnement(img, larg, haut)
                print("        >> Taille apres redimensionnement :", img.size[0] ,"x" ,img.size[1], "px")
                nouveau_nom = self.rennomage(nom[1].rsplit(".", 1)[0], larg, format_final)
                fond = image_new("RGB", (larg, haut), background_color)
                fond.paste(img, ((larg - img.size[0]) // 2, (haut - img.size[1]) // 2))
                if isfile(join(dossier_sauvegarde, nouveau_nom)):
                    adverbes_multplicatifs = ("_bis", "_ter", "_quater", "_quinquies", "_sexies", "_septies")
                    nom_deja_present = nouveau_nom
                    iteration = 0
                    while isfile(join(dossier_sauvegarde, nom_deja_present)):
                        nom_deja_present = nouveau_nom.rsplit(".", 1)[0] + adverbes_multplicatifs[iteration]
                        nom_deja_present += format_final
                        iteration += 1
                    fond.save(join(dossier_sauvegarde, nom_deja_present))
                else:
                    fond.save(join(dossier_sauvegarde, nouveau_nom))
            except Exception as e:
                print("    >>>ERREUR<<< : ", e)

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
    formats_acceptes = ("jpg", "jpeg", "png", "bmp", "gif", "webp")
    format_final = ".webp"
    app = QApplication([])
    widget = QWidget()
    if platform != "linux":
        redim.nettoyage_pyinstaller()
    while True:
        redim = Redim(formats_acceptes)
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
                "\n   (6) -> Modification des tailles",
                "\n   (7) -> Modification du RGB",
                "\n   (8) -> Modification du format de sortie",
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
            elif choix.strip() == "6":
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
                print("\n[-] Modification effectue.")
                input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                break
            elif choix.strip() == "7":
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
                print("\n[-] Modification effectue.")
                input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                break
            elif choix.strip() == "8":
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
                        print("\n[-] Modification effectue.")
                    else:
                        print(">>>ERREUR<<< Choix invalide.")
                        input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                        break
                except:
                    print(">>>ERREUR<<< Choix invalide.")
                input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                break
            elif choix.strip() == "9":
                exit(0)
            else:
                print("\n[-] Reponse invalide .")
                input("\n[-] fin, appuyer sur \'entrer\' pour recommencer .")
                break
