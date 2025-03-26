from bson import ObjectId
from app.database.connection import db

comments = db.comments
users = db.users

def crear_comentario(data):
    try:
        usuario_existe = users.find_one({"_id": ObjectId(data.id_usuario)})
        if not usuario_existe:
            return {"error": "El usuario no existe"}, 400

        comentario = {
            "id_publicacion": ObjectId(data.id_publicacion),
            "id_usuario": ObjectId(data.id_usuario),
            "contenido": data.contenido
        }
        result = comments.insert_one(comentario)

        comentario["_id"] = str(result.inserted_id)  # Convertir ObjectId a string antes de devolverlo
        return comentario
    except Exception as e:
        return {"error": str(e)}, 500


def obtener_comentarios(id_publicacion: str):
    comentarios = list(comments.find({"id_publicacion": ObjectId(id_publicacion)}))
    for comentario in comentarios:
        comentario["id"] = str(comentario["_id"])
        comentario["id_usuario"] = str(comentario["id_usuario"])
        comentario["id_publicacion"] = str(comentario["id_publicacion"])
    return comentarios

def eliminar_comentario(id: str, id_usuario: str):
    resultado = comments.delete_one({"_id": ObjectId(id), "id_usuario": id_usuario})
    return resultado.deleted_count > 0
