from fastapi import APIRouter, UploadFile, File, Form
from app.models.post_model import PostCreate
from app.services.post_service import crear_post, obtener_posts, obtener_post, actualizar_post, eliminar_post
from app.database.gridfs_handler import guardar_archivo, obtener_archivo
from fastapi.responses import StreamingResponse
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def crear_publicacion(
    titulo: str = Form(...),
    descripcion: str = Form(...),
    carrera: str = Form(...),
    id_usuario: str = Form(...),
    archivo: UploadFile = File(None)
):
    archivo_id = None
    if archivo:
        archivo_id = guardar_archivo(archivo)
    
    data = PostCreate(
        titulo=titulo,
        descripcion=descripcion,
        carrera=carrera,
        id_usuario=id_usuario
    )

    post = crear_post(data, archivo_id)
    post["id"] = str(post["_id"])
    del post["_id"]
    return post

@router.get("/")
def listar_publicaciones():
    posts = obtener_posts()
    for p in posts:
        p["id"] = str(p["_id"])
        del p["_id"]
    return posts

@router.get("/{id}")
def ver_publicacion(id: str):
    post = obtener_post(id)
    if post:
        post["id"] = str(post["_id"])
        del post["_id"]
        return post
    return {"error": "Publicación no encontrada"}

@router.get("/archivo/{archivo_id}")
def descargar_archivo(archivo_id: str):
    contenido, content_type, nombre = obtener_archivo(archivo_id)
    return StreamingResponse(content=contenido, media_type=content_type, headers={"Content-Disposition": f"attachment; filename={nombre}"})

@router.put("/{id}")
def editar_publicacion(id: str, data: PostCreate):
    ok = actualizar_post(id, data.id_usuario, data)
    return {"actualizado": ok}

@router.delete("/{id}")
def eliminar_publicacion(id: str, id_usuario: str):
    ok = eliminar_post(id, id_usuario)
    return {"eliminado": ok}
