from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


kv = '''
<ColoredLabel>:
    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            pos: self.pos
            size: self.size
        '''

Builder.load_string(kv)


class ColoredLabel(Label):
    background_color = ListProperty((0, 0, 0, 1))


def check_int(str):
    if len(str) == 0:
        return False
    if str[0] in ('-', '+'):
        return str[1:].isdigit()
    return str.isdigit()


def create_modal(text_modal, titre='Attention'):
    view = ModalView(size_hint=(None, None), size=(400, 400))
    gd = GridLayout()
    gd.cols = 1
    gd.add_widget(ColoredLabel(text=titre,
                               size_hint=(0.5, 0.25),
                               background_color=(255, 255, 255, 1),
                               color=(1,0,0,1),
                               bold=True,
                               font_size=36,))
    gd.add_widget(Label(text=text_modal))
    btn = Button(
        text="OK",
        size_hint=(0.5, 0.25),
        bold=True,
    )
    btn.bind(on_press=view.dismiss)
    gd.add_widget(btn)
    view.add_widget(gd)
    view.open()




