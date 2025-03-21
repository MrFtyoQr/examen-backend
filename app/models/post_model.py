from pydantic import BaseModel, Field
from typing import Optional

class PostCreate(BaseModel):
    titulo: str
    descripcion: str
    carrera: str  # Validaremos contra los enums
    id_usuario: str  # ID del usuario que hace la publicación

class PostResponse(BaseModel):
    id: str
    titulo: str
    descripcion: str
    archivo_id: Optional[str]
    carrera: str
    id_usuario: str
