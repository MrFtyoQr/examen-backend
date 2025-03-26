from bson import ObjectId
from app.database.connection import db

reactions = db.reactions
users = db.users

def agregar_reaccion(data):
    try:
        usuario_existe = users.find_one({"_id": ObjectId(data.id_usuario)})
        if not usuario_existe:
            return {"error": "El usuario no existe"}, 400

        reaccion = {
            "id_publicacion": ObjectId(data.id_publicacion),
            "id_usuario": ObjectId(data.id_usuario),
            "tipo": data.tipo
        }
        result = reactions.insert_one(reaccion)

        reaccion["_id"] = str(result.inserted_id)  # Convertir ObjectId a string
        return reaccion
    except Exception as e:
        return {"error": str(e)}, 500


def obtener_reacciones(id_publicacion: str):
    reacciones = reactions.aggregate([
        {"$match": {"id_publicacion": ObjectId(id_publicacion)}},
        {"$group": {"_id": "$tipo", "count": {"$sum": 1}}}
    ])
    return {r["_id"]: r["count"] for r in reacciones}

def eliminar_reaccion(id_reaccion: str, id_usuario: str):
    print(f"Intentando eliminar reacción con id: {id_reaccion} y id_usuario: {id_usuario}")  # 🔍 Debug

    filtro = {
        "_id": ObjectId(id_reaccion),  # Convertir ID de la reacción
        "id_usuario": ObjectId(id_usuario)  # Convertir ID del usuario
    }

    print(f"Filtro usado en MongoDB para eliminar: {filtro}")  # 🔍 Debug

    resultado = reactions.delete_one(filtro)
    
    print(f"Resultado de eliminación: {resultado.deleted_count}")  # 🔍 Debug

    return resultado.deleted_count > 0
