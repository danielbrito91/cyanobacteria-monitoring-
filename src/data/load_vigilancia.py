import os
import urllib
import yaml
from typing import Text
import pandas as pd

def load_vigilancia(config_path: Text) -> pd.DataFrame:
    """Realiza a leitura de dados baixados da Vigilancia para um dado manancial"""

    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    if not os.path.isfile(config["data_load"]["labels_download"]):
        urllib.request.urlretrieve(
            config["data_create"]["url"],
            config["data_load"]["labels_download"])

    vigilancia = pd.read_csv(config["data_load"]["labels_download"],
           compression="zip",
            sep=";",
            decimal=",",
            encoding="latin-1", low_memory=False,
            parse_dates=["Data de preenchimento do relatório mensal",
                        "Data da coleta"])
    
    vigilancia =  vigilancia.loc[( vigilancia["Município"] == config["data_create"]["municipio"]) &
          (vigilancia["Nome do manancial superficial"] == config["data_create"]["manancial"]), :]
    
    return vigilancia