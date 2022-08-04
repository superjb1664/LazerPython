from time import sleep
from typing import List, Any

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button

from kivy.uix.textinput import TextInput

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader

import socket
import asyncio
from threading import Thread
from enum import Enum
import utils
import joueur
from requeteClient import RequeteClient
from requeteClient import TypeRequete

class EtatServeur(Enum):
    stop = 1
    enAttente = 2
    partieEnCours = 3
    partieTerminee = 4


class InterfaceServeur(App):
    list_joueur: list[joueur.Joueur]

    def donneTexteServeur(self):
        if self.etat == EtatServeur.enAttente:
            return "En attente"
        elif self.etat == EtatServeur.stop:
            return "Arrêtée"
        elif self.etat == EtatServeur.partieEnCours:
            return "Partie en cours"
        else:
            return "Partie terminée"

    def build(self):
        # returns a window object with all it's widgets
        self.port = 5000
        self.etat = EtatServeur.stop
        self.mySocket = socket.socket()
        self.ip = socket.gethostbyname(socket.gethostname())
        self.tab_pannel = TabbedPanel()
        self.tab_pannel.default_tab_text = 'Accueil'
        self.tab_pannel.default_tab_content = GridLayout()
        self.tab_pannel.default_tab_content.cols = 1
        #  self.tp.default_tab_content.size_hint = (0.6, 0.7)
        self.tab_pannel.default_tab_content.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.accueil_title = Label(
            text="Accueil",
            font_size=36,
            color='#AAFFFF',
            bold=True,
        )
        self.tab_pannel.default_tab_content.add_widget(self.accueil_title)

        self.accueil_etat = Label(
            text="Etat : " + self.donneTexteServeur(),
            font_size=18,
            color='#00FFCE'
        )
        self.accueil_etat.size_hint = (1, 0.5)
        self.tab_pannel.default_tab_content.add_widget(self.accueil_etat)

        self.accueil_ip = Label(
            text="IP : " + self.ip,
            font_size=18,
            color='#00FFCE'
        )

        self.tab_pannel.default_tab_content.add_widget(self.accueil_ip)

        self.accueil_port_layout = GridLayout()
        self.accueil_port_layout.rows = 1
        self.accueil_port_layout.size_hint = (1, 0.5)
        self.accueil_port_layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.tab_pannel.default_tab_content.add_widget(self.accueil_port_layout)

        self.accueil_port_label = Label(
            text="Port : (entre 0 et 65535) ",
            font_size=18,
            color='#00FFCE'
        )
        self.accueil_port_layout.add_widget(self.accueil_port_label)

        self.accueil_port_input = TextInput(
            multiline=False,
            padding_y=(20, 20),
            size_hint=(1, 0.5),
            text=str(self.port)
        )
        self.accueil_port_input.input_filter = 'int'
        self.accueil_port_layout.add_widget(self.accueil_port_input)

        self.accueil_button_start = Button(
            text="START",
            size_hint=(0.5, 0.5),
            bold=True,
            background_color='#00FFCE',
        )
        self.accueil_button_start.bind(on_press=self.callback_accueil_port_input)
        self.tab_pannel.default_tab_content.add_widget(self.accueil_button_start)

        self.tab_attente = TabbedPanelHeader(text='Salle d\'attente')
        self.tab_pannel.add_widget(self.tab_attente)
        self.tab_attente.content = GridLayout()
        self.tab_attente.content.cols = 1
        self.tab_attente.content.size_hint = (1, 1)
        self.tab_attente.content.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.tab_attente.content.clear_widgets()
        self.tab_attente_title = Label(
            text="Joueur en salle d'attente",
            font_size=18,
            color='#00FFCE'
        )

        self.list_joueur = []
        self.tab_attente.content.add_widget(self.tab_attente_title)
        return self.tab_pannel

    def worker_serveur(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("" + self.ip)
        print("" + self.port)
        self.s.bind((str(self.ip), int(self.port)))
        while self.etat == EtatServeur.enAttente:
            self.s.listen()
            conn, addr = self.s.accept()
            with conn:
                print(f"Connected by {addr}")
                while self.etat == EtatServeur.enAttente:
                    data = conn.recv(1024)
                    if not data:
                        break
                    requete = RequeteClient(data)
                    if requete.type == TypeRequete.ajoutDeJoueur:
                        nvJoueur = joueur.Joueur()
                        nvJoueur.ip = addr
                        self.ajouter_salle_dattente(nvJoueur)

                        conn.send()
                conn.close()

        self.s.close()
        print("serveur arrêté")


    def ajouter_salle_dattente(self, joueurToAdd):

        self.list_joueur.append(joueurToAdd)
        self.regenerer_salle_dattente()

    def regenerer_salle_dattente(self):

        nbAdd = 0
        # On efface l'affichage précédent
        for joueur_instance in self.list_joueur:
            if not joueur_instance.affiche:
                joueur_instance.tab = GridLayout()
                joueur_instance.tab.rows = 1
                joueur_instance.tab.size_hint = (1, 1)
                joueur_instance.tab.pos_hint = {"center_x": 0.5, "center_y": 0.5}
                self.tab_attente.content.add_widget(joueur_instance.tab)
                joueur_instance.labelTitre = Label(
                    text='' + joueur_instance.id +
                         '\n' + joueur_instance.nom +
                         '\n' + joueur_instance.ip +
                         '\n' + joueur_instance.equipe,
                    font_size=18,
                    color='#00FFCE'
                )
                joueur_instance.tab.add_widget(joueur_instance.labelTitre)
                joueur_instance.affiche = True
                nbAdd += 1
            else:
                joueur_instance.labelTitre.text = '' + joueur_instance.id + '\n' + joueur_instance.nom + '\n' + joueur_instance.ip + '\n' + joueur_instance.equipe

        return nbAdd

    def callback_accueil_port_input(self, instance):
        if self.etat == EtatServeur.stop :
            if utils.check_int(self.accueil_port_input.text):
                # change label text to "Hello + user name!"
                self.accueil_etat.text = "lancé"
                self.etat = EtatServeur.enAttente
                self.port = self.accueil_port_input.text
                self.accueil_button_start.text = "Arrêter"
                Thread(target=self.worker_serveur).start()
            else:
                utils.create_modal('"Port" : entre 0 et 65535')
        else  : #TODO reflechir à un garde fou en cas de salle d'attente occupée !
            self.accueil_etat.text = "Arrêté"
            self.accueil_button_start.text = "Démarrer"
            self.etat = EtatServeur.stop
            socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM).connect((str(self.ip), int(self.port)))



# run Say Hello App Calss
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        InterfaceServeur().async_run()
    )
    loop.close()
