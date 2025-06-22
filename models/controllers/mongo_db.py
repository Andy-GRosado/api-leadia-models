
from pymongo import MongoClient
import pandas as pd

class InfoData:
  def __init__(self) -> None:
    pass

  def get_data(self) -> None:
    pass

class MongoData(InfoData):
  def __init__(self) -> None:
    self.mongo_uri = "mongodb+srv://fradmin:PZq7C51e8g0SNZm4@frcluster.ymiqdog.mongodb.net"
    self.client = MongoClient(self.mongo_uri)
    self.db_sales = self.client['sales']
    self.collection_reg_movils = self.db_sales['reg_movils']
    self.document = self.collection_reg_movils.find_one()

  def columns_intersection(self, list_columns):
    interseccion_columnas = set(list_columns[0])
    for lista_columnas in list_columns[1:]:
        interseccion_columnas = interseccion_columnas.intersection(set(lista_columnas))
    lista_columnas_comunes = list(interseccion_columnas)
    return lista_columnas_comunes

  def get_full_df(self, period_document):
    periodo = period_document['periodo']
    df = pd.DataFrame(period_document['data'])
    df['periodo'] = periodo
    return df

  def get_data(self):
    list_df = [self.get_full_df(period_document) for period_document in self.collection_reg_movils.find()]
    columnas_comunes = self.columns_intersection([df.columns for df in list_df])
    df_final = pd.concat([df[columnas_comunes] for df in list_df])
    return df_final
