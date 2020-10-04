"""Contient la class principale de Redim,
travail sur les photos à l'aide de pillow
"""

from os import mkdir, listdir
from os.path import isfile, isdir, join
from PIL.Image import ANTIALIAS
from PIL.Image import new as image_new
from PIL.Image import open as image_open


class Redim():
    """Classe principale de Redim, travail sur les photos"""
    def __init__(self):
        self.__character_underscore = (" ", "-")
        self.__character_indesirable = (
            "(", ")", "[", "]", "{", "}", "'", "#", "¨",
            "&", "$", "£", "¤", "€", "`", "^", "°", "§",
            "@", "!", ",", "~", "%", ";", "µ"
        )
        self.__adverbes_multplicatifs = (
            "_bis", "_ter", "_quater", "_quinquies",
            "_sexies", "_septies"
        )

    def rennomage(self, origine_nom, larg, format_final):
        """Formatage du nom en retirant tous ces charactères hideux"""
        nouveau_nom = origine_nom
        for i in self.__character_indesirable:
            nouveau_nom = nouveau_nom.replace(i, "")
        for i in self.__character_underscore:
            nouveau_nom = nouveau_nom.replace(i, "_")
        return nouveau_nom.lower() + "_modif_" + str(larg) + format_final

    @staticmethod
    def listage(dossier, larg, formats_acceptes):
        """Listage des fichiers présent dans le dossier sélectionné,
        return de la liste + du dossier ou seront enregistré les photos
        """
        liste = []
        destination = join(dossier, str(larg))
        if not isdir(destination):
            mkdir(destination)
        for nom in listdir(dossier):
            if isfile(join(dossier, nom)):
                if join(dossier, nom).rsplit(".", 1)[-1] in formats_acceptes:
                    liste.append([join(dossier, nom), nom])
        return liste, destination

    @staticmethod
    def suppression_de_alpha(img, background):
        """Suppression de l'alpha (transparent) des photos"""
        img = img.convert("RGBA")
        if img.mode in ("RGBA", "LA"):
            fond = image_new(img.mode[:-1], img.size, tuple(background))
            fond.paste(img, img.split()[-1])
            img = fond
        img.convert("RGB")
        return img

    @staticmethod
    def redimensionnement(img, larg, haut):
        """Redimensionnement en agrandissant ou reduisant
        pour coller aux dimensions finales
        """
        if (img.size[0] >= larg) or (img.size[1] >= haut):
            img.thumbnail((larg, haut), ANTIALIAS)
        elif (img.size[0] / img.size[1]) <= (larg / haut):
            nouvelle_larg = int(haut * img.size[0] / img.size[1])
            img = img.resize((nouvelle_larg, haut), ANTIALIAS)
        else:
            nouvelle_haut = int(larg * img.size[1] / img.size[0])
            img = img.resize((larg, nouvelle_haut), ANTIALIAS)
        return img

    def main(self, dossier, configuration):
        """Fonction principale, execute toutes les method dans l'ordre
        pour sauvegarder la photos aux bonnes dimensions, au bon format,
        et sans alpha
        """
        for loop in range(len(configuration["dimensions"])):
            print(
                "\n[-] travail pour",
                str(configuration["dimensions"][loop][0]),
                "x",
                str(configuration["dimensions"][loop][1]),
                "px :"
            )
            if dossier != "":
                if isdir(dossier):
                    liste, destination = self.listage(
                        dossier,
                        str(configuration["dimensions"][loop][0]),
                        configuration["formats_acceptes"]
                    )
                else:
                    print("    >>>ERREUR<<< : Le dossier n'existe plus.")
            else:
                print("    >>>ERREUR<<< : Aucun dossier selectionne.")
            for nom in liste:
                print("    [+] Travail sur :", nom[1])
                img = image_open(nom[0])
                print(
                    "        >> Taille initiale :",
                    img.size[0],
                    "x",
                    img.size[1],
                    "px"
                )
                if nom[1].rsplit(".", 1)[-1] in ("png", "webp"):
                    img = self.suppression_de_alpha(
                        img,
                        configuration["background"]
                    )
                img = self.redimensionnement(
                    img,
                    configuration["dimensions"][loop][0],
                    configuration["dimensions"][loop][1],
                )
                print(
                    "        >> Taille apres redimensionnement :",
                    img.size[0],
                    "x",
                    img.size[1],
                    "px"
                )
                nouveau_nom = self.rennomage(
                    nom[1].rsplit(".", 1)[0],
                    configuration["dimensions"][loop][0],
                    configuration["format_final"]
                )
                fond = image_new(
                    "RGB",
                    (
                        configuration["dimensions"][loop][0],
                        configuration["dimensions"][loop][1]
                    ),
                    tuple(configuration["background"])
                )
                fond.paste(
                    img,
                    (
                        (configuration["dimensions"][loop][0]
                         - img.size[0]) // 2,
                        (configuration["dimensions"][loop][1]
                         - img.size[1]) // 2
                    )
                )
                if isfile(join(destination, nouveau_nom)):
                    nom_deja_present = nouveau_nom
                    iteration = 0
                    while isfile(join(destination, nom_deja_present)):
                        nom_deja_present = nouveau_nom.rsplit(".", 1)[0]\
                            + self.__adverbes_multplicatifs[iteration]\
                            + configuration["format_final"]
                        iteration += 1
                    fond.save(join(destination, nom_deja_present))
                else:
                    fond.save(join(destination, nouveau_nom))
