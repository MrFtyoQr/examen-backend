from app.database.connection import db
from app.models.comment_model import CommentCreate
from bson import ObjectId

comentarios = db["comentarios"]

def crear_comentario(data: CommentCreate):
    comentario = {
        "id_publicacion": ObjectId(data.id_publicacion),
        "id_usuario": ObjectId(data.id_usuario),
        "contenido": data.contenido
    }
    comentarios.insert_one(comentario)

def obtener_comentarios(id_publicacion: str):
    comentarios_encontrados = comentarios.find({"id_publicacion": ObjectId(id_publicacion)})
    resultado = []
    for c in comentarios_encontrados:
        resultado.append({
            "usuario": str(c["id_usuario"]),
            "contenido": c["contenido"]
        })
    return resultado
