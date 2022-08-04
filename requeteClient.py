from enum import Enum
import utils
import joueur


class TypeRequete(Enum):
    erreur = 0
    ajoutDeJoueur = 1 #A
    retraitDeJoueur = 2 #R
    accuseChangements = 3 #C
    joueurTuePar = 4 #T


class RequeteClient:
    def __init__(self, data: str):
        tabData = data.split(' ')
        self.type = TypeRequete.erreur
        if tabData[0] == 'A':
            self.type = TypeRequete.ajoutDeJoueur
            self.idRequeteClient = tabData[1]
        elif tabData[0] == 'R':
            self.type = TypeRequete.retraitDeJoueur
            self.idRequeteClient = tabData[1]
        elif tabData[0] == 'C':
            self.type = TypeRequete.accuseChangements
            self.idRequeteClient = tabData[1]
        elif tabData[0] == 'T':
            self.type = TypeRequete.joueurTuePar
            self.idRequeteClient = tabData[1]



