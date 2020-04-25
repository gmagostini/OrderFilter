import os
from functools import partial

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput



class MyLabel(Label):
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            print("ciao")





class ConertFileGui(App):
    finsestra = None
    lista_file = []
    def build(self):
        Config.set('graphics', 'resizable', 0)
        Window.size = (800, 800)
        Window.bind(on_dropfile=self._on_file_drop)
        self.finsestra = self.ad_finestra()
        cornicie = BoxLayout
        cornicie.orientation = "vertical"
        #cornicie.add_widget(self.finsestra)
        process_file = Button()
        process_file.text = "processa ordini"
        cornicie.size = (200,40)
        cornicie.size_hint = (None, None)
        cornicie.add_widget(process_file)
       # chooser =  FileChooserListView()
        return process_file


    def _on_file_drop(self, window, file_path):
        self.lista_file.append(file_path.decode("utf-8"))
        name = file_path.decode("utf-8")
        self.ad_file_name(name, self.finsestra)
        print(f"tipo: {type(self.lista_file)} dato: {self.lista_file}")


    def ad_finestra(self):
        finsestra = GridLayout()
        finsestra.cols = 1
        finsestra.spacing = 20
        finsestra.size = (500,500)
        finsestra.size_hint = (None, None)
        return finsestra

    def ad_file_name(self, name, finestra):
        riga = BoxLayout()
        riga.orientation = "horizontal"
        riga.size = (800, 40)
        riga.size_hint = (None, None)
        riga.cartello = MyLabel()
        riga.cartello.text = name
        riga.cartello.size = (600, 40)
        riga.cartello.halign = 'right'
        riga.cartello.size_hint = (None, None)
        riga.add_widget(riga.cartello)
        riga.change = Button()
        riga.change.text = "cambia"
        riga.change.size = (100, 40)
        riga.change.size_hint = (None, None)
        riga.add_widget(riga.change)
        riga.delette = Button()
        riga.delette.text = "cancella"
        riga.delette.size = (100, 40)
        riga.delette.size_hint = (None, None)
        riga.delette.bind(on_press= partial(self.delete_riga, riga = riga))
        riga.add_widget(riga.delette)
        finestra.add_widget(riga)

    def delete_riga(self,value, riga):
        self.lista_file.remove(riga.cartello.text)
        self.finsestra.remove_widget(riga)

if __name__ == "__main__":
    ConertFileGui().run()