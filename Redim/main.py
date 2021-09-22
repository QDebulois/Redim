import sys
from os.path import join
from config import Config
from core import Redim
from PyQt5 import QtWidgets, QtCore, QtGui


class Ajout_taille(QtWidgets.QDialog):
    """Fenêtre pour rajout d'une taille
    """
    def __init__(self, config):
        super(Ajout_taille, self).__init__()
        self.setWindowTitle("Ajout d'une dimension")
        logo = join("Ressources", "icon.ico")
        self.setWindowIcon(QtGui.QIcon(logo))
        self.config = config
        self.ajout = False
        texte_larg = QtWidgets.QLabel("Largeur:")
        self.edit_larg = QtWidgets.QLineEdit()
        texte_haut = QtWidgets.QLabel("Hauteur:")
        self.edit_haut = QtWidgets.QLineEdit()
        self.layout_btn = QtWidgets.QHBoxLayout()
        btn_ajouter = QtWidgets.QPushButton("Ajouter")
        btn_ajouter.clicked.connect(self.valider)
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_groupbox = QtWidgets.QVBoxLayout()
        self.layout_taille = QtWidgets.QHBoxLayout()
        self.groupbox_main = QtWidgets.QGroupBox("Ajout d'une dimension (en pixel)")
        self.groupbox_main.setLayout(self.layout_groupbox)
        self.layout_taille.addWidget(texte_larg)
        self.layout_taille.addWidget(self.edit_larg)
        self.layout_taille.addWidget(texte_haut)
        self.layout_taille.addWidget(self.edit_haut)
        self.layout_btn.addStretch()
        self.layout_btn.addWidget(btn_ajouter)
        self.layout_btn.addStretch()
        self.layout_groupbox.addLayout(self.layout_taille)
        self.layout_main.addWidget(self.groupbox_main)
        self.layout_main.addStretch()
        self.layout_main.addLayout(self.layout_btn)
        self.setLayout(self.layout_main)

    def valider(self):
        if self.edit_larg.text().isdigit() and self.edit_haut.text().isdigit():
            self.config["dimensions"].append(
                    [int(self.edit_larg.text()), int(self.edit_haut.text())]
                )
            self.ajout = True
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Entrée incorrecte")


