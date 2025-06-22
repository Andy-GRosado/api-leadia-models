from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
from datetime import datetime
import cloudpickle as cp
from models.input_rfm import InputRFM
from models.controllers.mongo_db import MongoData

router_rfm = APIRouter(prefix="/rfm", tags=["RFM Clustering"])

# def meses_hasta_hoy(X):
#   hoy = pd.Timestamp(datetime.now().date())
#   fechas = pd.to_datetime(X.iloc[:, 0], format='%Y-%m-%d')
#   meses = (hoy.year - fechas.dt.year) * 12 + (hoy.month - fechas.dt.month)
#   return meses.to_frame()


with open("kmeans_rfm_pipeline.pkl", "rb") as f:
    pipeline_rfm = cp.load(f)

with open("df_rfm.pkl", "rb") as f:
    df_rfm = cp.load(f)

def GetClientsInfo():
    mongo_data_client = MongoData()
    df_data = mongo_data_client.get_data()
    def convert_to_rfm(df, id_column, r_column, f_column, m_column, **more_fields):
        df_grouped = df.groupby(id_column).agg(
        recency=(r_column, 'max'),
        monetary_value=(m_column, 'sum'),
        quantity_purchases=(f_column, 'nunique'),
        **more_fields
        ).reset_index()
        return df_grouped
    
    df_agrupado = convert_to_rfm(df_data, 'ruc', 'fecha_operacion', 'sec', 'comision_final', quantity_products=('sec', 'count'))
    df_agrupado = df_agrupado[df_agrupado['monetary_value'] > 0].copy()
    df_agrupado['recency'] = pd.to_datetime(df_agrupado['recency'], format='%Y-%m-%d')

    preprocesador = pipeline_rfm[:-1]
    kmeans_model = pipeline_rfm.named_steps['kmeans']

    X_transformed = preprocesador.transform(df_agrupado)
    X_labels = kmeans_model.predict(X_transformed)
    df_final = df_agrupado.copy()
    df_final['cluster'] = X_labels
    df_merged = pd.merge(df_data, df_final, on='ruc', how='inner')
    return df_merged

def GetClusterInfo(df, columns = ['plan']):
    if (len(columns) <= 0):
        return {}
    num_columns = ['extorno_tope', 'cargo_real', 'cargo_fijo', 'extorno_sivco', 'comision_final', 'fuera_plazo', 'factor', 'comision_base']
    cat_columns = ['periodo', 'tipo_operacion', 'fuera_plazo', 'plan', 'servicio', 'estado_linea']
    response = {}
    # min_cluster = df['cluster'].min()
    # max_cluster = df['cluster'].max()
    
    for cluster in df['cluster'].unique():
        response_cluster = {
            'size': 0,
            'columns': {},
            'elements_id': [],
        }

        response_cluster['elements_id'] = df_clients[df_clients['cluster'] == cluster]['ruc'].unique().tolist()
        response_cluster['size'] = len(response_cluster['elements_id'])

        for col in columns:
            column_info = {}
            
            if (col in num_columns): column_info['column_type'] = 'numeric'
            elif (col in cat_columns): column_info['column_type'] = 'categoric'
            else: raise HTTPException(status_code=404, detail={ 'error': 'Not identified column', 'message': f'No se encontro la columna "{columns}"' })

            column_stats = df_clients[df_clients['cluster'] == cluster][col].describe().to_dict()
            if (col in cat_columns): column_stats['value_counts'] = df_clients[df_clients['cluster'] == cluster][col].value_counts().to_dict()
            column_info.update(column_stats)
            response_cluster['columns'][col] = column_info
        
        response[str(cluster)] = response_cluster
    return response


df_clients = GetClientsInfo()
clusters_info = GetClusterInfo(df=df_clients)

@router_rfm.post("/predict")
def predict_cluster(data: InputRFM):
    df = pd.DataFrame([data.dict()])
    df.rename(columns={'last_purchase': 'recency', 'frequency': 'quantity_purchases', 'density_products': 'quantity_products'}, inplace=True)

    preprocesador = pipeline_rfm[:-1]
    kmeans_model = pipeline_rfm.named_steps['kmeans']
    
    transformed = preprocesador.transform(df)
    cluster = kmeans_model.predict(transformed)[0]

    centroides = kmeans_model.cluster_centers_
    distancias = np.linalg.norm(centroides - transformed, axis=1)
    distancias_dict = [float(d) for d in distancias]

    return {
        "rfm_values": transformed.to_dict()[0],
        "cluster": int(cluster),
        "distancias": distancias_dict
    }

# GET   /info/              -> Describe RFM distribution
@router_rfm.get("/info")
def get_clusters_info():
    clusters = df_rfm['cluster'].unique()
    response = {}
    for c in clusters:
        response[f'{c}'] = df_rfm[df_rfm['cluster'] == c].describe().to_dict()
    return response

# GET   /info/{cluster}     -> Describe RFM distribution for cluster
@router_rfm.get("/info/{cluster}")
def get_clusters_info(cluster: int):
    clusters = df_rfm['cluster'].unique()
    if (cluster not in clusters):
        raise HTTPException(status_code=404, detail={ "error":"Cluster not found", "message":"El cluster especificado no fue encontrado" })

    cluster_info = df_rfm[df_rfm['cluster'] == cluster].describe().to_dict()
    return cluster_info


# GET   /clients/           -> Get info of clients of all the clusters
# TODO: Get the rucs, plans and RFM values for each ruc in clusters
@router_rfm.get("/clients/")
def update_clients_data():
    return clusters_info


# POST  /clients/           -> Update info of clients
@router_rfm.post("/clients/")
def update_clients_data():
    df_clients = GetClientsInfo()
    clusters_info = GetClusterInfo(df=df_clients, cluster=1)
    return { "message": "Clientes actualizados correctamente" }


@router_rfm.get("/clients/{cluster}/{column}")
def get_cluster_clients(cluster: int, column: str):
    num_columns = ['extorno_tope', 'cargo_real', 'cargo_fijo', 'extorno_sivco', 'comision_final', 'fuera_plazo', 'factor', 'comision_base', 'cluster']
    cat_columns = ['periodo', 'tipo_operacion', 'fuera_plazo', 'plan', 'servicio', 'estado_linea', 'cluster']

    response = {}
    if (column in num_columns):
        response['column_type'] = 'numeric'
    elif (column in cat_columns):
        response['column_type'] = 'categoric'
    else:
        raise HTTPException(status_code=404, detail={ 'error': 'Not identified column', 'message': f'No se encontro la columna "{column}"' })
    
    for i in range(4):
        count_elements = df_clients[df_clients['cluster'] == i].shape[0]
        print(f'In {i} there is {count_elements} elements')
    
    return response


# GET   /info/              -> Describe RFM distribution
# GET   /info/{cluster}     -> Describe RFM distribution for cluster
# 
# GET   /clients/           -> Get info of clients of all the clusters
# POST  /clients/           -> Update info of clients
# GET   /clients/{cluster}  -> Get info of clients of all the clusters
# 