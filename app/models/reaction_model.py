from pydantic import BaseModel
from typing import Literal

class ReactionCreate(BaseModel):
    id_publicacion: str  # Publicación a la que se reacciona
    id_usuario: str  # Usuario que reacciona
    tipo: Literal["like", "love", "fire", "laugh", "angry"]  # Tipos de reacciones

class ReactionResponse(BaseModel):
    id: str
    id_publicacion: str
    id_usuario: str
    tipo: str
