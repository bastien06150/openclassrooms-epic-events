import sentry_sdk
from app.models import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.security import hash_password
from app.permissions import require_management


class EmployeeService:
    def __init__(self, session):
        self.employee_repository = EmployeeRepository(session)

    def create_employee(
        self,
        current_user,
        employee_number: str,
        full_name: str,
        email: str,
        password: str,
        department_id: int,
    ):
        require_management(current_user)

        if not employee_number.strip():
            raise ValueError("Le numéro employé est obligatoire.")
        if not full_name.strip():
            raise ValueError("Le nom complet est obligatoire.")
        if not email.strip():
            raise ValueError("L'email est obligatoire.")
        if not password.strip():
            raise ValueError("Le mot de passe est obligatoire.")

        if self.employee_repository.get_by_email(email):
            raise ValueError("Un collaborateur avec cet email existe déjà.")

        if self.employee_repository.get_by_employee_number(employee_number):
            raise ValueError("Un collaborateur avec ce numéro existe déjà.")

        employee = Employee(
            employee_number=employee_number,
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            department_id=department_id,
        )

        created_employee = self.employee_repository.create(employee)

        sentry_sdk.capture_message(
            f"Collaborateur créé : {created_employee.email}", level="info"
        )

        return created_employee

    def update_employee(
        self,
        current_user,
        employee_id: int,
        full_name: str | None = None,
        email: str | None = None,
        department_id: int | None = None,
        password: str | None = None,
    ):
        require_management(current_user)

        employee = self.employee_repository.get_by_id(employee_id)
        if employee is None:
            raise ValueError("Collaborateur introuvable.")

        if full_name is not None:
            if not full_name.strip():
                raise ValueError("Le nom complet ne peut pas être vide.")
            employee.full_name = full_name

        if email is not None:
            if not email.strip():
                raise ValueError("L'email ne peut pas être vide.")
            existing = self.employee_repository.get_by_email(email)
            if existing and existing.id != employee.id:
                raise ValueError("Cet email est déjà utilisé.")
            employee.email = email

        if department_id is not None:
            employee.department_id = department_id

        if password is not None:
            if not password.strip():
                raise ValueError("Le mot de passe ne peut pas être vide.")
            employee.password_hash = hash_password(password)

        updated_employee = self.employee_repository.update(employee)

        sentry_sdk.capture_message(
            f"Collaborateur modifié : {updated_employee.email}", level="info"
        )

        return updated_employee

    def delete_employee(self, current_user, employee_id: int):
        require_management(current_user)

        employee = self.employee_repository.get_by_id(employee_id)
        if employee is None:
            raise ValueError("Collaborateur introuvable.")

        self.employee_repository.delete(employee)
