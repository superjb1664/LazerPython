from enum import Enum

class TypeReponse(Enum):
    erreur = 0 #ERR
    OK = 1 #OK

class ReponseServeur:
    def __init__(self, type: TypeReponse, numeroRequete: str):
        self.type = type
        self.num = numeroRequete


    def donneByte(self):
        reponse = ""
        if self.type == TypeReponse.erreur:
            reponse = "ERR " + str(self.num)
        elif self.type == TypeReponse.OK:
            reponse = "OK " + str(self.num)
        return  bytes(reponse,"ascii")