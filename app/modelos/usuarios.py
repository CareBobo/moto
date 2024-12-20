from sqlalchemy import Column, Integer, String
from app.backend.conexion import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
