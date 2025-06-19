from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from typing import Literal
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import silhouette_score

from routes import clustering, nearest_neighbors, rfm_model

# Cargar el pipeline entrenado
pipeline = joblib.load("kmeans_pipeline.pkl")  # Ruta local al archivo .pkl

# Crear instancia de la aplicación
app = FastAPI(title="KMeans Clustering API")

app.include_router(clustering.router, prefix="/api/v1")
app.include_router(nearest_neighbors.router_knn, prefix="/api/v1")
app.include_router(rfm_model.router_rfm, prefix="/api/v1")

