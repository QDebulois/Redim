from PIL.Image import ANTIALIAS
from PIL.Image import new as image_new
from PIL.Image import open as image_open
from os import mkdir, listdir
from os.path import isfile, isdir, join


class Redim():
    def __init__(self, formats_acceptes):
        self.formats_acceptes = formats_acceptes

    def start(self, dossier, larg, haut, background_color, format_final):
        print("\n[-] travail pour", larg, "x", haut, "px :")
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
        return nouveau_nom.lower() + "_modif_" + str(larg) + format_final

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
