from bson import ObjectId
from app.database.connection import db
from app.database.gridfs_handler import guardar_archivo

posts = db["publicaciones"]

def crear_post(data, archivo_id=None):
    post = {
        "titulo": data.titulo,
        "descripcion": data.descripcion,
        "carrera": data.carrera,
        "id_usuario": data.id_usuario,
        "archivo_id": archivo_id
    }
    result = posts.insert_one(post)
    post["_id"] = result.inserted_id
    return post

def obtener_posts():
    return list(posts.find())

def obtener_post(id: str):
    return posts.find_one({"_id": ObjectId(id)})

def actualizar_post(id: str, user_id: str, data):
    filtro = {"_id": ObjectId(id), "id_usuario": user_id}
    actualizacion = {
        "$set": {
            "titulo": data.titulo,
            "descripcion": data.descripcion,
            "carrera": data.carrera
        }
    }
    resultado = posts.update_one(filtro, actualizacion)
    return resultado.modified_count > 0


def eliminar_post(id: str, user_id: str):
    resultado = posts.delete_one({"_id": ObjectId(id), "id_usuario": user_id})
    return resultado.deleted_count > 0
