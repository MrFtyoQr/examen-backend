from fastapi import FastAPI
from app.api import auth_routes
from app.api import post_routes
from app.api import comment_routes

app = FastAPI()

# Rutas agrupadas
app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticación"])
app.include_router(post_routes.router, prefix="/posts", tags=["Publicaciones"])
app.include_router(comment_routes.router, prefix="/comments", tags=["Comentarios"])

@app.get("/")
def index():
    return {"mensaje": "¡Bienvenido a la red social FastAPI 🚀!"}
