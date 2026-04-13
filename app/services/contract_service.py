import sentry_sdk
from app.repositories.contract_repository import ContractRepository
from app.permissions import require_management, require_authenticated_user
from app.models import Contract
from app.permissions import require_authenticated_user


class ContractService:
    def __init__(self, session):
        self.contract_repository = ContractRepository(session)

    def list_contracts(self, current_user):
        """
        Retourne la liste de tous les contrats.

        Args:
            current_user: utilisateur connecté.

        """
        require_authenticated_user(current_user)
        return self.contract_repository.get_all()

    def create_contract(
        self,
        current_user,
        client_id: int,
        total_amount,
        amount_due,
        is_signed: bool,
    ):
        """
        Crée un nouveau contrat.

        Args:
            current_user: utilisateur connecté. Doit appartenir au département management.
            client_id: identifiant du client lié au contrat.
            total_amount: montant total du contrat.
            amount_due: montant restant dû.
            is_signed: statut de signature du contrat.

        """

        require_management(current_user)

        if total_amount is None or float(total_amount) < 0:
            raise ValueError("Le montant total doit être positif ou nul.")
        if amount_due is None or float(amount_due) < 0:
            raise ValueError("Le montant restant doit être positif ou nul.")
        if float(amount_due) > float(total_amount):
            raise ValueError(
                "Le montant restant ne peut pas dépasser le montant total."
            )

        contract = Contract(
            client_id=client_id,
            total_amount=total_amount,
            amount_due=amount_due,
            is_signed=is_signed,
        )

        return self.contract_repository.create(contract)

    def update_contract(
        self,
        current_user,
        contract_id: int,
        client_id: int | None = None,
        total_amount=None,
        amount_due=None,
        is_signed: bool | None = None,
    ):
        """
        Met à jour un contrat existant.

        Args:
            current_user: utilisateur connecté. Doit appartenir au département management.
            contract_id: identifiant du contrat à modifier.
            client_id: nouvel identifiant client, optionnel.
            total_amount: nouveau montant total, optionnel.
            amount_due: nouveau montant restant dû, optionnel.
            is_signed: nouveau statut signé, optionnel.

        """
        require_management(current_user)

        contract = self.contract_repository.get_by_id(contract_id)
        if contract is None:
            raise ValueError("Contrat introuvable.")

        if client_id is not None:
            contract.client_id = client_id

        new_total = contract.total_amount if total_amount is None else total_amount
        new_due = contract.amount_due if amount_due is None else amount_due

        if float(new_total) < 0:
            raise ValueError("Le montant total doit être positif ou nul.")
        if float(new_due) < 0:
            raise ValueError("Le montant restant doit être positif ou nul.")
        if float(new_due) > float(new_total):
            raise ValueError(
                "Le montant restant ne peut pas dépasser le montant total."
            )

        contract.total_amount = new_total
        contract.amount_due = new_due

        was_signed = contract.is_signed

        if is_signed is not None:
            contract.is_signed = is_signed

        updated_contract = self.contract_repository.update(contract)

        if not was_signed and updated_contract.is_signed:
            sentry_sdk.capture_message(
                f"Contrat signé : ID {updated_contract.id}", level="info"
            )

        return updated_contract

    def delete_contract(self, current_user, contract_id: int):
        """
        Supprime un contrat.

        Args:
            current_user: utilisateur connecté. Doit appartenir au département management.
            contract_id: identifiant du contrat à supprimer.

        """
        require_management(current_user)

        contract = self.contract_repository.get_by_id(contract_id)
        if contract is None:
            raise ValueError("Contrat introuvable.")

        self.contract_repository.delete(contract)
