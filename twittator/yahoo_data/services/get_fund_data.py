import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import requests
import pprint
import os
import zipfile
import io
class GetFundData:
    def __init__(self):
        years = range(2020,2023)

        url_base = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/'
        
        year = '2023'
        print(url_base + f"dfp_cia_aberta_{year}.zip")
        download = requests.get(url_base + f"dfp_cia_aberta_{year}.zip")

        zip = zipfile.ZipFile(download.content.decode())
        zip.extractall()

        print(zip)

instance = GetFundData()