from fastapi import APIRouter
from models.input_nn import InputNearestNeighbors
import pandas as pd
import joblib

# Create a parent router for the common /neighbors path
router_neighbors = APIRouter(prefix="/neighbors", tags=["Nearest Neighbors"])

# Create child routers for clients and prospects
router_nn_clients = APIRouter(prefix="/clients", tags=["Nearest Neighbors clients"])
router_nn_prospects = APIRouter(prefix="/prospects", tags=["Nearest Neighbors prospects"])

# Cargar pipeline solo una vez
pipeline_nn_prospects = joblib.load("dir/nearest_neighbors/nearest_neighbors_prospects.pkl")
df_nn_prospects = joblib.load("dir/nearest_neighbors/df_prospects.pkl")

pipeline_nn_clients = joblib.load("dir/nearest_neighbors/nearest_neighbors_clients.pkl")
df_nn_clients = joblib.load("dir/nearest_neighbors/df_clients.pkl")


@router_nn_prospects.post("/predict")
def get_nearest_neighbors_prospects(data: InputNearestNeighbors):
    df = pd.DataFrame([data.dict()])
    preprocesador = pipeline_nn_prospects.named_steps['preprocessor']
    nn_model = pipeline_nn_prospects.named_steps['model']
    
    transformed = preprocesador.transform(df)
    (distances, indices) = nn_model.kneighbors(transformed)
    indices_val = df_nn_prospects.iloc[indices[0]].index.tolist()
    distances_val = distances[0].tolist()

    result = {}
    for index, value in enumerate(indices_val):
        result[value] = distances_val[index]

    return {
        "neighbors": result
    }

@router_nn_clients.post("/predict")
def get_nearest_neighbors_clients(data: InputNearestNeighbors):
    df = pd.DataFrame([data.dict()])
    preprocesador = pipeline_nn_clients.named_steps['preprocessor']
    nn_model = pipeline_nn_clients.named_steps['model']
    
    transformed = preprocesador.transform(df)
    (distances, indices) = nn_model.kneighbors(transformed)
    indices_val = df_nn_clients.iloc[indices[0]].index.tolist()
    distances_val = distances[0].tolist()

    result = {}
    for index, value in enumerate(indices_val):
        result[value] = distances_val[index]

    return {
        "neighbors": result
    }

router_neighbors.include_router(router_nn_clients)
router_neighbors.include_router(router_nn_prospects)