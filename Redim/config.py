import json

class config():
    def sauvegarde(json_path, largeur1, hauteur1, largeur2, hauteur2, background_color, format_final):
        dictionnaire = {
                "dimensions" : [[largeur1, hauteur1], [largeur2,hauteur2]],
                "background_color" : background_color,
                "format_final" : format_final
                }
        if not isdir(json_path):
            mkdir(json_path)
        with open(join(json_path, "config_redim"), "w") as f:
            json.dump(dictionnaire, f)

    def lecture(json_path):
        with open(join(json_path, "config_redim"), "r") as f:
                dictionnaire = json.load(f)
        largeur1 = dictionnaire["dimensions"][0][0]
        hauteur1 = dictionnaire["dimensions"][0][1]
        largeur2 = dictionnaire["dimensions"][1][0]
        hauteur2 = dictionnaire["dimensions"][1][1]
        background_color = dictionnaire["background_color"]
        format_final = dictionnaire["format_final"]
        return largeur1, hauteur1, largeur2, hauteur2, background_color, format_final

