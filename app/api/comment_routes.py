from fastapi import APIRouter, Form
from app.models.comment_model import CommentCreate
from app.services.comment_service import crear_comentario  # <- usar crear_comentario
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/")
async def publicar_comentario(
    id_publicacion: str = Form(...),
    id_usuario: str = Form(...),
    contenido: str = Form(...)
):
    comentario = CommentCreate(
        id_publicacion=id_publicacion,
        id_usuario=id_usuario,
        contenido=contenido
    )
    crear_comentario(comentario)  # <- importante: usar await
    return RedirectResponse(url="/", status_code=303)
