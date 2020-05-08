import os

import pandas as pd

import pdfkit
import json

import logging

logging.basicConfig(filename='log.txt', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')

from queue import Queue
#from ConvertFileGui import ConertFileGui
from kivy.app import App
class Filter():
    file_list_global = []
    working = False
    output_check = ""
    def read_cvs_diveideOrder(self,primitive_data, home):
        column_name = {} #nome delle collonne in dizionario
        header = [] #elementi del headre
        items = [] #elemendi dei singoli pezzi


        #legge i nomi delle colonne dal file config e assegan le liste del heade e dgli items
        with open(os.path.join(home, "config.json"), 'r') as read_file:
            column_name = json.load(read_file)
            header = column_name["header"]
            items = column_name["items"]
            image_size = column_name["image_size"]


        header_ref = []
        item_ref = []

        #seleziona solo le colonne presenti nella tabella
        for col in header :
            if col in primitive_data:
                header_ref.append(col)

        for col in items:
            if col in primitive_data:
                item_ref.append(col)
            else:
                print(f"ho escluso {col}")

        tabella_prodotti = pd.read_csv(os.path.join(home, "Product", "Tabella.csv"))


        all_column = header_ref + item_ref
                        #print(list(primitive_data))
        refind_data = primitive_data[all_column]
        all_column_material = all_column
        #aggiunge colonna materiale

        """refind_data_materie = pd.DataFrame(columns=all_column)
        refind_data_materie = refind_data[refind_data["Item's Name"].isin(tabella_prodotti["Modello"]) ]"""

        refind_data["Material"] = None
        refind_data["Reparto"] = None
        refind_data["N# sostegni"] = 0
        for index, row in refind_data.iterrows():

            if row["Item's Name"] in tabella_prodotti["Modello"].to_list():
                refind_data.loc[index,"Material"] = tabella_prodotti[tabella_prodotti["Modello"] == row["Item's Name"]]["Materiale schrmo"].iloc[0]
                refind_data.loc[index, "Reparto"] = tabella_prodotti[tabella_prodotti["Modello"] == row["Item's Name"]]["Reparto"].iloc[0]
                refind_data.loc[index, "N# sostegni"] = tabella_prodotti[tabella_prodotti["Modello"] == row["Item's Name"]]["N# sostegni"].iloc[0]
                refind_data.loc[index, "Stacco da terrra"] = tabella_prodotti[tabella_prodotti["Modello"] == row["Item's Name"]]["Stacco da terrra"].iloc[0]
        print(refind_data["Stacco da terrra"])

        #estrae gli indicici sulla base del numero del ordine
        ordini = refind_data["Order #"].to_list()

        # e li ordina
        ordini.sort()


        #toglie i duplucati
        ordini_indice = []
        for i in ordini:
            if i not in ordini_indice:
                ordini_indice.append(i)

        # estrae e ragruppa i singoli ordini dai dati ragginati
        elenco_ordini_ragruppati = []
        for i in ordini_indice:
            elenco_ordini_ragruppati.append(refind_data[refind_data["Order #"] == i])


        #print(f"elsenco degli ordini raffinati: \n{elenco_ordini_ragruppati}")

        return elenco_ordini_ragruppati, header_ref, item_ref ,image_size




    def scrivi_dizinario(self,elenco_ordini_ragruppati, header, items):
        ordine1 = elenco_ordini_ragruppati
        ordine_dizionario = {}
        for name in header:
            ordine_dizionario[name] = ordine1[name].iat[0]

        ordine_dizionario["Items"] = ordine1[items]
        return ordine_dizionario


    def scrivi_file_html(self,ordine_dizionario = None, home = None, header = [], items = [], image_size =[80,80] ):

        file_html = os.path.join(home,"html"
                                 , f"order{ordine_dizionario['Order #']}.html")
        file_pdf = os.path.join(home,"Pdf"
                                 , f"order{ordine_dizionario['Order #']}.pdf")



        with open(file_html, mode='w') as file_out:

            file_out.write(f"<table border=1>")
    #STAMPA HEADER
            for name in header:
                file_out.write(f"""
                <tr>
                    <th> {name} </th>
                    <th> {ordine_dizionario[name]} </th>
                </tr>
                """)


    #STAMPA GLI ITEMS
            file_out.write(f"<tr>")
            for name in items:
                if name != "Notes to Seller" and name != "Item's Variant":
                    file_out.write(f"""
                                    <th> {name} </th>
                                """)
                elif name == "Item's Variant":
                    file_out.write(f"""
                                    <th> Item's Variant </th>
                                    """)

                    file_out.write(f"""
                                    <th> Image </th>
                                    """)

            file_out.write(f"</tr>")
            items_name_list = []

            for index, row in ordine_dizionario["Items"].iterrows():
                file_out.write(f"<tr>")
                for name in items:
                    if name != "Notes to Seller" and name != "Item's Variant":
                        file_out.write(f"""
                                    <th style="text-align:left" > {row[name]} </th>
                                    """)
                    elif name == "Item's Variant":
                        temp = row["Item's Variant"].replace("|", "<br>")
                        file_out.write(f"""
                                        <th style="text-align:left" ><h2>  {temp} </h2></th>
                                        """)

                        self.load_image(row,file_out,home,image_size)



                file_out.write(f"</tr>")
                if str(row["Notes to Seller"]) != 'nan':
                    file_out.write(f"<tr>")
                    file_out.write(f"""
                                    <th>Notes to Seller</th>
                                    <th> {row["Notes to Seller"]} </th>
                                    """)
                    file_out.write(f"</tr>")




            file_out.write("</table>")


        #print(ordine_dizionario['Order #'])
        pdfkit.from_file(file_html, file_pdf)


        with open("log.txt", mode='a') as log:
            log.write(f"Ordine n:{ordine_dizionario['Order #']}\n")


    def scrive_wood_and_stone(self, home, ordine:pd.DataFrame, image_size =[80,80]):

        schermo_plexiglass = []
        wood = 0
        stone = 0
        item_wood = {}
        item_stone = {}

        print("SCRIVI WOOD AND STONE")
        for index,row in ordine.iterrows():
            #se lo schemro è in pèelxiplax estrapola le dimensioni
            print(row["Material"] == "Plexiglass")
            if row["Material"] == "Plexiglass":
                lista = row["Item's Variant"].split("|")
                valori_dizionario = {}
                for i in lista:
                    temp = i.split(":")
                    valori_dizionario[temp[0]] = temp[1]

                valori_dizionario["item"] = row["Item's Name"]
                valori_dizionario[" Altezza"] = [int(s) for s in valori_dizionario[" Altezza"].split() if s.isdigit()][0] - 5
                valori_dizionario[" Larghezza"] = [int(s) for s in valori_dizionario[" Larghezza"].split() if s.isdigit()][0]
                schermo_plexiglass.append(valori_dizionario)

            #se i blocchi sono in legno
            if row["Reparto"] =="W":
                wood += int(row["N# sostegni"])
                if row["Item's Name"] in item_wood:
                    item_wood[row["Item's Name"]][0] += 1
                else:
                    item_wood[row["Item's Name"]] = [1, row["N# sostegni"]]

            #se i blocchi sono in pietra:
            if row["Reparto"] =="S":
                stone += int(row["N# sostegni"])
                if row["Item's Name"] in item_stone:
                    item_stone[row["Item's Name"]][0] += 1
                else:
                    item_stone[row["Item's Name"]] = [1, row["N# sostegni"]]
        print(f"ordein: \n {ordine}")
        #SRIVI FILE WOOD AND STONE
        file_html_wood = os.path.join(home, "html"
                                      , f"order{ordine['Order #'].iloc[0]}-wood.html")
        file_pdf_wood = os.path.join(home, "Pdf"
                                     , f"order{ordine['Order #'].iloc[0]}-wood.pdf")

        file_html_stone = os.path.join(home, "html"
                                       , f"order{ordine['Order #'].iloc[0]}-stone.html")
        file_pdf_stone = os.path.join(home, "Pdf"
                                      , f"order{ordine['Order #'].iloc[0]}-stone.pdf")

        if wood > 0:
            with open(file_html_wood, mode='w') as file_out:

                file_out.write(f"<table border=1>")

                file_out.write(f"""
                    <tr>
                        <th> BLOCCHE DI LEGNO TOTALIA </th>
                        <th> {wood} </th>
                    </tr>
                    """)
                #nomi degli item e quantita
                file_out.write(f"""
                                    <tr>
                                        <th> Numero pezi </th>
                                        <th> prodotto </th>
                                        <th> Numero sostegni per pr. singolo </th>
                                        <th> Numero sostegni totali </th>
                                    </tr>
                                    """)
                for key in item_wood:
                    file_out.write(f"""
                    <tr>
                        <th> {item_wood[key][0]} </th>
                        <th> {key} </th>
                        <th> {item_wood[key][1]} </th> 
                        <th> {int(item_wood[key][1]) * int(item_wood[key][0])} </th>
                    </tr>
                    """)
                file_out.write("<tr></tr>")
                file_out.write("<tr></tr>")

                if schermo_plexiglass:
                    print(schermo_plexiglass)
                    for elemento in schermo_plexiglass:
                        file_out.write(f"""
                                            <tr>
                                                <th> {elemento["item"]} </th>
                                                <th>Altezza {elemento[' Altezza']} cm </th>
                                                <th>Larghezza {elemento[' Larghezza']} cm </th>
                                            </tr> """)

                    #self.load_image(row,file_out,image_size)
                file_out.write("</table")
            pdfkit.from_file(file_html_wood, file_pdf_wood)

        if stone > 0:
            with open(file_html_stone, mode='w') as file_out:

                file_out.write(f"<table border=1>")

                file_out.write(f"""
                    <tr>
                        <th> BLOCCHE DI pietra  TOTALI  </th>
                        <th> {stone} </th>
                    </tr>
                    """)
                # nomi degli item e quantita
                file_out.write(f"""
                                                    <tr>
                                                        <th> Numero pezi </th>
                                                        <th> prodotto </th>
                                                        <th> Numero prodotti </th>
                                                    </tr>
                                                    """)
                for key in item_stone:
                    file_out.write(f"""
                    <tr>
                        <th> {key} </th>
                        <th> {item_stone[key][0]} </th>
                        <th> {item_stone[key][1]}
                    </tr>
                    """)
                i=1


                   #self.load_image(row, file_out, image_size)
                file_out.write("</table")
            pdfkit.from_file(file_html_stone, file_pdf_stone)


    def load_image(self, row,file_out,home, image_size=[80,80]):

        name_items = row["Item's Name"]
        name_items = name_items.replace('/', '')
        logging.info(f'{os.listdir(os.path.join(home, "Product", "Image"))}')
        for name_picture in os.listdir(os.path.join(home, "Product", "Image")):
            if name_items in name_picture:
                name_picture = os.path.join(home, "Product", "Image", name_picture)
                print(f"inserisoc immagine {os.path.join(home,'Product', 'Image', name_picture)}")
                file_out.write(f"<th>")
                file_out.write(
                    f'<img src = "{name_picture}" height="{image_size[0]} width="{image_size[1]}">')
                file_out.write(f"</th>")


    def start_filter(self, _file_list = []):

        with open("log.txt", mode='w') as log:
            log.write("")
        self.working = True
        self. file_list_local = _file_list
        self.file_list_using = []

        if self. file_list_local == []:
            self.file_list_using = self.file_list_global
        else:
            self.file_list_using = self.file_list_local


        #print(self. file_list_using)
        home = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(os.path.join(home, "Pdf")):
            os.makedirs(os.path.join(home, "Pdf"))
            print("pdf")

        if not os.path.exists(os.path.join(home, "html")):
            os.makedirs(os.path.join(home, "html"))
            print("html")

        if not os.path.exists(os.path.join(home, "Input")):
            os.makedirs(os.path.join(home, "Input"))
            print("input")

        if not os.path.exists(os.path.join(home, "Product")):
            os.makedirs(os.path.join(home, "Product"))
            print("Image")

        if not os.path.exists(os.path.join(home,"Product", "Image")):
            os.makedirs(os.path.join(home,"Product", "Image"))
            print("Image")

        directori = os.path.join(home, "Input")

        for file in self. file_list_using:
            if file.endswith(".csv"):

                #legge i dati graezzi dal gile .csv dell ordine e gli lavora in modo che restino solo le colonne
                dati, header, items, image_size = self.read_cvs_diveideOrder(pd.read_csv(file), home)
                #print(dati)
                i = 0
                #itera tra i singoli ordini
                for ordine in dati:
                    self.scrive_wood_and_stone(home,ordine)
                    #crea un dizionario con i singoli ordini con header e tabella items
                    dizionario = self.scrivi_dizinario(ordine, header, items)
                    self.scrivi_file_html(ordine_dizionario=dizionario, home = home,  header= header, items = items ,image_size = image_size)
                    #scrivi_file_csv(dizionario, i, home)
                    i += 1
            print("yes, I did it")

        self.working = False