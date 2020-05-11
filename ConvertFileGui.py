import os
import subprocess
import time
from functools import partial
import platform

import kivy
kivy.require('1.9.0')
from kivy.app import App
from kivy.config import Config

from kivy.graphics.instructions import Canvas
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle



from OrderFilter.Filter import Filter
from multiprocessing import Process, freeze_support, active_children

from queue import Queue
from threading import Thread

if __name__ == '__main__':
	freeze_support()


class MyLabel(Label):
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            print("ciao")





class ConertFileGuiApp(App):
    finsestra = None
    lista_file = []
    filtro = Filter()
    Window_create = False
    def build(self):
        Config.set('graphics', 'resizable', True)
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'height', '800')
        if self.Window_create is False:
            from kivy.core.window import Window
            self.Window_create = True
        Window.bind(on_dropfile=self._on_file_drop)
        self.cornicie = GridLayout(cols = 1, spacing = 10 )

        self.finsestra = self.ad_finestra()
        self.cornicie.add_widget(self.finsestra)
        self.menu = BoxLayout(orientation = "horizontal")
        self.load_file = Button(text = "load file", size = (200,40), size_hint = (None, None) )

        self.html = Button(text = "HTML", size = (200,40), size_hint = (None, None) )
        self.pdf = Button(text="pdf", size=(200, 40), size_hint=(None, None))
        self.state_labe = Label(text = "READY", size=(200, 40), size_hint=(None, None))
        self.menu.add_widget(self.load_file)
        self.menu.add_widget(self.html)
        self.menu.add_widget(self.pdf)
        self.menu.add_widget(self.state_labe)
        self.pdf.bind(on_press = self.open_pdf_directory)
        self.html.bind(on_press= self.open_html_directory)
        self.cornicie.add_widget(self.menu)
        self.load_file.bind(on_press =partial(self.extract_order))
        self.output = Label( halign="left", valign="top",size=(400, 400), size_hint=(None, None))
        self.output.text_size = self.output.size
        self.finestra_out = self.ad_finestra()
        self.cornicie.add_widget(self.finestra_out)
        self.finestra_out.add_widget(self.output)
        return self.cornicie





    def ad_finestra(self):
        finsestra = GridLayout()
        finsestra.cols = 1
        finsestra.spacing = 10
        finsestra.size = (200,400)
        finsestra.size_hint = (None, None)
        finsestra.pos = 0, self.cornicie.height - 100
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
        _quee = Queue()
        print()
        print("start")
        self.filtro.file_list_global = self.lista_file
        #self.filtro.start_filter(_file_list= self.lista_file)
        #Process(target=self.filtro.start_filter).start()

        #t1 = Thread(target= self.on_workin)
        #t1.start()
        #t1.join()

        #t2 = Thread(target= self.filtro.start_filter)
        #t2.start()
        #t2.join()

        #t3 = Thread(target=self.on_ready)
        #t3.start()
        #t3.join()

        t0 = Thread(target=self.processo_parallo)
        t0.start()
        #t0.join()


        #t4 = Thread(target=self.read_log)
        #t4.start()
        #t4.join()
    def processo_parallo(self):
        self.on_workin()
        self.filtro.start_filter()
        self.on_ready()
        self.read_log()

    def on_workin(self):
        self.state_labe.text = "Working"
        self.load_file.disabled = True

    def on_ready(self):

        self.load_file.disabled = False
        self.state_labe.text = "Ready"

    def read_log(self):
        with open("log.txt", mode="r") as log:
            self.output.text = log.read()



    def open_pdf_directory (self, value):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"pdf")
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def open_html_directory (self,value):
        self.filtro.leggi_tabella_prodotti()

if __name__ == "__main__":

    ConertFileGuiApp().run()