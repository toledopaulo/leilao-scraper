import datetime
import pandas as pd

class Excel(object):
    def __init__(self):
        return
    
    def dict_to_pandas_excel(self, dictionary: list):
        dia_atual = str(datetime.datetime.today()).split(".")[0].replace(":", "-")
        planilha_path = "./planilhas/pandas-" + str(dia_atual) + ".xlsx"
        tabela = pd.DataFrame(dictionary).to_excel(planilha_path)