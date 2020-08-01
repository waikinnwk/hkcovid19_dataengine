import pandas as pd
import pdfplumber
import requests
import ssl
import os

url = "https://www.chp.gov.hk/files/pdf/building_list_eng.pdf"

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

file_name = "tempPdf.pdf"



building_name_key = 'Building Name'
district_key = 'District'
related_case_key = 'Related Confirmed / \nProbable Case(s)'
try:
    response = requests.get(url, headers=header)
    if os.path.exists(file_name):
      os.remove(file_name)
    open(file_name, 'wb').write(response.content)

    pdf = pdfplumber.open(file_name)
    p0 = pdf.pages[0]

    table = p0.extract_table()
    df0 = pd.DataFrame(table[1:], columns=table[0])
    print(df0)
    print(df0.iloc[1][district_key])
    print(df0.iloc[1][building_name_key])
    print(df0.iloc[1][related_case_key])

    pdf.close()
    if os.path.exists(file_name):
      os.remove(file_name)

except Exception as e:
    print("Error " + str(e))

