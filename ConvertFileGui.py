import os
import subprocess
from functools import partial
import platform

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics.instructions import Canvas
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from Filter import Filter


class MyLabel(Label):
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            print("ciao")





class ConertFileGui(App):
    finsestra = None
    lista_file = []
    filtro = Filter()

    def build(self):
        Config.set('graphics', 'resizable', 0)
        Window.size = (800, 800)
        Window.bind(on_dropfile=self._on_file_drop)
        self.cornicie = GridLayout(cols = 1, spacing = 10 )
        self.finsestra = self.ad_finestra()
        self.cornicie.add_widget(self.finsestra)
        self.menu = BoxLayout(orientation = "horizontal")
        self.load_file = Button(text = "load file", size = (200,40), size_hint = (None, None) )
        self.load_file.bind(on_press = self.extract_order)
        self.html = Button(text = "HTML", size = (200,40), size_hint = (None, None) )
        self.pdf = Button(text="pdf", size=(200, 40), size_hint=(None, None))
        self.menu.add_widget(self.load_file)
        self.menu.add_widget(self.html)
        self.menu.add_widget(self.pdf)
        self.pdf.bind(on_press = self.open_pdf_directory)
        self.cornicie.add_widget(self.menu)
        return self.cornicie




    def ad_finestra(self):
        finsestra = GridLayout()
        finsestra.cols = 1
        finsestra.spacing = 10
        finsestra.size = (800,380)
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

    def _on_file_drop(self, window, file_path):
        name = file_path.decode("utf-8")
        if name.endswith(".csv"):
            if not name in self.lista_file:
                self.lista_file.append(name)
                self.ad_file_name(name, self.finsestra)
                print(f"tipo: {type(self.lista_file)} dato: {self.lista_file}")
            else:
                print("file gia caricato")
        else:
            print("tipo di file sbalgiato. solo .csv")


    def delete_riga(self,value, riga):
        self.lista_file.remove(riga.cartello.text)
        self.finsestra.remove_widget(riga)

    def extract_order(self,value):
        print("start")
        self.filtro.start_filter(file_list= self.lista_file)

    def open_pdf_directory (self):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"pdf")
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def open_pdf_directory (self):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"pdf")
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

if __name__ == "__main__":
    ConertFileGui().run()