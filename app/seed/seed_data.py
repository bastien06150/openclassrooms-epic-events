from app.database import SessionLocal
from app.models import Department, Employee
from app.security import hash_password


def seed_database():
    session = SessionLocal()

    try:
        # Vérifie si les départements existent déjà
        existing_department = session.query(Department).first()
        if existing_department:
            print("La base contient déjà des données de seed.")
            return

        # Création des départements
        management = Department(name="management")
        sales = Department(name="sales")
        support = Department(name="support")

        session.add_all([management, sales, support])
        session.commit()

        # Création des employés
        employee_1 = Employee(
            employee_number="EMP001",
            full_name="Alice Martin",
            email="alice@epicevents.com",
            password_hash=hash_password("Admin123!"),
            department_id=management.id,
        )

        employee_2 = Employee(
            employee_number="EMP002",
            full_name="Bob Durand",
            email="bob@epicevents.com",
            password_hash=hash_password("Sales123!"),
            department_id=sales.id,
        )

        employee_3 = Employee(
            employee_number="EMP003",
            full_name="Claire Petit",
            email="claire@epicevents.com",
            password_hash=hash_password("Support123!"),
            department_id=support.id,
        )

        session.add_all([employee_1, employee_2, employee_3])
        session.commit()

        print("Départements et employés créés avec succès.")

    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
