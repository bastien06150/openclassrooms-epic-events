from app.database import engine, Base
from app.models import Department, Employee, Client, Contract, Event

Base.metadata.create_all(bind=engine)

print("Tables créées avec succès.")
