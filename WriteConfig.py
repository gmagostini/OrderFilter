from random import randint

import pandas as pd
from xlwings import xrange

df = pd.DataFrame({'A': [randint(1, 9) for x in xrange(10)],
                       'B': [randint(1, 9)*10 for x in xrange(10)],
                       'C': [randint(1, 9)*100 for x in xrange(10)]})

for index, row in df.iterrows():
    for colum in list(df):
        print(row[colum])



def scrivi_dizinario(elenco_ordini_ragruppati, header, items):
    ordine1 = elenco_ordini_ragruppati
    ordine_dizionario = {}
    ordine_dizionario["Order #"]  = ordine1["Order #"].iat[0]
    ordine_dizionario["Date"]  = ordine1["Date"].iat[0]
    ordine_dizionario["Billing Customer"]  = ordine1["Billing Customer"].iat[0]
    ordine_dizionario["Shipping Label"]  = ordine1["Shipping Label"].iat[0]
    ordine_dizionario["Buyer's Email"]  = ordine1["Buyer's Email"].iat[0]
    ordine_dizionario["Buyer's Phone #"]  = ordine1["Buyer's Phone #"].iat[0]
    ordine_dizionario["Item's Name"] = ordine1[[ "Item's Name", "Item's Variant", "Qty", "Notes to Seller", "Weight"]]
    return ordine_dizionario




def scrivi_file_html(ordine_dizionario = None, home = None, header = [], items = [] ):
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
                                <td>Notes to Seller</td>
                                <td>"Weight"</td>
                            </tr>
                                """)

    for column, row in ordine_dizionario["Item's Name"].iterrows():
        row["Item's Variant"] = row["Item's Variant"].replace('|', '<br>')
        file_out.write(f"""
                    <tr>
                        <td>{row["Item's Name"]}</td>
                        <td>{row["Item's Variant"]}</td>
                        <td>{row["Qty"]}</td>
    
                        """)
        if f"{row['Notes to Seller']}" != "nan":
            file_out.write(f"""
                                    <td>{row["Notes to Seller"]}</td>
                                    """)

        file_out.write(f"""
                                <td>{row["Weight"]}</td>
                                """)

        file_out.write("</tr>")
    file_out.write("</table>")

    pdfkit.from_file(file_html, file_pdf)