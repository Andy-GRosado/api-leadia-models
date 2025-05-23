from pydantic import BaseModel, Field, validator
from typing import Literal

KMEANS_VALID_DISTRITOS = [
    'LA MOLINA', 'LIMA', 'COMAS', 'SANTA ANITA', 'LA VICTORIA', 'SAN BARTOLO',
    'SAN ISIDRO', 'ATE', 'SANTIAGO DE SURCO', 'VILLA MARIA DEL TRIUNFO',
    'PACHACAMAC', 'EL AGUSTINO', 'SAN MIGUEL', 'BARRANCO', 'LOS OLIVOS',
    'CARABAYLLO', 'SAN JUAN DE LURIGANCHO', 'INDEPENDENCIA', 'CHORRILLOS',
    'SAN MARTIN DE PORRES', 'BREÑA', 'MAGDALENA DEL MAR', 'MIRAFLORES',
    'JESUS MARIA', 'SURQUILLO', 'VILLA EL SALVADOR', 'LINCE', 'RIMAC',
    'PUEBLO LIBRE', 'ANCON', 'SAN LUIS',
]
KMEANS_VALID_TIPOS_CONTRIBUYENTE = [
    'SOCIEDAD ANONIMA CERRADA', 'EMPRESA INDIVIDUAL DE RESP. LTDA',
    'SOC.COM.RESPONS. LTDA', 'SOCIEDAD ANONIMA', 'ASOCIACION',
    'PERSONA NATURAL CON NEGOCIO', 'COOPERATIVAS, SAIS, CAPS',
    'SOCIEDAD IRREGULAR', 'INSTITUCIONES RELIGIOSAS', 'SOCIEDAD CIVIL',
    'UNIVERS. CENTROS EDUCAT. Y CULT.',
]

class InputKmeans(BaseModel):
    distrito: str
    tipo_contribuyente: str
    actividad_economica_principal_cod: int
    actividad_economica_secundaria_cod: float
    trabajadores_actual: int
    antiguedad: int

    @validator("distrito")
    def validate_distrito(cls, v):
        if v not in KMEANS_VALID_DISTRITOS:
            raise ValueError("Distrito no permitido")
        return v
    
    @validator("tipo_contribuyente")
    def validate_tipo_contribuyente(cls, v):
        if v not in KMEANS_VALID_TIPOS_CONTRIBUYENTE:
            raise ValueError("Tipo de contribuyente no permitido")
        return v
    


