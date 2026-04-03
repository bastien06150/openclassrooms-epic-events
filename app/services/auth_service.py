from app.auth.jwt_handler import create_access_token, decode_access_token
from app.auth.token_storage import delete_token, load_token, save_token
from app.repositories.employee_repository import EmployeeRepository
from app.security import verify_password


class AuthService:
    def __init__(self, session):
        self.employee_repository = EmployeeRepository(session)

    def authenticate(self, email: str, password: str):
        employee = self.employee_repository.get_by_email(email)

        if employee is None:
            return None

        if not verify_password(password, employee.password_hash):
            return None

        return employee

    def login(self, email: str, password: str) -> bool:
        employee = self.authenticate(email, password)
        if employee is None:
            return False

        token = create_access_token(employee)
        save_token(token)
        return True

    def logout(self) -> None:
        delete_token()

    def get_current_user(self):
        token = load_token()
        if not token:
            return None

        payload = decode_access_token(token)
        if not payload:
            return None

        employee_id = payload.get("employee_id")
        if employee_id is None:
            return None

        return self.employee_repository.get_by_id(employee_id)
