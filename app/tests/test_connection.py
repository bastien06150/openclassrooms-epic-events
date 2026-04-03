from sqlalchemy import text
from app.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connexion réussie :", result.scalar())
except Exception as error:
    print("Erreur :", error)
