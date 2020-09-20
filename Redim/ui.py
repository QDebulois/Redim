from os import system
from sys import platform


class Ui:
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
        print(*self.banner)

    def affichage_menu(self):
        print(*self.menu)

    def question_taille(self, configuration):
        texte = [
            "    [>] Largeur : ",
            "    [>] Hauteur : "
        ]
        tailles = []
        for i in range(len(configuration)):
            print("\n[-] Taille {0!s}:".format(i + 1))
            dimensions = []
            for j in range(len(texte)):
                while True:
                    reponse = input(texte[j])
                    try:
                        reponse = int(reponse.strip())
                        if reponse > 0:
                            dimensions.append(reponse)
                            break
                        else:
                            print("    >>>ERREUR<<< Valeur incorrecte.")
                    except:
                        print("    >>>ERREUR<<< Valeur incorrecte.")
            tailles.append(dimensions)
        return tailles

    def question_background(self, configuration):
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
                    if reponse >= 0 and reponse < 256:
                        background.append(reponse)
                        break
                    else:
                        print("    >>>ERREUR<<< Valeur incorrecte.")
                except:
                    print("    >>>ERREUR<<< Valeur incorrecte.")
        return background

    def question_format_final(self, configuration):
        print("\n[-] Modification du format de sortie:\n")
        for pos, i in enumerate(configuration):
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
                if reponse > 0:
                    format_final = "." + configuration[reponse - 1]
                    return format_final
                else:
                    print(">>>ERREUR<<< Choix invalide.")
            except:
                print(">>>ERREUR<<< Choix invalide.")

    def affichage_fin(self):
        input("\n[-] fin, appuyer sur \'entrer\' pour continuer.")

    def reset_screen(self):
        if platform != "linux":
            system("cls")
        else:
            system("clear")
