from app.database import SessionLocal
from app.services.auth_service import AuthService
from app.services.employee_service import EmployeeService


def main():
    session = SessionLocal()

    try:
        auth_service = AuthService(session)
        employee_service = EmployeeService(session)

        current_user = auth_service.get_current_user()
        if current_user is None:
            print("Aucun utilisateur connecté.")
            return

        employee = employee_service.update_employee(
            current_user=current_user,
            employee_id=2,
            full_name="Bob Durand Modifié",
            department_id=2,
        )

        print(
            f"Collaborateur modifié : {employee.full_name}, département_id={employee.department_id}"
        )

    except (PermissionError, ValueError) as error:
        print(f"Erreur : {error}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
