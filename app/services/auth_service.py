from app.database.connection import db
from app.models.user_model import UserRegister, UserLogin
from app.core.security import hash_password, verify_password

users_collection = db["users"]

def register_user(user: UserRegister) -> dict:
    if users_collection.find_one({"correo": user.correo}):
        return {"success": False, "message": "El correo ya está registrado."}

    hashed_pwd = hash_password(user.contraseña)
    new_user = {
        "nombre": user.nombre,
        "correo": user.correo,
        "contraseña": hashed_pwd,
        "foto": user.foto,
        "carrera": user.carrera
    }

    result = users_collection.insert_one(new_user)
    return {
        "success": True,
        "message": "Usuario registrado correctamente.",
        "user_id": str(result.inserted_id)
    }

def login_user(user: UserLogin) -> dict:
    existing_user = users_collection.find_one({"correo": user.correo})
    if not existing_user:
        return {"success": False, "message": "Correo no encontrado"}

    if not verify_password(user.contraseña, existing_user["contraseña"]):
        return {"success": False, "message": "Contraseña incorrecta"}

    return {
        "success": True,
        "message": "Inicio de sesión exitoso",
        "user_data": {
            "id": str(existing_user["_id"]),
            "nombre": existing_user["nombre"],
            "correo": existing_user["correo"],
            "foto": existing_user.get("foto", ""),
            "carrera": existing_user.get("carrera", "")
        }
    }
