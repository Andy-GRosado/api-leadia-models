from fastapi import APIRouter
import pandas as pd
import joblib
import numpy as np
from datetime import datetime
import cloudpickle as cp
from models.input_rfm import InputRFM

router_rfm = APIRouter(prefix="/rfm", tags=["RFM Clustering"])

def meses_hasta_hoy(X):
  hoy = pd.Timestamp(datetime.now().date())
  fechas = pd.to_datetime(X.iloc[:, 0], format='%Y-%m-%d')
  meses = (hoy.year - fechas.dt.year) * 12 + (hoy.month - fechas.dt.month)
  return meses.to_frame()


with open("kmeans_rfm_pipeline.pkl", "rb") as f:
    pipeline_rfm = cp.load(f)
# Cargar pipeline solo una vez
# pipeline_rfm = joblib.load("kmeans_rfm_pipeline.pkl")

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

# @router_rfm.post("/predict")
# def get_nearest_neighbors(data: InputKnn):
#     df = pd.DataFrame([data.dict()])
#     preprocesador = pipeline_rfm.named_steps['preprocessor']
#     knn_model = pipeline_rfm.named_steps['model']
    
#     transformed = preprocesador.transform(df)
#     (distances, indices) = knn_model.kneighbors(transformed)
#     indices_val = df_knn.iloc[indices[0]].index.tolist()
#     distances_val = distances[0].tolist()

#     result = {}
#     for index, value in enumerate(indices_val):
#         result[value] = distances_val[index]

#     return {
#         "neighbors": result
#     }