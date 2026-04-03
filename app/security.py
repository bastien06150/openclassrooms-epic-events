from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Retourne une version hachée et salée du mot de passe."""
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Vérifie qu'un mot de passe correspond au hash stocké."""
    try:
        return password_hasher.verify(hashed_password, password)
    except (VerifyMismatchError, InvalidHash):
        return False
