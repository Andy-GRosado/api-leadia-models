from fastapi import APIRouter
from models.input_kmeans import InputKmeans
import pandas as pd
import joblib
import numpy as np

router = APIRouter(prefix="/clustering", tags=["Clustering"])

# Cargar pipeline solo una vez
pipeline_kmeans = joblib.load("kmeans_pipeline.pkl")

@router.post("/predict2")
def predict_cluster(data: InputKmeans):
    df = pd.DataFrame([data.dict()])
    cluster = pipeline_kmeans.predict(df)[0]
    return {"cluster_predicho": int(cluster)}

@router.post("/predict")
def predict_cluster_with_distances(data: InputKmeans):
    df = pd.DataFrame([data.dict()])
    preprocesador = pipeline_kmeans[:-1]
    kmeans_model = pipeline_kmeans.named_steps['model']
    
    transformed = preprocesador.transform(df)
    cluster = kmeans_model.predict(transformed)[0]

    centroides = kmeans_model.cluster_centers_
    distancias = np.linalg.norm(centroides - transformed, axis=1)
    distancias_dict = [float(d) for d in distancias]

    return {
        "cluster": int(cluster),
        "distancias": distancias_dict
    }