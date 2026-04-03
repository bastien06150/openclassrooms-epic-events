from app.database import SessionLocal
from app.services.auth_service import AuthService
from app.permissions import is_management, is_sales, is_support


def main():
    session = SessionLocal()

    try:
        auth_service = AuthService(session)
        employee = auth_service.get_current_user()

        if employee is None:
            print("Aucun utilisateur connecté.")
            return

        print(f"Utilisateur : {employee.full_name}")
        print(f"Département : {employee.department.name}")
        print(f"is_management: {is_management(employee)}")
        print(f"is_sales: {is_sales(employee)}")
        print(f"is_support: {is_support(employee)}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
