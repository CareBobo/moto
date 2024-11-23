from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import mysql.connector
from app.backend.conexion import connection
from app.modelos.usuarios import Usuario
from app.modelos.accesorios import Accesorio
from fastapi.requests import Request


# Crear instancia de FastAPI
app = FastAPI()

# Configuración de plantillas y archivos estáticos
templates = Jinja2Templates(directory="app/sign-in")
app.mount("/static", StaticFiles(directory="app/sign-in"), name="static")

# Middleware CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raíz (/) para mostrar un mensaje de bienvenida
@app.get("/")
async def root():
    return {"message": "¡Bienvenido a mi API con FastAPI!"}

# Endpoint para renderizar el formulario de login
@app.get("/login", response_class=HTMLResponse)
async def render_login(request: Request):
    user_name = "Invitado"
    return templates.TemplateResponse("index.html", {"request": request, "user_name": user_name})

# CRUD para usuarios
@app.get('/usuarios')
async def get_usuarios():
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM usuarios'

    try:
        cursor.execute(query)
        users = cursor.fetchall()
        return users
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los usuarios: {err}")
    finally:
        cursor.close()

@app.get('/usuarios/{usuario_id}')
async def get_usuario(usuario_id: int):
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM usuarios WHERE id = %s'
    values = (usuario_id,)

    try:
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            return user
        else:
            raise HTTPException(
                status_code=404, detail=f"Usuario con id {usuario_id} no encontrado")
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el usuario: {err}")
    finally:
        cursor.close()

@app.post('/usuarios')
async def create_usuario(usuario: Usuario):
    cursor = connection.cursor()
    query = 'INSERT INTO usuarios (correo, password) VALUES (%s, %s)'
    values = (usuario.correo, usuario.password)

    try:
        cursor.execute(query, values)
        connection.commit()
        return {"message": "Usuario creado correctamente"}
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al crear el usuario: {err}")
    finally:
        cursor.close()

@app.put('/usuarios/{usuario_id}')
async def update_usuario(usuario_id: int, usuario: Usuario):
    cursor = connection.cursor()
    query = 'UPDATE usuarios SET correo = %s, password = %s WHERE id = %s'
    values = (usuario.correo, usuario.password, usuario_id)

    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail=f"Usuario con id {usuario_id} no encontrado")
        return {"message": "Usuario actualizado correctamente"}
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar el usuario: {err}")
    finally:
        cursor.close()

@app.delete('/usuarios/{usuario_id}')
async def delete_usuario(usuario_id: int):
    cursor = connection.cursor()
    query = 'DELETE FROM usuarios WHERE id = %s'
    values = (usuario_id,)

    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail=f"Usuario con id {usuario_id} no encontrado")
        return {"message": "Usuario eliminado correctamente"}
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el usuario: {err}")
    finally:
        cursor.close()

# CRUD para accesorios
@app.get('/accesorios')
async def get_accesorios():
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM accesorios'

    try:
        cursor.execute(query)
        products = cursor.fetchall()
        return products
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los accesorios: {err}")
    finally:
        cursor.close()

@app.get('/accesorios/{accesorios_id}')
async def get_accesorio(accesorios_id: int):
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM accesorios WHERE id = %s'
    values = (accesorios_id,)

    try:
        cursor.execute(query, values)
        product = cursor.fetchone()
        if product:
            return product
        else:
            raise HTTPException(
                status_code=404, detail=f"Accesorio con id {accesorios_id} no encontrado")
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el accesorio: {err}")
    finally:
        cursor.close()

@app.post('/accesorios')
async def create_accesorio(accesorios: Accesorio):
    cursor = connection.cursor()
    query = 'INSERT INTO accesorios (nombre, valor) VALUES (%s, %s)'
    values = (accesorios.nombre, accesorios.valor)

    try:
        cursor.execute(query, values)
        connection.commit()
        return {"message": "Accesorio creado correctamente"}
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al crear el accesorio: {err}")
    finally:
        cursor.close()

@app.put('/accesorios/{accesorios_id}')
async def update_accesorio(accesorios_id: int, accesorios: Accesorio):
    cursor = connection.cursor()
    query = 'UPDATE accesorios SET nombre = %s, valor = %s WHERE id = %s'
    values = (accesorios.nombre, accesorios.valor, accesorios_id)

    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail=f"Accesorio con id {accesorios_id} no encontrado")
        return {"message": "Accesorio actualizado correctamente"}
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar el accesorio: {err}")
    finally:
        cursor.close()

@app.delete('/accesorios/{accesorios_id}')
async def delete_accesorio(accesorios_id: int):
    cursor = connection.cursor()
    query = 'DELETE FROM accesorios WHERE id = %s'
    values = (accesorios_id,)

    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail=f"Accesorio con id {accesorios_id} no encontrado")
        return {"message": "Accesorio eliminado correctamente"}
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el accesorio: {err}")
    finally:
        cursor.close()
        
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user_name": "Invitado"})        

@app.post('/login')
def login(usuario: Usuario):
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM usuarios WHERE correo = %s AND password = %s'
    values = (usuario.correo, usuario.password)

    try:
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            return {"message": "Usuario autenticado correctamente"}
        else:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado o contraseña incorrecta"
            )
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al autenticar el usuario: {err}"
        )
    finally:
        cursor.close()


