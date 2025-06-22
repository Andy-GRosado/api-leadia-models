from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
from datetime import datetime
import cloudpickle as cp
from models.input_rfm import InputRFM

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
        "cluster": int(cluster),
        "distancias": distancias_dict
    }


@router_rfm.get("/info")
def get_clusters_info():
    clusters = df_rfm['cluster'].unique()
    response = {}
    for c in clusters:
        response[f'{c}'] = df_rfm[df_rfm['cluster'] == c].describe().to_dict()
    return response

@router_rfm.get("/info/{cluster}")
def get_clusters_info(cluster: int):
    clusters = df_rfm['cluster'].unique()
    if (cluster not in clusters):
        raise HTTPException(status_code=404, detail={ "error":"Cluster not found", "message":"El cluster especificado no fue encontrado" })

    cluster_info = df_rfm[df_rfm['cluster'] == cluster].describe().to_dict()
    return cluster_info