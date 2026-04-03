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

        client_id = int(input("ID du client : ").strip())
        total_amount = input("Montant total : ").strip()
        amount_due = input("Montant restant dû : ").strip()
        is_signed_input = input("Contrat signé ? (oui/non) : ").strip().lower()

        is_signed = is_signed_input == "oui"

        contract = contract_service.create_contract(
            current_user=current_user,
            client_id=client_id,
            total_amount=total_amount,
            amount_due=amount_due,
            is_signed=is_signed,
        )

        print("\nContrat créé avec succès.")
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
