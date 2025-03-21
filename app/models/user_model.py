from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    nombre: str
    correo: EmailStr
    contraseña: str
    foto: str = ""
    carrera: str

class UserLogin(BaseModel):
    correo: EmailStr
    contraseña: str
