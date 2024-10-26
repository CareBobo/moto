from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from backend.conexion import connection
from modelos.usuarios import Usuario
from modelos.accesorios import Accesorio


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    except ValueError as err:
        raise HTTPException(
            status_code=400, detail=f"Error en los valores: {err}")
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
    except ValueError as err:
        raise HTTPException(
            status_code=400, detail=f"Error en los valores: {err}")
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


@app.get('/accesorios')
async def get_aceesorios():
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM accesorios'

    try:
        cursor.execute(query)
        products = cursor.fetchall()
        return products
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los Accesorios: {err}")
    finally:
        cursor.close()


@app.get('/accesorios/{accesorios_id}')
async def get_accesorio(accesorios_id: int):
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM accesorios WHERE id = %s'
    values = (accesorios_id,)

    try:
        cursor.execute(query, values)
        products = cursor.fetchone()
        if products:
            return products
        else:
            raise HTTPException(
                status_code=404, detail=f"Accesorio con id {accesorios_id} no encontrado")
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el Accesorio: {err}")
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
            status_code=500, detail=f"Error al crear el Accesorio: {err}")
    except ValueError as err:
        raise HTTPException(
            status_code=400, detail=f"Error en los valores: {err}")
    finally:
        cursor.close()


@app.put('/accesorios/{accesorios_id}')
async def update_accesorio(accesorios_id: int, accesorios: Accesorio):
    cursor = connection.cursor()
    query = 'UPDATE accesorios SET nombre = %s, precio = %s WHERE id = %s'
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
            status_code=500, detail=f"Error al actualizar el Accesorio: {err}")
    except ValueError as err:
        raise HTTPException(
            status_code=400, detail=f"Error en los valores: {err}")
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
            status_code=500, detail=f"Error al eliminar el Accesorio: {err}")
    finally:
        cursor.close()


@app.post('/login')
def login(usuario: Usuario):
    cursor = connection.cursor()
    query = 'SELECT * FROM usuarios WHERE correo = %s AND password = %s'
    values = (usuario.email, usuario.password)

    try:
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            return {"message": "Usuario autenticado correctamente"}
        else:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado contraseña incorrecta")
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Error al autenticar el usuario: {err}")
    finally:
        cursor.close()
