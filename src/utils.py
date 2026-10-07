# utils.py — fonctions partagées entre notebooks

# Regroupement des divisions NAF (2 premiers caractères du code APE)
LIBELLES_NAF = {
    "01": "Agriculture", "02": "Sylviculture", "03": "Pêche",
    "05": "Extraction", "06": "Pétrole/gaz", "07": "Minerais",
    "08": "Autres extractions", "09": "Services extraction",
    "10": "Alimentation", "11": "Boissons", "12": "Tabac",
    "13": "Textile", "14": "Habillement", "15": "Cuir",
    "16": "Bois", "17": "Papier", "18": "Imprimerie",
    "19": "Raffinage", "20": "Chimie", "21": "Pharmacie",
    "22": "Plastique", "23": "Minéraux", "24": "Métallurgie",
    "25": "Fabrication métallique", "26": "Électronique",
    "27": "Équipements électriques", "28": "Machines",
    "29": "Automobile", "30": "Autres transports",
    "31": "Meubles", "32": "Autres industries",
    "33": "Réparation machines", "35": "Énergie",
    "36": "Eau", "37": "Assainissement", "38": "Déchets",
    "39": "Dépollution", "41": "Construction bâtiments",
    "42": "Génie civil", "43": "Travaux spécialisés",
    "45": "Commerce auto", "46": "Commerce gros",
    "47": "Commerce détail", "49": "Transport terrestre",
    "50": "Transport eau", "51": "Transport aérien",
    "52": "Entreposage", "53": "Livraison",
    "55": "Hôtellerie", "56": "Restauration",
    "58": "Édition", "59": "Cinéma/audio",
    "60": "Audiovisuel", "61": "Télécoms",
    "62": "Informatique", "63": "Services info",
    "64": "Finance", "65": "Assurance",
    "66": "Services financiers", "68": "Immobilier",
    "69": "Juridique/comptable", "70": "Direction entreprises",
    "71": "Ingénierie", "72": "Recherche",
    "73": "Publicité", "74": "Autres spécialisés",
    "75": "Vétérinaire", "77": "Location",
    "78": "Emploi", "79": "Tourisme",
    "80": "Sécurité", "81": "Services bâtiments",
    "82": "Services admin", "84": "Administration publique",
    "85": "Enseignement", "86": "Santé",
    "87": "Hébergement médico-social", "88": "Action sociale",
    "90": "Arts", "91": "Bibliothèques/musées",
    "92": "Jeux de hasard", "93": "Sports/loisirs",
    "94": "Organisations associatives", "95": "Réparation biens",
    "96": "Services personnels", "97": "Ménages employeurs",
    "98": "Ménages producteurs", "99": "Organismes internationaux",
}


def categoriser_juridique(code):
    """Regroupe les codes de catégorie juridique INSEE en grandes familles."""
    if code == 1000:
        return "Entrepreneur individuel"
    elif code in [5499, 5498]:
        return "SARL"
    elif code in [5710, 5720]:
        return "SAS"
    elif code in [5200, 5215, 5308]:
        return "SA"
    elif code in [9220, 9221, 9222, 9223, 9224, 9225, 9230, 9240, 9260]:
        return "Association"
    elif 6000 <= code <= 6999:
        return "Société civile"
    elif code in [9110, 9150, 9160]:
        return "Syndicat/GIE"
    else:
        return "Autre"
