
import os
from urllib.parse import urlparse, unquote

import pg8000.dbapi
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("No se encuentra DATABASE_URL en el archivo .env")


# Crear aplicación
app = FastAPI(title="API Catálogo de Videojuegos")


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo de datos
class Videojuego(BaseModel):
    titulo: str = Field(min_length=1)
    plataforma: str
    genero: str
    anio: int
    precio: float
    imagen_url: str | None = None


# Conexión con Supabase
def conectar():
    datos = urlparse(DATABASE_URL)

    return pg8000.dbapi.connect(
        user=unquote(datos.username or ""),
        password=unquote(datos.password or ""),
        host=datos.hostname,
        port=datos.port or 5432,
        database=datos.path.lstrip("/"),
        ssl_context=True
    )


# Función para ejecutar consultas SQL
def ejecutar_sql(sql, parametros=(), fetch="all"):
    conexion = conectar()
    cursor = None

    try:
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)

        if fetch == "one":
            fila = cursor.fetchone()
            columnas = [columna[0] for columna in cursor.description]
            resultado = dict(zip(columnas, fila)) if fila else None

        elif fetch == "all":
            filas = cursor.fetchall()
            columnas = [columna[0] for columna in cursor.description]
            resultado = [
                dict(zip(columnas, fila)) for fila in filas
            ]

        else:
            resultado = None

        conexion.commit()
        return resultado

    except Exception:
        conexion.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


# GET: listar videojuegos
@app.get("/videojuegos")
def listar_videojuegos():
    return ejecutar_sql(
        "SELECT * FROM videojuegos ORDER BY id"
    )


# GET: buscar videojuego por ID
@app.get("/videojuegos/{id}")
def obtener_videojuego(id: int):
    videojuego = ejecutar_sql(
        "SELECT * FROM videojuegos WHERE id = %s",
        (id,),
        fetch="one"
    )

    if videojuego is None:
        raise HTTPException(
            status_code=404,
            detail="Videojuego no encontrado"
        )

    return videojuego


# POST: crear videojuego
@app.post("/videojuegos")
def crear_videojuego(videojuego: Videojuego):
    return ejecutar_sql(
        """
        INSERT INTO videojuegos
        (titulo, plataforma, genero, anio, precio, imagen_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
        """,
        (
            videojuego.titulo,
            videojuego.plataforma,
            videojuego.genero,
            videojuego.anio,
            videojuego.precio,
            videojuego.imagen_url
        ),
        fetch="one"
    )


# PUT: actualizar videojuego
@app.put("/videojuegos/{id}")
def actualizar_videojuego(id: int, videojuego: Videojuego):
    actualizado = ejecutar_sql(
        """
        UPDATE videojuegos
        SET titulo = %s,
            plataforma = %s,
            genero = %s,
            anio = %s,
            precio = %s,
            imagen_url = %s
        WHERE id = %s
        RETURNING *
        """,
        (
            videojuego.titulo,
            videojuego.plataforma,
            videojuego.genero,
            videojuego.anio,
            videojuego.precio,
            videojuego.imagen_url,
            id
        ),
        fetch="one"
    )

    if actualizado is None:
        raise HTTPException(
            status_code=404,
            detail="Videojuego no encontrado"
        )

    return actualizado


# DELETE: eliminar videojuego
@app.delete("/videojuegos/{id}")
def eliminar_videojuego(id: int):
    eliminado = ejecutar_sql(
        "DELETE FROM videojuegos WHERE id = %s RETURNING id",
        (id,),
        fetch="one"
    )

    if eliminado is None:
        raise HTTPException(
            status_code=404,
            detail="Videojuego no encontrado"
        )

    return {"mensaje": "Videojuego eliminado correctamente"}

