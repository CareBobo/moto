from app.backend.conexion import engine, Base
from app.modelos.usuarios import Usuario
from app.modelos.accesorios import Accesorio

# Crear todas las tablas definidas en los modelos
print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas correctamente.")
