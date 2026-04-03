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

        clients = client_service.list_clients(current_user)

        print(f"Utilisateur connecté : {current_user.full_name}")
        print(f"Département : {current_user.department.name}")
        print(f"Nombre de clients : {len(clients)}\n")

        for client in clients:
            print(
                f"ID: {client.id} | "
                f"Nom: {client.full_name} | "
                f"Email: {client.email} | "
                f"Entreprise: {client.company_name} | "
                f"Commercial ID: {client.sales_contact_id}"
            )

    except PermissionError as error:
        print(f"Accès refusé : {error}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
