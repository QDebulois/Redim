"""Contient toute la partie 'TUI' de Redim"""

from os import system
from sys import platform


class Ui:
    """Gestion de l'interaction avec l'utilisateur"""
    def __init__(self, configuration):
        self.banner = (
            "\n  ____                 _                 ____   ____ \n",
            "|  _ \\ _ __ ___ _ __ (_)_   _ _ __ ___ |  _ \\ / ___|\n",
            "| |_) | '__/ _ \\ '_ \\| | | | | '_ ` _ \\| |_) | |    \n",
            "|  __/| | |  __/ | | | | |_| | | | | | |  __/| |___ \n",
            "|_|   |_|  \\___|_| |_|_|\\__,_|_| |_| |_|_|    \\____|\n",
            "\n######################################################\n",
            "\n[-] tailles (lxh): {0}".format(
                ", ".join(map(
                    str,
                    ["x".join(map(str, configuration["dimensions"][i]))
                     for i in range(len(configuration["dimensions"]))]
                ))
            ),
            "\n[-] rgb background:", configuration["background"],
            "\n[-] formats acceptes:", configuration["formats_acceptes"],
            "\n[-] format de sortie:", configuration["format_final"],
            "\n\n######################################################"
        )
        self.menu = (
            "\n[-] Que faire?\n",
            "\n   (1) -> Conversions",
            "\n   (5) -> Modification des tailles",
            "\n   (6) -> Modification du RGB",
            "\n   (7) -> Modification du format de sortie",
            "\n   (8) -> Reset des parametres",
            "\n   (9) -> Quitter\n"
        )

    def affichage_banner(self):
        """Reset de l'écran + affichage de la 'banner'"""
        self.reset_screen()
        print(*self.banner)

    def affichage_menu(self):
        """Affichage du menu principal"""
        print(*self.menu)

    @staticmethod
    def question_taille(configuration):
        """Récupère largeur & hauteur pour chaques tailles
        enregistrées dans la configuration initiale
        """
        texte = [
            "    [>] Largeur: ",
            "    [>] Hauteur: "
        ]
        tailles = []
        for i in range(len(configuration)):
            print("\n[-] Taille {0!s}:".format(i + 1))
            dimensions = []
            for j in texte:
                while True:
                    reponse = input(j)
                    try:
                        reponse = int(reponse.strip())
                        if 5 < reponse < 5000:
                            dimensions.append(reponse)
                            break
                        print("    [ERREUR] La valeur trop petite"
                              " ou trop grande.")
                    except ValueError:
                        print("    [ERREUR] La valeur entree"
                              " n'est pas un chiffre.")
            tailles.append(dimensions)
        return tailles

    @staticmethod
    def question_background(configuration):
        """Récupère 3 valeurs entre 0 & 255 pour la couleur qui servira
        en remplissage si les photos sont redimensionnées ou avec alpha
        """
        texte = [
            "    [>] Valeur Rouge: ",
            "    [>] Valeur Vert: ",
            "    [>] Valeur Bleu: "
        ]
        background = []
        print(
            "\n[-] Modification de la couleur"
            " du background (Valeur RGB 0-255):\n"
        )
        for i in range(len(configuration)):
            while True:
                reponse = input(texte[i])
                try:
                    reponse = int(reponse.strip())
                    if 0 <= reponse < 256:
                        background.append(reponse)
                        break
                    print("    [ERREUR] La valeur trop petite"
                          " ou trop grande.")
                except ValueError:
                    print("    [ERREUR] La valeur entree"
                          " n'est pas un chiffre.")
        return background

    @staticmethod
    def question_format_final(configuration):
        """Récupère le choix de sortie en fonction des formats
        acceptés dans la configuration initiale
        """
        print("\n[-] Modification du format de sortie:\n")
        for pos, i in enumerate(configuration[1:]):
            print(
                "    ("
                + str(pos + 1)
                + ") ->",
                i
            )
        while True:
            reponse = input("\n[>] Choix (numero) : ")
            try:
                reponse = int(reponse.strip())
                if 0 < reponse <= len(configuration[1:]):
                    format_final = "." + configuration[reponse]
                    return format_final
                print("[ERREUR] Choix en dehors des possibilites.")
            except ValueError:
                print("[ERREUR] La valeur entree n'est pas un chiffre.")

    @staticmethod
    def affichage_fin():
        """Bête appuye sur entrer pour continuer"""
        input("\n[-] fin, appuyer sur \'entrer\' pour continuer.")

    @staticmethod
    def reset_screen():
        """Reset de l'écran, cls pour CMD windows"""
        if platform != "linux":
            system("cls")
        else:
            system("clear")
