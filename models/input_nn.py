from pydantic import BaseModel, Field, validator
from typing import Literal

class InputNearestNeighbors(BaseModel):
    tipo_contribuyente: str
    actividad_economica_principal_cod: int | str
    actividad_economica_secundaria_cod: int | str
    trabajadores_actual: int
    antiguedad: int

