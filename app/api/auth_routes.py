from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from app.models.user_model import UserRegister, UserLogin
from app.services.auth_service import register_user, login_user

router = APIRouter()

@router.post("/register")
async def register(
    nombre: str = Form(...),
    correo: str = Form(...),
    contraseña: str = Form(...),
    carrera: str = Form(...),
    foto: str = Form("")
):
    user = UserRegister(
        nombre=nombre,
        correo=correo,
        contraseña=contraseña,
        carrera=carrera,
        foto=foto
    )
    result = register_user(user)
    if result["success"]:
        return RedirectResponse(url="/auth/login", status_code=303)
    return {"error": result["message"]}

@router.post("/login")
async def login(
    request: Request,
    correo: str = Form(...),
    contraseña: str = Form(...)
):
    user = UserLogin(correo=correo, contraseña=contraseña)
    result = login_user(user)
    if result["success"]:
        return RedirectResponse(url="/", status_code=303)
    return {"error": result["message"]}
