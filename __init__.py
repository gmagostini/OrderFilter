import glob
import os

import pandas as pd
import csv
import pdfkit

def read_cvs_diveideOrder(primitive_data):

    #print(list(primitive_data))
    refind_data = primitive_data[["Order #", "Date",  "Billing Customer", "Shipping Label", "Buyer's Email", "Buyer's Phone #", "Item's Name", "Item's Variant", "Qty", "Notes to Seller"]]
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

    return elenco_ordini_ragruppati

def scrivi_dizinario(elenco_ordini_ragruppati):
    ordine1 = elenco_ordini_ragruppati
    ordine_dizionario = {}
    ordine_dizionario["Order #"]  = ordine1["Order #"].iat[0]
    ordine_dizionario["data"]  = ordine1["Date"].iat[0]
    ordine_dizionario["Billing Customer"]  = ordine1["Billing Customer"].iat[0]
    ordine_dizionario["Shipping Label"]  = ordine1["Shipping Label"].iat[0]
    ordine_dizionario["Buyer's Email"]  = ordine1["Buyer's Email"].iat[0]
    ordine_dizionario["Buyer's Phone #"]  = ordine1["Buyer's Phone #"].iat[0]
    ordine_dizionario["Item's Name"] = ordine1[[ "Item's Name", "Item's Variant", "Qty", "Notes to Seller"]]
    return ordine_dizionario


def scrivi_file_html(ordine_dizionario = None, home = None):

    file_html = os.path.join(home,"html"
                             , f"order{ordine_dizionario['Order #']}.html")
    file_pdf = os.path.join(home,"Pdf"
                             , f"order{ordine_dizionario['Order #']}.pdf")
    with open(file_html, mode='w') as file_out:

        ordine_dizionario["Shipping Label"] = ordine_dizionario["Shipping Label"].replace('/', '<br>')

        file_out.write(f"""
        <table border=1>
            <tr>
                <th>Order #</th>
                <th>{ordine_dizionario["Order #"]}</th>
            </tr>
            <tr>
                <td>data</td>
                <td>{ordine_dizionario["data"]}</td>
            </tr>
            <tr>
                <td>Billing Customer</td>
                <td>{ordine_dizionario["Billing Customer"]}</td>
            </tr>
            <tr>
                <td>Shipping Label</td>
                <td>S{ordine_dizionario["Shipping Label"]}</td>
            </tr>
            <tr>
                <td>Buyer's Email</td>
                <td>{ordine_dizionario["Buyer's Email"]}</td>
            </tr>
            <tr>
                <td>Buyer's Phone #</td>
                <td>{ordine_dizionario["Buyer's Phone #"]}</td>
            </tr>
        """)

        file_out.write(f"""
                        <tr>
                            <td>Item's Name</td>
                            <td>Item's Variant</td>
                            <td>Qty</td>
                        </tr>
                            """)

        for column, row in ordine_dizionario["Item's Name"].iterrows():
            row["Item's Variant"] = row["Item's Variant"].replace('|', '<br>')
            file_out.write(f"""
                <tr>
                    <td>{row["Item's Name"]}</td>
                    <td>{row["Item's Variant"]}</td>
                    <td>{row["Qty"]}</td>
                </tr>
                    """)
            if f"{row['Notes to Seller']}" != "nan":
                file_out.write(f"""
                                <tr>
                                    <td>Notes to Seller</td>
                                    <td>{row["Notes to Seller"]}</td>
                                </tr>
                                    """)

        file_out.write("</table>")

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


    directori = os.path.join(home, "Input")

    for file in os.listdir(directori):
        if file.endswith(".csv"):
            primitive_data = pd.read_csv(os.path.join(directori,file))
            dati = read_cvs_diveideOrder(primitive_data)
            #print(dati)
            i = 0
            for ordine in dati:
                dizionario = scrivi_dizinario(ordine)
                scrivi_file_html(ordine_dizionario=dizionario, home = home)
                #scrivi_file_csv(dizionario, i, home)
                i += 1
        print("yes, I do it")

if __name__ == "__main__":
    main()