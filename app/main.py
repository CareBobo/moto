from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.backend.conexion import get_db
from app.modelos.usuarios import Usuario as UsuarioModel
from app.modelos.accesorios import Accesorio as AccesorioModel

app = FastAPI()

# Configuración de CORS para permitir solicitudes del Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar "*" por la URL específica del Frontend si es necesario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de plantillas y archivos estáticos
templates = Jinja2Templates(directory="app/sign-in")
app.mount("/static", StaticFiles(directory="app/sign-in"), name="static")

# Endpoint para renderizar el index
@app.get("/", response_class=HTMLResponse)
def render_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint para renderizar el dashboard
@app.get("/dashboard", response_class=HTMLResponse)
def render_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post('/login')
def login_usuario(credentials: dict, db: Session = Depends(get_db)):
    correo = credentials.get("correo")
    password = credentials.get("password")
    if not correo or not password:
        raise HTTPException(status_code=400, detail="Correo y contraseña son requeridos")

    user = db.query(UsuarioModel).filter(UsuarioModel.correo == correo).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    return {"message": "Inicio de sesión exitoso", "correo": user.correo}


# CRUD para Usuarios
@app.post("/usuarios/")
def create_usuario(correo: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(UsuarioModel).filter(UsuarioModel.correo == correo).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    nuevo_usuario = UsuarioModel(correo=correo, password=password)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"message": "Usuario creado correctamente"}

@app.get("/usuarios/")
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(UsuarioModel).all()

@app.put("/usuarios/{usuario_id}")
def update_usuario(usuario_id: int, correo: str, password: str, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.correo = correo
    usuario.password = password
    db.commit()
    db.refresh(usuario)
    return {"message": "Usuario actualizado correctamente"}

@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"message": f"Usuario con ID {usuario_id} eliminado correctamente."}

# CRUD para Accesorios
@app.post("/accesorios/")
def create_accesorio(nombre: str, valor: str, db: Session = Depends(get_db)):
    nuevo_accesorio = AccesorioModel(nombre=nombre, valor=valor)
    db.add(nuevo_accesorio)
    db.commit()
    db.refresh(nuevo_accesorio)
    return {"message": "Accesorio creado correctamente"}

@app.get("/accesorios/")
def get_accesorios(db: Session = Depends(get_db)):
    return db.query(AccesorioModel).all()

@app.put("/accesorios/{accesorio_id}")
def update_accesorio(accesorio_id: int, nombre: str, valor: str, db: Session = Depends(get_db)):
    accesorio = db.query(AccesorioModel).filter(AccesorioModel.id == accesorio_id).first()
    if not accesorio:
        raise HTTPException(status_code=404, detail="Accesorio no encontrado")
    accesorio.nombre = nombre
    accesorio.valor = valor
    db.commit()
    db.refresh(accesorio)
    return {"message": "Accesorio actualizado correctamente"}

@app.delete("/accesorios/{accesorio_id}")
def delete_accesorio(accesorio_id: int, db: Session = Depends(get_db)):
    accesorio = db.query(AccesorioModel).filter(AccesorioModel.id == accesorio_id).first()
    if not accesorio:
        raise HTTPException(status_code=404, detail="Accesorio no encontrado")
    db.delete(accesorio)
    db.commit()
    return {"message": f"Accesorio con ID {accesorio_id} eliminado correctamente."}

@app.get("/usuarios/actual")
def get_current_user(correo: str, db: Session = Depends(get_db)):
    user = db.query(UsuarioModel).filter(UsuarioModel.correo == correo).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"correo": user.correo}
