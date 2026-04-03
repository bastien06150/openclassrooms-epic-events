from app.database import SessionLocal
from app.services.auth_service import AuthService


def main():
    session = SessionLocal()

    try:
        auth_service = AuthService(session)

        print("1. Login")
        print("2. Utilisateur courant")
        print("3. Logout")
        choice = input("Choix : ").strip()

        if choice == "1":
            email = input("Email : ").strip()
            password = input("Mot de passe : ").strip()

            if auth_service.login(email, password):
                print("Connexion réussie. Jeton enregistré.")
            else:
                print("Identifiants invalides.")

        elif choice == "2":
            employee = auth_service.get_current_user()
            if employee:
                print(f"Utilisateur courant : {employee.full_name}")
                print(f"Département : {employee.department.name}")
            else:
                print("Aucun utilisateur connecté ou jeton expiré.")

        elif choice == "3":
            auth_service.logout()
            print("Déconnexion effectuée.")

        else:
            print("Choix invalide.")

    finally:
        session.close()


if __name__ == "__main__":
    main()
