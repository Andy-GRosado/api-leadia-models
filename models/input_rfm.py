from pydantic import BaseModel, Field, validator
from typing import Literal
from datetime import datetime

# KMEANS_VALID_DISTRITOS = [
#     'LA MOLINA', 'LIMA', 'COMAS', 'SANTA ANITA', 'LA VICTORIA', 'SAN BARTOLO',
#     'SAN ISIDRO', 'ATE', 'SANTIAGO DE SURCO', 'VILLA MARIA DEL TRIUNFO',
#     'PACHACAMAC', 'EL AGUSTINO', 'SAN MIGUEL', 'BARRANCO', 'LOS OLIVOS',
#     'CARABAYLLO', 'SAN JUAN DE LURIGANCHO', 'INDEPENDENCIA', 'CHORRILLOS',
#     'SAN MARTIN DE PORRES', 'BREÑA', 'MAGDALENA DEL MAR', 'MIRAFLORES',
#     'JESUS MARIA', 'SURQUILLO', 'VILLA EL SALVADOR', 'LINCE', 'RIMAC',
#     'PUEBLO LIBRE', 'ANCON', 'SAN LUIS',
# ]
# KMEANS_VALID_TIPOS_CONTRIBUYENTE = [
#     'SOCIEDAD ANONIMA CERRADA', 'EMPRESA INDIVIDUAL DE RESP. LTDA',
#     'SOC.COM.RESPONS. LTDA', 'SOCIEDAD ANONIMA', 'ASOCIACION',
#     'PERSONA NATURAL CON NEGOCIO', 'COOPERATIVAS, SAIS, CAPS',
#     'SOCIEDAD IRREGULAR', 'INSTITUCIONES RELIGIOSAS', 'SOCIEDAD CIVIL',
#     'UNIVERS. CENTROS EDUCAT. Y CULT.',
# ]

class InputRFM(BaseModel):
    last_purchase: datetime = Field(..., description="Fecha de la última compra")
    frequency: int = Field(..., description="Frecuencia de compra")
    # frequency: Literal[
    #     'SOCIEDAD ANONIMA CERRADA', 'EMPRESA INDIVIDUAL DE RESP. LTDA',
    #     'SOC.COM.RESPONS. LTDA', 'SOCIEDAD ANONIMA', 'ASOCIACION',
    #     'PERSONA NATURAL CON NEGOCIO', 'COOPERATIVAS, SAIS, CAPS',
    #     'SOCIEDAD IRREGULAR', 'INSTITUCIONES RELIGIOSAS', 'SOCIEDAD CIVIL',
    #     'UNIVERS. CENTROS EDUCAT. Y CULT.',
    # ] = Field(..., description="Tipo de contribuyente")
    monetary_value: float = Field(..., description="Valor monetario (Total de compras)")
    density_products: int = Field(..., description="Cantidad de productos comprados promedio")

    @validator("last_purchase")
    def validate_last_purchase(cls, v):
        if v >  datetime.now():
            raise ValueError("Ultima compra no permitida")
        return v
    
    @validator("frequency")
    def validate_frequency(cls, v):
        if v < 0:
            raise ValueError("Frecuencia no permitida")
        return v
    
    @validator("monetary_value")
    def validate_monetary_value(cls, v):
        if v < 0:
            raise ValueError("Valor monetario no permitido")
        return v
    
    @validator("density_products")
    def validate_density_products(cls, v):
        if v < 0:
            raise ValueError("Cantidad de productos comprados promedio no permitido")
        return v


