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

        events = event_service.list_events(current_user)

        print(f"Utilisateur connecté : {current_user.full_name}")
        print(f"Département : {current_user.department.name}")
        print(f"Nombre d'événements : {len(events)}\n")

        for event in events:
            print(
                f"ID: {event.id} | "
                f"Nom: {event.name} | "
                f"Contract ID: {event.contract_id} | "
                f"Support ID: {event.support_contact_id} | "
                f"Lieu: {event.location} | "
                f"Participants: {event.attendees}"
            )

    except PermissionError as error:
        print(f"Accès refusé : {error}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
