def is_management(employee) -> bool:
    return employee is not None and employee.department.name == "management"


def is_sales(employee) -> bool:
    return employee is not None and employee.department.name == "sales"


def is_support(employee) -> bool:
    return employee is not None and employee.department.name == "support"


def require_management(employee) -> None:
    if not is_management(employee):
        raise PermissionError("Accès réservé au département management.")


def require_sales(employee) -> None:
    if not is_sales(employee):
        raise PermissionError("Accès réservé au département commercial.")


def require_support(employee) -> None:
    if not is_support(employee):
        raise PermissionError("Accès réservé au département support.")


def require_authenticated_user(employee) -> None:
    if employee is None:
        raise PermissionError("Vous devez être authentifié pour accéder aux données.")
