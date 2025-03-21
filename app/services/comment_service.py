from bson import ObjectId
from app.database.connection import db

comments = db["comentarios"]

def crear_comentario(data):
    comentario = {
        "id_publicacion": data.id_publicacion,
        "id_usuario": data.id_usuario,
        "contenido": data.contenido
    }
    result = comments.insert_one(comentario)
    comentario["_id"] = result.inserted_id
    return comentario

def obtener_comentarios(id_publicacion: str):
    return list(comments.find({"id_publicacion": id_publicacion}))

def eliminar_comentario(id: str, id_usuario: str):
    resultado = comments.delete_one({"_id": ObjectId(id), "id_usuario": id_usuario})
    return resultado.deleted_count > 0
