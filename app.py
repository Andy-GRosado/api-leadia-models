from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from typing import Literal
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import silhouette_score
from fastapi.middleware.cors import CORSMiddleware
from routes import clustering, nearest_neighbors, rfm_model

# Cargar el pipeline entrenado
pipeline = joblib.load("kmeans_pipeline.pkl")  # Ruta local al archivo .pkl

# Crear instancia de la aplicación
app = FastAPI(title="KMeans Clustering API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

app.include_router(clustering.router, prefix="/api/v1")
app.include_router(nearest_neighbors.router_neighbors, prefix="/api/v1")
app.include_router(rfm_model.router_rfm, prefix="/api/v1")

