from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button

from kivy.uix.textinput import TextInput

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader


class Joueur:
    count: int = 0

    def __init__(self):
        self.count += 1
        self.nom = ""
        self.id = self.count  # numero de joueur
        self.ip = ""
        self.score = []
        self.equipe = -1
        self.affiche = False
        self.labelTitre = None
        self.labeLlIp = None
        self.tab = None
