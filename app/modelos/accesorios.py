from sqlalchemy import Column, Integer, String
from app.backend.conexion import Base

class Accesorio(Base):
    __tablename__ = "accesorios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    valor = Column(String(50), nullable=False)
