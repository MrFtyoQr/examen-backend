from tempfile import template
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.models.user_model import UserRegister, UserLogin
from app.services.auth_service import register_user, login_user
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/register")
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(user: UserLogin):
    result = login_user(user)
    if result["success"]:
        return JSONResponse(content={
            "success": True,
            "message": result["message"],
            "user_id": result["user_data"]["id"]  # ✅ Corregido aquí
        })
    return JSONResponse(content={"success": False, "message": result["message"]}, status_code=401)

@router.post("/register")
async def register_post(request: Request):
    form = await request.form()
    user = UserRegister(
        nombre=form["nombre"],
        correo=form["correo"],
        contraseña=form["contraseña"],
        carrera=form["carrera"],
        foto=""  # Si no tienes campo para foto, ponlo vacío
    )
    result = register_user(user)
    if result["success"]:
        return RedirectResponse(url="/auth/login", status_code=303)
    return templates.TemplateResponse("register.html", {"request": request, "error": result["message"]})

