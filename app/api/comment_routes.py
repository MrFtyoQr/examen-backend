from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models.comment_model import CommentCreate
from app.services.comment_service import crear_comentario, obtener_comentarios, eliminar_comentario

router = APIRouter()

@router.post("/")
def agregar_comentario(data: CommentCreate):
    # Validar que los IDs sean ObjectId válidos antes de usarlos
    if not ObjectId.is_valid(data.id_usuario):
        raise HTTPException(status_code=400, detail="ID de usuario no válido")
    
    if not ObjectId.is_valid(data.id_publicacion):
        raise HTTPException(status_code=400, detail="ID de publicación no válido")

    comentario = crear_comentario(data)

    if isinstance(comentario, tuple):  # Si hubo un error (mensaje, código HTTP)
        raise HTTPException(status_code=comentario[1], detail=comentario[0]["error"])

    # Convertir `_id` a `id` si está presente
    if comentario and isinstance(comentario, dict) and "_id" in comentario:
        comentario["id"] = str(comentario["_id"])
        comentario["id_usuario"] = str(comentario["id_usuario"])
        comentario["id_publicacion"] = str(comentario["id_publicacion"])
        del comentario["_id"]

    return comentario


@router.get("/{id_publicacion}")
def listar_comentarios(id_publicacion: str):
    # Validar el ObjectId antes de la consulta
    if not ObjectId.is_valid(id_publicacion):
        raise HTTPException(status_code=400, detail="ID de publicación no válido")

    comentarios = obtener_comentarios(id_publicacion)

    # Convertir los ObjectId en strings para evitar errores de serialización
    for comentario in comentarios:
        if "_id" in comentario:
            comentario["id"] = str(comentario["_id"])
            del comentario["_id"]
        
        if "id_usuario" in comentario:
            comentario["id_usuario"] = str(comentario["id_usuario"])
        
        if "id_publicacion" in comentario:
            comentario["id_publicacion"] = str(comentario["id_publicacion"])

    return comentarios


@router.delete("/{id}")
def borrar_comentario(id: str, id_usuario: str):
    # Validar que los IDs sean ObjectId válidos antes de usarlos
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de comentario no válido")
    
    if not ObjectId.is_valid(id_usuario):
        raise HTTPException(status_code=400, detail="ID de usuario no válido")

    ok = eliminar_comentario(id, id_usuario)

    if not ok:
        raise HTTPException(status_code=404, detail="Comentario no encontrado o no tienes permiso para eliminarlo")

    return {"eliminado": True}
