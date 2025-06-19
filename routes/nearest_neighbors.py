from fastapi import APIRouter
from models.input_knn import InputKnn
import pandas as pd
import joblib

router_knn = APIRouter(prefix="/neighbors", tags=["Nearest Neighbors"])

# Cargar pipeline solo una vez
pipeline_knn = joblib.load("knn_pipeline.pkl")
df_knn = joblib.load("df_knn.pkl")

@router_knn.post("/predict")
def get_nearest_neighbors(data: InputKnn):
    df = pd.DataFrame([data.dict()])
    preprocesador = pipeline_knn.named_steps['preprocessor']
    knn_model = pipeline_knn.named_steps['model']
    
    transformed = preprocesador.transform(df)
    (distances, indices) = knn_model.kneighbors(transformed)
    indices_val = df_knn.iloc[indices[0]].index.tolist()
    distances_val = distances[0].tolist()

    result = {}
    for index, value in enumerate(indices_val):
        result[value] = distances_val[index]

    return {
        "neighbors": result
    }