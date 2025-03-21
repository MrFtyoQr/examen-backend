from pymongo import MongoClient

# 🔧 Sustituye por tu URI real
MONGO_URI = "mongodb+srv://quintanarealjqr:ZzWt8qAgQ8fp6uYX@utaweb.bk93x.mongodb.net/?retryWrites=true&w=majority&appName=utaweb"

client = MongoClient(MONGO_URI)
db = client["red_social_db"]  # Puedes cambiar el nombre de la BD si gustas
