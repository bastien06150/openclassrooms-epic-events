from app.database import SessionLocal
from app.services.auth_service import AuthService
from app.services.client_service import ClientService


def main():
    session = SessionLocal()

    try:
        auth_service = AuthService(session)
        client_service = ClientService(session)

        current_user = auth_service.get_current_user()

        if current_user is None:
            print("Aucun utilisateur connecté.")
            return

        print(f"Utilisateur connecté : {current_user.full_name}")
        print(f"Département : {current_user.department.name}")

        full_name = input("Nom complet du client : ").strip()
        email = input("Email du client : ").strip()
        phone = input("Téléphone du client : ").strip()
        company_name = input("Entreprise du client : ").strip()

        client = client_service.create_client(
            current_user=current_user,
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
        )

        print("\nClient créé avec succès.")
        print(f"ID : {client.id}")
        print(f"Nom : {client.full_name}")
        print(f"Entreprise : {client.company_name}")
        print(f"Commercial associé : {current_user.full_name}")

    except PermissionError as error:
        print(f"\nAccès refusé : {error}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
