from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from app.api import auth_routes, post_routes, comment_routes, reaction_routes
from app.database.gridfs_handler import obtener_archivo
from app.services.post_service import obtener_posts
from app.services.comment_service import obtener_comentarios
from app.services.reaction_service import obtener_reacciones
from io import BytesIO

app = FastAPI()

# Configuración de plantillas y archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Rutas agrupadas
app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticación"])
app.include_router(post_routes.router, prefix="/posts", tags=["Publicaciones"])
app.include_router(comment_routes.router, prefix="/comments", tags=["Comentarios"])
app.include_router(reaction_routes.router, prefix="/reactions", tags=["Reacciones"])

@app.get("/")
def index(request: Request):
    posts = obtener_posts()  # Obtener publicaciones desde la base de datos
    for post in posts:
        post["id"] = str(post["_id"])
        if "archivo_id" in post:
            post["archivo_id"] = str(post["archivo_id"])
        # Obtener comentarios y reacciones para cada publicación
        post["comentarios"] = obtener_comentarios(post["id"])
        post["reacciones"] = obtener_reacciones(post["id"])
    return templates.TemplateResponse("feed.html", {"request": request, "posts": posts})

@app.get("/posts/archivo/{archivo_id}")
def descargar_archivo(archivo_id: str):
    contenido, content_type, nombre = obtener_archivo(archivo_id)

    # ✅ Si contenido es tipo bytes
    if isinstance(contenido, bytes):
        contenido = BytesIO(contenido)

    return StreamingResponse(
        content=contenido,
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={nombre}"}
    )