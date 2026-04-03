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

        event_id = int(input("ID de l'événement à modifier : ").strip())

        name = input("Nouveau nom (vide si inchangé) : ").strip()
        contract_id_input = input("Nouveau contract_id (vide si inchangé) : ").strip()
        support_contact_input = input(
            "Nouveau support_contact_id (vide si inchangé) : "
        ).strip()
        event_start_input = input(
            "Nouvelle date début YYYY-MM-DD HH:MM (vide si inchangé) : "
        ).strip()
        event_end_input = input(
            "Nouvelle date fin YYYY-MM-DD HH:MM (vide si inchangé) : "
        ).strip()
        location = input("Nouveau lieu (vide si inchangé) : ").strip()
        attendees_input = input(
            "Nouveau nombre de participants (vide si inchangé) : "
        ).strip()
        notes = input("Nouvelles notes (vide si inchangé) : ").strip()

        contract_id = int(contract_id_input) if contract_id_input else None
        support_contact_id = (
            int(support_contact_input) if support_contact_input else None
        )
        event_start = (
            datetime.strptime(event_start_input, "%Y-%m-%d %H:%M")
            if event_start_input
            else None
        )
        event_end = (
            datetime.strptime(event_end_input, "%Y-%m-%d %H:%M")
            if event_end_input
            else None
        )
        attendees = int(attendees_input) if attendees_input else None

        event = event_service.update_event(
            current_user=current_user,
            event_id=event_id,
            name=name if name else None,
            contract_id=contract_id,
            support_contact_id=support_contact_id,
            event_start=event_start,
            event_end=event_end,
            location=location if location else None,
            attendees=attendees,
            notes=notes if notes else None,
        )

        print("\nÉvénement modifié avec succès.")
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
