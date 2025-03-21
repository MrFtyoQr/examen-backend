from pydantic import BaseModel
from typing import Optional

class CommentCreate(BaseModel):
    id_publicacion: str  # Relacionado con la publicación
    id_usuario: str  # Usuario que comenta
    contenido: str  # Texto del comentario

class CommentResponse(BaseModel):
    id: str
    id_publicacion: str
    id_usuario: str
    contenido: str
