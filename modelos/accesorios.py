from pydantic import BaseModel, Field, condecimal
from decimal import Decimal

class Accesorio(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    valor: Decimal = condecimal(gt=0, decimal_places=2)