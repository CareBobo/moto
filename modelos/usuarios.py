from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

class Usuario(BaseModel):
    correo: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=100, pattern=r'^[A-Za-z\d@$!%*?&]{8,}$')]
