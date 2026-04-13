import sentry_sdk
from app.models import Client
from app.permissions import require_sales, require_authenticated_user
from app.repositories.client_repository import ClientRepository


class ClientService:
    def __init__(self, session):
        self.client_repository = ClientRepository(session)

    def create_client(
        self,
        current_user,
        full_name: str,
        email: str,
        phone: str,
        company_name: str,
    ):
        """
        Crée un nouveau client.

        Args:
            current_user: utilisateur connecté
            full_name: nom complet du client
            email: email du client
            phone: téléphone du client
            company_name: nom de l'entreprise

        """

        # 1. Vérifier que l'utilisateur connecté est bien sales
        require_sales(current_user)

        # 2. Créer le client en l'associant automatiquement au commercial connecté
        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            sales_contact_id=current_user.id,
        )

        created_client = self.client_repository.create(client)

        sentry_sdk.capture_message(
            f"Client créé : {created_client.email}", level="info"
        )

        return created_client

    def list_clients(self, current_user):
        """
        Retourne la liste de tous les clients.

        Args:
            current_user: utilisateur connecté.
        """

        require_authenticated_user(current_user)
        return self.client_repository.get_all()

    def delete_client(self, current_user, client_id: int):
        """
        Supprime un client appartenant au commercial connecté.

        Args:
            current_user: utilisateur connecté. Doit appartenir au département sales.
            client_id: identifiant du client à supprimer.
        """

        require_sales(current_user)

        client = self.client_repository.get_by_id(client_id)
        if client is None:
            raise ValueError("Client introuvable")

        if client.sales_contact_id != current_user.id:
            raise PermissionError("Vous ne pouvez supprimer que vos propres clients. ")

        self.client_repository.delete(client)
