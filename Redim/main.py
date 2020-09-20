"""Fichier principal de Redim"""

import sys
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication
from ui import Ui
from core import Redim
from config import Config


def main():
    """Function principale de Redim, instanciation des classes
    et exécution des choix de l'utilisateur dans le menu principal
    """
    app = QApplication([])
    widget = QWidget()
    config = Config()
    redim = Redim()
    while True:
        configuration = config.lecture()
        tui = Ui(configuration)
        tui.affichage_banner()
        tui.affichage_menu()
        choix = input(
            "[>] Choix (numero) : "
        )
        while True:
            tui.affichage_banner()
            if choix.strip() == "1":
                dossier = QFileDialog.getExistingDirectory(
                    widget,
                    "Sélectionner le dossier sur lequel travailler."
                )
                redim.main(dossier, configuration)
                tui.affichage_fin()
                break
            if choix.strip() == "5":
                tui.affichage_banner()
                configuration["dimensions"] = tui.question_taille(
                    configuration["dimensions"]
                )
                config.sauvegarde(configuration)
                tui.affichage_fin()
                break
            if choix.strip() == "6":
                tui.affichage_banner()
                configuration["background"] = tui.question_background(
                    configuration["background"]
                )
                config.sauvegarde(configuration)
                tui.affichage_fin()
                break
            if choix.strip() == "7":
                tui.affichage_banner()
                configuration["format_final"] = tui.question_format_final(
                    configuration["formats_acceptes"]
                )
                config.sauvegarde(configuration)
                tui.affichage_fin()
                break
            if choix.strip() == "8":
                tui.affichage_banner()
                print("\n[-] Reset des parametres.")
                config.sauvegarde(config.base_configuration)
                tui.affichage_fin()
                break
            if choix.strip() == "9":
                tui.reset_screen()
                sys.exit(0)
            else:
                tui.affichage_banner()
                print("\n[-] Reponse invalide .")
                tui.affichage_fin()
                break


if __name__ == "__main__":
    main()
