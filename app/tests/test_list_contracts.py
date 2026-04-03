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

        contracts = contract_service.list_contracts(current_user)

        print(f"Utilisateur connecté : {current_user.full_name}")
        print(f"Département : {current_user.department.name}")
        print(f"Nombre de contrats : {len(contracts)}\n")

        for contract in contracts:
            print(
                f"ID: {contract.id} | "
                f"Client ID: {contract.client_id} | "
                f"Montant total: {contract.total_amount} | "
                f"Reste à payer: {contract.amount_due} | "
                f"Signé: {contract.is_signed}"
            )

    except PermissionError as error:
        print(f"Accès refusé : {error}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
