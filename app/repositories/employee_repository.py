from app.models import Employee


class EmployeeRepository:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, employee_id: int):
        return self.session.query(Employee).filter_by(id=employee_id).first()

    def get_by_email(self, email: str):
        return self.session.query(Employee).filter_by(email=email).first()

    def get_by_employee_number(self, employee_number: str):
        return (
            self.session.query(Employee)
            .filter_by(employee_number=employee_number)
            .first()
        )

    def create(self, employee: Employee):
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def update(self, employee: Employee):
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def delete(self, employee):
        self.session.delete(employee)
        self.session.commit()
