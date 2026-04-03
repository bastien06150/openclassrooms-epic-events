from datetime import datetime

from app.database import SessionLocal
from app.services.auth_service import AuthService
from app.services.event_service import EventService


def main():
    session = SessionLocal()

    try:
        auth_service = AuthService(session)
        event_service = EventService(session)

        current_user = auth_service.get_current_user()

        if current_user is None:
            print("Aucun utilisateur connecté.")
            return

        print(f"Utilisateur connecté : {current_user.full_name}")
        print(f"Département : {current_user.department.name}")

        name = input("Nom de l'événement : ").strip()
        contract_id = int(input("ID du contrat : ").strip())
        event_start_str = input("Date de début (YYYY-MM-DD HH:MM) : ").strip()
        event_end_str = input("Date de fin (YYYY-MM-DD HH:MM) : ").strip()
        location = input("Lieu : ").strip()
        attendees = int(input("Nombre de participants : ").strip())
        notes = input("Notes (optionnel) : ").strip()
        support_contact_input = input("ID du support (optionnel) : ").strip()

        event_start = datetime.strptime(event_start_str, "%Y-%m-%d %H:%M")
        event_end = datetime.strptime(event_end_str, "%Y-%m-%d %H:%M")
        support_contact_id = (
            int(support_contact_input) if support_contact_input else None
        )

        event = event_service.create_event(
            current_user=current_user,
            name=name,
            contract_id=contract_id,
            event_start=event_start,
            event_end=event_end,
            location=location,
            attendees=attendees,
            notes=notes if notes else None,
            support_contact_id=support_contact_id,
        )

        print("\nÉvénement créé avec succès.")
        print(f"ID : {event.id}")
        print(f"Nom : {event.name}")
        print(f"Contract ID : {event.contract_id}")
        print(f"Support ID : {event.support_contact_id}")
        print(f"Lieu : {event.location}")
        print(f"Participants : {event.attendees}")

    except (PermissionError, ValueError) as error:
        print(f"\nErreur : {error}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
