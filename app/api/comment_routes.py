from fastapi import APIRouter
from app.models.comment_model import CommentCreate
from app.services.comment_service import crear_comentario, obtener_comentarios, eliminar_comentario

router = APIRouter()

@router.post("/")
def agregar_comentario(data: CommentCreate):
    comentario = crear_comentario(data)
    comentario["id"] = str(comentario["_id"])
    del comentario["_id"]
    return comentario

@router.get("/{id_publicacion}")
def listar_comentarios(id_publicacion: str):
    comentarios = obtener_comentarios(id_publicacion)
    for c in comentarios:
        c["id"] = str(c["_id"])
        del c["_id"]
    return comentarios

@router.delete("/{id}")
def borrar_comentario(id: str, id_usuario: str):
    ok = eliminar_comentario(id, id_usuario)
    return {"eliminado": ok}
