# Catálogo de Videojuegos

## Descripción

Proyecto individual de desarrollo Full Stack con inteligencia artificial generativa.

La aplicación permite consultar, añadir, modificar y eliminar videojuegos de un catálogo almacenado en una base de datos.

## Tecnologías utilizadas

- Python
- FastAPI
- Supabase (PostgreSQL)
- pg8000
- React
- Tailwind CSS
- Lovable
- Render
- Postman
- Git y GitHub

## Funcionalidades

- Listar todos los videojuegos.
- Consultar un videojuego por ID.
- Añadir nuevos videojuegos.
- Modificar videojuegos existentes.
- Eliminar videojuegos.
- Buscar videojuegos por título.
- Gestionar errores de la API.

## Enlaces del proyecto

- Frontend: https://juegos-en-pesetas-no.lovable.app/
- Backend: https://catalogo-videojuegos-4ulc.onrender.com
- Documentación de la API: https://catalogo-videojuegos-4ulc.onrender.com/docs

## Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /videojuegos | Listar videojuegos |
| GET | /videojuegos/{id} | Obtener videojuego por ID |
| POST | /videojuegos | Añadir videojuego |
| PUT | /videojuegos/{id} | Modificar videojuego |
| DELETE | /videojuegos/{id} | Eliminar videojuego |

## Instalación en local

1. Clonar el repositorio.
2. Abrir el proyecto en Visual Studio Code.
3. Crear un entorno virtual:

   python -m venv .venv

4. Activar el entorno virtual en Windows:

   .venv\Scripts\Activate.ps1

5. Instalar las dependencias:

   python -m pip install -r requirements.txt

6. Crear un archivo .env siguiendo el ejemplo de .env.example e introducir la conexión a Supabase.

7. Ejecutar el servidor:

   python -m uvicorn main:app --reload

8. Acceder a la documentación:

   http://127.0.0.1:8000/docs

## Postman

El proyecto incluye el archivo postman_collection.json con las cinco peticiones CRUD para probar la API.

## Seguridad

La conexión a la base de datos se almacena en una variable de entorno. El archivo .env está excluido del repositorio mediante .gitignore.

## Desarrollo

El backend se ha desarrollado con FastAPI y el frontend se ha generado con Lovable utilizando inteligencia artificial generativa.