from app.database import SessionLocal
from app.services.auth_service import AuthService
from app.services.contract_service import ContractService


def main():
    session = SessionLocal()

    try:
        auth_service = AuthService(session)
        contract_service = ContractService(session)

        current_user = auth_service.get_current_user()

        if current_user is None:
            print("Aucun utilisateur connecté.")
            return

        print(f"Utilisateur connecté : {current_user.full_name}")
        print(f"Département : {current_user.department.name}")

        contract_id = int(input("ID du contrat à modifier : ").strip())

        client_id_input = input(
            "Nouveau client_id (laisser vide si inchangé) : "
        ).strip()
        total_amount_input = input(
            "Nouveau montant total (laisser vide si inchangé) : "
        ).strip()
        amount_due_input = input(
            "Nouveau montant restant dû (laisser vide si inchangé) : "
        ).strip()
        is_signed_input = (
            input("Nouveau statut signé ? (oui/non/vide) : ").strip().lower()
        )

        client_id = int(client_id_input) if client_id_input else None
        total_amount = total_amount_input if total_amount_input else None
        amount_due = amount_due_input if amount_due_input else None

        if is_signed_input == "oui":
            is_signed = True
        elif is_signed_input == "non":
            is_signed = False
        else:
            is_signed = None

        contract = contract_service.update_contract(
            current_user=current_user,
            contract_id=contract_id,
            client_id=client_id,
            total_amount=total_amount,
            amount_due=amount_due,
            is_signed=is_signed,
        )

        print("\nContrat modifié avec succès.")
        print(f"ID : {contract.id}")
        print(f"Client ID : {contract.client_id}")
        print(f"Montant total : {contract.total_amount}")
        print(f"Montant restant dû : {contract.amount_due}")
        print(f"Signé : {contract.is_signed}")

    except (PermissionError, ValueError) as error:
        print(f"\nErreur : {error}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
