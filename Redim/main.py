from sys import exit
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication
from ui import Ui
from core import Redim
from config import Config


def main():
    app = QApplication([])
    widget = QWidget()
    config = Config()
    redim = Redim()
    while True:
        configuration = config.lecture()
        ui = Ui(configuration)
        ui.reset_screen()
        ui.affichage_banner()
        ui.affichage_menu()
        choix = input(
            "[>] Choix (numero) : "
        )
        while True:
            ui.reset_screen()
            ui.affichage_banner()
            if choix.strip() == "1":
                dossier = QFileDialog.getExistingDirectory(
                    widget,
                    "Sélectionner le dossier sur lequel travailler."
                )
                redim.start(dossier, configuration)
                ui.affichage_fin()
                break
            elif choix.strip() == "5":
                ui.reset_screen()
                ui.affichage_banner()
                configuration["dimensions"] = ui.question_taille(
                    configuration["dimensions"]
                )
                config.sauvegarde(configuration)
                ui.affichage_fin()
                break
            elif choix.strip() == "6":
                ui.reset_screen()
                ui.affichage_banner()
                configuration["background"] = ui.question_background(
                    configuration["background"]
                )
                config.sauvegarde(configuration)
                ui.affichage_fin()
                break
            elif choix.strip() == "7":
                ui.reset_screen()
                ui.affichage_banner()
                configuration["format_final"] = ui.question_format_final(
                    configuration["formats_acceptes"]
                )
                config.sauvegarde(configuration)
                ui.affichage_fin()
                break
            elif choix.strip() == "8":
                ui.reset_screen()
                ui.affichage_banner()
                print("\n[-] Reset des parametres.")
                config.sauvegarde(config._base_configuration)
                ui.affichage_fin()
                break
            elif choix.strip() == "9":
                ui.reset_screen()
                exit(0)
            else:
                ui.reset_screen()
                ui.affichage_banner()
                print("\n[-] Reponse invalide .")
                ui.affichage_fin()
                break


if __name__ == "__main__":
    main()
