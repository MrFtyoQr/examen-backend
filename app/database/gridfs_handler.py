import gridfs
from bson import ObjectId
from io import BytesIO
from app.database.connection import db

fs = gridfs.GridFS(db)

ALLOWED_CONTENT_TYPES = ["application/pdf", "image/jpeg", "video/mp4"]

def guardar_archivo(file) -> str:
    contenido = file.file.read()
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError("Tipo de archivo no permitido")
    archivo_id = fs.put(contenido, filename=file.filename, content_type=file.content_type)
    return str(archivo_id)

def obtener_archivo(archivo_id: str):
    archivo = fs.get(ObjectId(archivo_id))  # GridOut object
    return archivo, archivo.content_type, archivo.filename

"""
def obtener_archivo(archivo_id: str):
    archivo = fs.get(ObjectId(archivo_id))
    contenido = archivo.read()
    return BytesIO(contenido), archivo.content_type, archivo.filename

"""
