from app.permissions import require_authenticated_user
from app.repositories.event_repository import EventRepository
from app.models import Event
from app.permissions import require_sales
from app.repositories.contract_repository import ContractRepository


class EventService:
    def __init__(self, session):
        self.event_repository = EventRepository(session)
        self.contract_repository = ContractRepository(session)

    def list_events(self, current_user):
        """
        Retourne la liste de tous les événements.

        Args:
            current_user: utilisateur connecté.

        """
        require_authenticated_user(current_user)
        return self.event_repository.get_all()

    def create_event(
        self,
        current_user,
        name: str,
        contract_id: int,
        event_start,
        event_end,
        location: str,
        attendees: int,
        notes: str | None = None,
        support_contact_id: int | None = None,
    ):
        """
        Crée un nouvel événement.

        Args:
            current_user: utilisateur connecté. Doit appartenir au département sales.
            name: nom de l'événement.
            contract_id: identifiant du contrat lié à l'événement.
            event_start: date et heure de début.
            event_end: date et heure de fin.
            location: lieu de l'événement.
            attendees: nombre de participants.
            notes: notes complémentaires, optionnel.
            support_contact_id: identifiant du collaborateur support assigné, optionnel.

        """
        require_sales(current_user)

        if not name.strip():
            raise ValueError("Le nom de l'événement est obligatoire.")
        if not location.strip():
            raise ValueError("Le lieu est obligatoire.")
        if attendees < 0:
            raise ValueError("Le nombre de participants doit être positif ou nul.")
        if event_end <= event_start:
            raise ValueError("La date de fin doit être après la date de début.")

        contract = self.contract_repository.get_by_id(contract_id)
        if contract is None:
            raise ValueError("Contrat introuvable.")
        if not contract.is_signed:
            raise ValueError(
                "Impossible de créer un événement pour un contrat non signé."
            )

        event = Event(
            name=name,
            contract_id=contract_id,
            support_contact_id=support_contact_id,
            event_start=event_start,
            event_end=event_end,
            location=location,
            attendees=attendees,
            notes=notes,
        )

        return self.event_repository.create(event)

    def update_event(
        self,
        current_user,
        event_id: int,
        name: str | None = None,
        contract_id: int | None = None,
        support_contact_id: int | None = None,
        event_start=None,
        event_end=None,
        location: str | None = None,
        attendees: int | None = None,
        notes: str | None = None,
    ):
        """
        Met à jour un événement existant.

        Args:
            current_user: utilisateur connecté.
            event_id: identifiant de l'événement à modifier.
            name: nouveau nom, optionnel.
            contract_id: nouveau contrat lié, optionnel.
            support_contact_id: nouvel identifiant support, optionnel.
            event_start: nouvelle date de début, optionnel.
            event_end: nouvelle date de fin, optionnel.
            location: nouveau lieu, optionnel.
            attendees: nouveau nombre de participants, optionnel.
            notes: nouvelles notes, optionnel.

        """
        event = self.event_repository.get_by_id(event_id)
        if event is None:
            raise ValueError("Événement introuvable.")

        department = current_user.department.name

        if department == "management":
            pass
        elif department == "support":
            if event.support_contact_id != current_user.id:
                raise PermissionError("Vous ne pouvez modifier que vos événements.")
        else:
            raise PermissionError("Accès refusé pour la modification de l'événement.")

        if name is not None:
            if not name.strip():
                raise ValueError("Le nom de l'événement ne peut pas être vide.")
            event.name = name

        if contract_id is not None:
            event.contract_id = contract_id

        if support_contact_id is not None:
            event.support_contact_id = support_contact_id

        new_start = event.event_start if event_start is None else event_start
        new_end = event.event_end if event_end is None else event_end

        if new_end <= new_start:
            raise ValueError("La date de fin doit être après la date de début.")

        event.event_start = new_start
        event.event_end = new_end

        if location is not None:
            if not location.strip():
                raise ValueError("Le lieu ne peut pas être vide.")
            event.location = location

        if attendees is not None:
            if attendees < 0:
                raise ValueError("Le nombre de participants doit être positif ou nul.")
            event.attendees = attendees

        if notes is not None:
            event.notes = notes

        return self.event_repository.update(event)

    def delete_event(self, current_user, event_id: int):
        """
        Supprime un événement.

        Args:
            current_user: utilisateur connecté.
            event_id: identifiant de l'événement à supprimer.

        """
        event = self.event_repository.get_by_id(event_id)
        if event is None:
            raise ValueError("Événement introuvable.")

        department = current_user.department.name

        if department == "management":
            pass
        elif department == "support":
            if event.support_contact_id != current_user.id:
                raise PermissionError(
                    "Vous ne pouvez supprimer que les événements qui vous sont attribués."
                )
        else:
            raise PermissionError("Accès refusé pour la suppression de l'événement.")

        self.event_repository.delete(event)
