import glob
import os

import pandas as pd

import pdfkit
import json

def read_cvs_diveideOrder(primitive_data, home):
    column_name = {}
    header = []
    items = []
    with open(os.path.join(home, "config.json"), 'r') as read_file:
        column_name = json.load(read_file)
        header = column_name["Header"]
        items = column_name["Items"]

    header_ref = []
    item_ref = []
    for col in header :
        if col in primitive_data:
            header_ref.append(col)

    for col in items:
        if col in primitive_data:
            item_ref.append(col)
        else:
            print(f"ho escluso {col}")

    all_column = header_ref + item_ref
                    #print(list(primitive_data))
    refind_data = primitive_data[all_column]
    #seleziona numero ordini e eleiminia duplicati
    ordini = refind_data["Order #"].to_list()

    ordini.sort()

    ordini_indice = []

    for i in ordini:
        if i not in ordini_indice:
            ordini_indice.append(i)

    elenco_ordini_ragruppati = []
    for i in ordini_indice:
        elenco_ordini_ragruppati.append(refind_data[refind_data["Order #"] == i])

    return elenco_ordini_ragruppati, header_ref, item_ref

def scrivi_dizinario(elenco_ordini_ragruppati, header, items):
    ordine1 = elenco_ordini_ragruppati
    ordine_dizionario = {}
    for name in header:
        ordine_dizionario[name] = ordine1[name].iat[0]

    ordine_dizionario["Items"] = ordine1[items]
    return ordine_dizionario


def scrivi_file_html(ordine_dizionario = None, home = None, header = [], items = [] ):

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
            if name != "Notes to Seller":
                file_out.write(f"""
                                <th> {name} </th>
                            """)
        file_out.write(f"</tr>")

        items_name_list = []

        for index, row in ordine_dizionario["Items"].iterrows():
            file_out.write(f"<tr>")
            for name in items:
                if name != "Notes to Seller":
                    file_out.write(f"""
                                <th> {row[name]} </th>
                                """)

            file_out.write(f"</tr>")
            if str(row["Notes to Seller"]) != 'nan':
                file_out.write(f"<tr>")
                file_out.write(f"""
                                <th>Notes to Seller</th>
                                <th> {row["Notes to Seller"]} </th>
                                """)
                file_out.write(f"</tr>")
            if  row["Item's Name"] not in  items_name_list:
                items_name_list.append(row["Item's Name"])

        file_out.write("</table>")
        for name_items in items_name_list:
            for name_picture in os.listdir(os.path.join(home,"Image")):
                print(f"{name_items}  {name_picture}  {name_items is name_picture}")
                name_items = name_items.replace('/', '')
                name_items = name_items.replace('\\', '')
                if name_items in name_picture:
                    file_out.write("<body>")
                    file_out.write(f'<img src = "{os.path.join(home, "Image", name_picture)}" height="420 width="420">')
                    file_out.write("</body>")
                    print(f"inserisoc immagine {os.path.join(home, 'Image', name_picture)}")


    print(ordine_dizionario['Order #'])
    pdfkit.from_file(file_html, file_pdf)




def main():
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

    if not os.path.exists(os.path.join(home, "Image")):
        os.makedirs(os.path.join(home, "Image"))
        print("Image")

    directori = os.path.join(home, "Input")

    for file in os.listdir(directori):
        if file.endswith(".csv"):
            primitive_data = pd.read_csv(os.path.join(directori,file,))
            dati, header, items = read_cvs_diveideOrder(primitive_data, home)
            #print(dati)
            i = 0
            for ordine in dati:
                dizionario = scrivi_dizinario(ordine, header, items)
                scrivi_file_html(ordine_dizionario=dizionario, home = home,  header= header, items = items)
                #scrivi_file_csv(dizionario, i, home)
                i += 1
        print("yes, I do it")

if __name__ == "__main__":
    main()