class Gui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Gui, self).__init__()
        self.redim = Redim()
        self.config = Config()
        self.configuration = self.config.lecture()
        self.choix_dimensions = [[], []]
        logo = join("Ressources", "icon.ico")
        self.setWindowIcon(QtGui.QIcon(logo))
        menu = self.menuBar()
        menu_options = menu.addMenu("Options")
        btn_reset = QtWidgets.QAction("Reset des paramètres", self)
        btn_reset.triggered.connect(self.reset)
        btn_apropos = QtWidgets.QAction("A propos", self)
        btn_apropos.triggered.connect(self.a_propos)
        menu_options.addAction(btn_reset)
        menu_options.addAction(btn_apropos)
        self.setWindowTitle("Redim")
        self.home()

    def home(self):
        self.layout_main = QtWidgets.QVBoxLayout()
        # Layout Sélection dossier
        self.edit_source = QtWidgets.QLineEdit("Aucun dossier sélectionné.")
        self.edit_source.setReadOnly(True)
        btn_source = QtWidgets.QPushButton("Sélection dossier")
        btn_source.clicked.connect(self.selection_dossier)
        self.groupbox_source = QtWidgets.QGroupBox(
                "Sélection du dossier source"
                )
        self.layout_source = QtWidgets.QHBoxLayout()
        self.layout_source.addWidget(self.edit_source)
        self.layout_source.addWidget(btn_source)
        # Layout Configuration
        self.combobox_taille_1 = QtWidgets.QComboBox(self)
        self.combobox_taille_2 = QtWidgets.QComboBox(self)
        self.update_dimensions()
        self.combobox_taille_1.activated[str].connect(self.choix_combobox_1)
        self.combobox_taille_2.activated[str].connect(self.choix_combobox_2)
        btn_modif_taille = QtWidgets.QPushButton("Ajout taille")
        btn_modif_taille.clicked.connect(self.ajout_taille)
        self.edit_red = QtWidgets.QLineEdit()
        self.edit_green = QtWidgets.QLineEdit()
        self.edit_blue = QtWidgets.QLineEdit()
        if self.configuration["transparence"]:
            self.edit_red.setReadOnly(True)
            self.edit_green.setReadOnly(True)
            self.edit_blue.setReadOnly(True)
        else:
            self.edit_red.setText(str(self.configuration["background"][0]))
            self.edit_green.setText(str(self.configuration["background"][0]))
            self.edit_blue.setText(str(self.configuration["background"][0]))
        self.checkbox_transparency = QtWidgets.QCheckBox(
                "Conserver la transparence."
            )
        self.checkbox_transparency.stateChanged.connect(
                self.update_checkbox_transparency
            )
        if self.configuration["transparence"]:
            self.checkbox_transparency.setCheckState(QtCore.Qt.Checked)
        self.cb_format = QtWidgets.QComboBox(self)
        if self.configuration["transparence"]:
            self.cb_format.addItem(".webp")
            self.cb_format.addItem(".png")
        else:
            for i in self.configuration["formats_possibles"]:
                self.cb_format.addItem(".{0}".format(i))
        self.layout_config = QtWidgets.QHBoxLayout()
        self.groupbox_taille = QtWidgets.QGroupBox("Choix Dimensions")
        self.layout_taille = QtWidgets.QVBoxLayout()
        self.layout_taille.addStretch()
        self.layout_taille.addWidget(self.combobox_taille_1)
        self.layout_taille.addWidget(self.combobox_taille_2)
        self.layout_taille.addWidget(btn_modif_taille)
        self.groupbox_taille.setLayout(self.layout_taille)
        self.layout_config.addWidget(self.groupbox_taille)
        self.layout_config.addStretch()       
        self.groupbox_rgb = QtWidgets.QGroupBox("RGB")
        self.layout_rgb = QtWidgets.QVBoxLayout()
        self.layout_rgb.addStretch()
        self.layout_edit_rgb = QtWidgets.QHBoxLayout()
        self.layout_edit_rgb.addWidget(self.edit_red)
        self.layout_edit_rgb.addWidget(self.edit_green)
        self.layout_edit_rgb.addWidget(self.edit_blue)
        self.layout_rgb.addLayout(self.layout_edit_rgb)
        self.layout_rgb.addWidget(self.checkbox_transparency)
        self.layout_rgb.addStretch()
        self.groupbox_rgb.setLayout(self.layout_rgb)
        self.layout_config.addWidget(self.groupbox_rgb)
        self.layout_config.addStretch()
        self.groupbox_format = QtWidgets.QGroupBox("Choix format de sortie")
        self.layout_format = QtWidgets.QVBoxLayout()
        self.layout_format.addStretch()
        self.layout_format.addWidget(self.cb_format)
        self.layout_format.addStretch()
        self.groupbox_format.setLayout(self.layout_format)
        self.layout_config.addWidget(self.groupbox_format)
        self.layout_config.addStretch()
        # Layout Validation
        self.progressbar_validation = QtWidgets.QProgressBar()
        self.progressbar_validation.setMaximum(100)
        self.nom_fichier_en_cour = QtWidgets.QLabel("Travail sur:")
        btn_validation = QtWidgets.QPushButton("Convertir")
        btn_validation.clicked.connect(self.valider)
        self.groupbox_validation = QtWidgets.QGroupBox("Validation")
        self.layout_validation = QtWidgets.QHBoxLayout()
        self.layout_validation.addWidget(self.progressbar_validation)
        self.layout_validation.addWidget(self.nom_fichier_en_cour)
        self.layout_validation.addStretch()
        self.layout_validation.addWidget(btn_validation)
        # Layout Main
        self.mainWidget = QtWidgets.QWidget()
        self.layout_main.addStretch()
        self.groupbox_source.setLayout(self.layout_source)
        self.layout_main.addWidget(self.groupbox_source)
        self.layout_main.addStretch()
        self.layout_main.addLayout(self.layout_config)
        self.layout_main.addStretch()
        self.groupbox_validation.setLayout(self.layout_validation)
        self.layout_main.addWidget(self.groupbox_validation)
        self.layout_main.addStretch()
        self.mainWidget.setLayout(self.layout_main)
        self.setCentralWidget(self.mainWidget)
        self.show()

    def selection_dossier(self, choix):
        self.dossier = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le dossier sur lequel travailler."
        )
        if self.dossier != "":
            self.edit_source.setText(self.dossier)
        else:
            self.edit_source.setText("Aucun dossier sélectionné.")

    def choix_combobox_1(self, choix):
        self.choix_dimensions[0] = [int(i) for i in choix.split("x")]

    def choix_combobox_2(self, choix):
        self.choix_dimensions[1] = [int(i) for i in choix.split("x")]

    def ajout_taille(self):
        ajout_taille_gui = Ajout_taille(self.configuration)
        ajout_taille_gui.exec()
        if ajout_taille_gui.ajout:
            self.config.sauvegarde(ajout_taille_gui.config)
            self.configuration = self.config.lecture()
            self.update_dimensions()

    def update_dimensions(self):
        for i in range(self.combobox_taille_1.count()):
            self.combobox_taille_1.removeItem(0)
            self.combobox_taille_2.removeItem(0)
        for i in self.configuration["dimensions"]:
            self.combobox_taille_1.addItem("{0}x{1}".format(i[0], i[1]))
            self.combobox_taille_2.addItem("{0}x{1}".format(i[0], i[1]))
        self.combobox_taille_1.setCurrentIndex(self.combobox_taille_1.count() - 2)
        self.choix_dimensions[0] = [
                int(i) for i in self.combobox_taille_1.currentText().split("x")
            ]
        self.combobox_taille_2.setCurrentIndex(self.combobox_taille_1.count() - 1)
        self.choix_dimensions[1] = [
                int(i) for i in self.combobox_taille_2.currentText().split("x")
            ]

    def update_checkbox_transparency(self, value):
        if (QtCore.Qt.Checked == value):
            if not self.configuration["transparence"]:
                self.configuration["transparence"] = True
                self.config.sauvegarde(self.configuration)
                self.edit_red.setReadOnly(True)
                self.edit_red.setText("")
                self.edit_green.setReadOnly(True)
                self.edit_green.setText("")
                self.edit_blue.setReadOnly(True)
                self.edit_blue.setText("")
                for i in range(self.cb_format.count()):
                    self.cb_format.removeItem(0)
                self.cb_format.addItem(".webp")
                self.cb_format.addItem(".png")
        else:
            self.configuration["transparence"] = False
            self.config.sauvegarde(self.configuration)
            self.edit_red.setReadOnly(False)
            self.edit_red.setText(str(self.configuration["background"][0]))
            self.edit_green.setReadOnly(False)
            self.edit_green.setText(str(self.configuration["background"][1]))
            self.edit_blue.setReadOnly(False)
            self.edit_blue.setText(str(self.configuration["background"][2]))
            for i in range(self.cb_format.count()):
                self.cb_format.removeItem(0)
            for i in self.configuration["formats_possibles"]:
                self.cb_format.addItem(".{0}".format(i))

    def update_progress_bar(self, value):
        self.progressbar_validation.setValue(value)

    def update_nom_travail_fichier(self, value):
        self.nom_fichier_en_cour.setText("Travail sur: %s" % value)

    def valider(self):
        self.configuration["format_choisi"] = self.cb_format.currentText()
        print(self.configuration)
        if not self.configuration["transparence"]:
            rgb_background = []
            rgb_background.append(self.edit_red.text())
            rgb_background.append(self.edit_green.text())
            rgb_background.append(self.edit_blue.text())
            for i, j in enumerate(rgb_background):
                if j.isdigit():
                    rgb_background[i] = int(j)
                else:
                    QtWidgets.QMessageBox.warning(
                            self,
                            "Erreur",
                            "Entrée RGB incorrecte"
                            )
                    return
            if rgb_background != self.configuration["background"]:
                self.configuration["background"] = rgb_background
                self.config.sauvegarde(self.configuration)
        if hasattr(self, "dossier"):
            configFinal = self.configuration
            self.configuration["dimensions"] = self.choix_dimensions
            self.redim._progress_bar_value.connect(self.update_progress_bar)
            self.redim._travail_sur_value.connect(
                    self.update_nom_travail_fichier
                    )
            returncode_redim = self.redim.main(self.dossier, configFinal)
            if returncode_redim == 0:
                QtWidgets.QMessageBox.information(
                        self,
                        "Redim",
                        "redimensionnement terminé!"
                        )
            elif returncode_redim == 1:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Erreur",
                    "Plus de 10 fichiers ont le même nom dans le répertoire final.\
                    <br>Veuillez renommer vos fichiers originaux ou renommer les précédentes conversions."
                    )
        else:
            QtWidgets.QMessageBox.warning(
                    self,
                    "Erreur",
                    "Veuillez sélectionner un dossier"
                    )

    def reset(self):
        self.config.reset()
        self.configuration = self.config.lecture()
        self.choix_dimensions = [[], []]
        self.update_dimensions()
        self.checkbox_transparency.setCheckState(0)
        self.update_checkbox_transparency(0)
        QtWidgets.QMessageBox.information(
                self,
                "Reset des paramètres",
                "Les paramètres ont été réinitialisés."
                )

    def a_propos(self):
        QtWidgets.QMessageBox.information(
            self,
            "A propos",
            "Logiciel de redimensionnement d'image.\
            <br>Version: %s\
            <br>Auteur: Debulois Quentin\
            <br>Copyright: \
            <a href='https://www.gnu.org/licenses/gpl-3.0.txt'>GNU GPLv3</a>\
            <br>Code source: \
            <a href='https://git.debulois.fr/redim/'>git.debulois.fr/redim</a>" % self.configuration["version"]
            )


if __name__ == "__main__":
    def main():
        """Démarrage de l'app
        """
        app = QtWidgets.QApplication(sys.argv)
        GUI = Gui()
        sys.exit(app.exec_())

    main()
