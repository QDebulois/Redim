from os import system
from sys import platform


class Ui:
    def __init__(self, configuration, formats_acceptes):
        self.banner = (
                "\n  ____                 _                 ____   ____ \n",
                "|  _ \\ _ __ ___ _ __ (_)_   _ _ __ ___ |  _ \\ / ___|\n",
                "| |_) | '__/ _ \\ '_ \\| | | | | '_ ` _ \\| |_) | |    \n",
                "|  __/| | |  __/ | | | | |_| | | | | | |  __/| |___ \n",
                "|_|   |_|  \\___|_| |_|_|\\__,_|_| |_| |_|_|    \\____|\n",
                "\n######################################################\n",
                "\n[-] taille 1:", configuration["largeur1"], "x", configuration["hauteur1"],
                ", taille 2:", configuration["largeur2"], "x", configuration["hauteur2"],
                "\n[-] rgb background:", configuration["background_color"],
                "\n[-] formats acceptes:", formats_acceptes,
                "\n[-] format de sortie:", configuration["format_final"],
                "\n\n######################################################"
                )
        self.menu = (
               "\n[-] Que faire?\n",
               "\n   (1) -> Conversion (", configuration["largeur1"], "x", configuration["hauteur1"],
               "px et", configuration["largeur2"], "x", configuration["hauteur2"], "px)",
               "\n   (5) -> Modification des tailles",
               "\n   (6) -> Modification du RGB",
               "\n   (7) -> Modification du format de sortie",
               "\n   (8) -> Reset des parametres",
               "\n   (9) -> Quitter\n"
               )

    def reset_screen(self):
        if platform != "linux":
            system("cls")
        else:
            system("clear")
