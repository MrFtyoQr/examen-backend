from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models.reaction_model import ReactionCreate
from app.services.reaction_service import agregar_reaccion, obtener_reacciones, eliminar_reaccion

router = APIRouter()

@router.post("/")
def reaccionar(data: ReactionCreate):
    # Validar que los IDs sean ObjectId válidos antes de usarlos
    if not ObjectId.is_valid(data.id_usuario):
        raise HTTPException(status_code=400, detail="ID de usuario no válido")
    
    if not ObjectId.is_valid(data.id_publicacion):
        raise HTTPException(status_code=400, detail="ID de publicación no válido")

    reaccion = agregar_reaccion(data)

    if isinstance(reaccion, tuple):
        raise HTTPException(status_code=reaccion[1], detail=reaccion[0]["error"])

    # Convertir todos los ObjectId a string antes de devolver la respuesta
    if isinstance(reaccion, dict):  # Asegurar que es un diccionario antes de modificarlo
        reaccion["id"] = str(reaccion.get("_id", ""))
        reaccion["id_usuario"] = str(reaccion.get("id_usuario", ""))
        reaccion["id_publicacion"] = str(reaccion.get("id_publicacion", ""))
        reaccion.pop("_id", None)  # Eliminar _id después de la conversión

    return reaccion


@router.get("/{id_publicacion}")
def listar_reacciones(id_publicacion: str):
    if not ObjectId.is_valid(id_publicacion):
        raise HTTPException(status_code=400, detail="ID de publicación no válido")

    print(f"Buscando reacciones con id_publicacion: {id_publicacion}")  # 🔍 Debug

    reacciones = obtener_reacciones(id_publicacion)

    print(f"Reacciones obtenidas: {reacciones}")  # 🔍 Debug

    for reaccion in reacciones:
        if isinstance(reaccion, dict):
            reaccion["id"] = str(reaccion.get("_id", ""))
            reaccion["id_usuario"] = str(reaccion.get("id_usuario", ""))
            reaccion["id_publicacion"] = str(reaccion.get("id_publicacion", ""))
            reaccion.pop("_id", None)

    return reacciones


@router.delete("/{id_reaccion}")
def borrar_reaccion(id_reaccion: str, id_usuario: str):
    if not ObjectId.is_valid(id_reaccion):
        raise HTTPException(status_code=400, detail="ID de reacción no válido")
    
    if not ObjectId.is_valid(id_usuario):
        raise HTTPException(status_code=400, detail="ID de usuario no válido")

    print(f"Intentando eliminar reacción con id_reaccion: {id_reaccion} y id_usuario: {id_usuario}")  # 🔍 Debug

    ok = eliminar_reaccion(id_reaccion, id_usuario)

    if not ok:
        raise HTTPException(status_code=404, detail="Reacción no encontrada o no tienes permiso para eliminarla")

    return {"eliminado": True}

