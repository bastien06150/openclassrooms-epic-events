import click
import sentry_sdk
from datetime import datetime

from app.database import SessionLocal
from app.services.auth_service import AuthService
from app.services.client_service import ClientService
from app.services.contract_service import ContractService
from app.services.event_service import EventService
from app.services.employee_service import EmployeeService
from app.sentry_setup import init_sentry

init_sentry()


@click.group()
def cli():
    pass


@cli.command("test-sentry")
def test_sentry():
    raise ValueError("Test Sentry depuis CLI")


# AUTH


@cli.command()
@click.option("--email", prompt="Email")
@click.option("--password", prompt="Mot de passe", hide_input=True)
def login(email, password):
    """Connecte un utilisateur."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)

        if auth_service.login(email, password):
            click.echo("Connexion réussie.")
        else:
            click.echo("Identifiants invalides.")
    finally:
        session.close()


@cli.command("current-user")
def current_user():
    """Affiche l'utilisateur actuellement connecté."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        employee = auth_service.get_current_user()

        if employee is None:
            click.echo("Aucun utilisateur connecté.")
            return

        click.echo(f"ID : {employee.id}")
        click.echo(f"Utilisateur : {employee.full_name}")
        click.echo(f"Département : {employee.department.name}")
    finally:
        session.close()


@cli.command()
def logout():
    """Déconnecte l'utilisateur courant."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        auth_service.logout()
        click.echo("Déconnexion effectuée.")
    finally:
        session.close()


# CLIENT


@cli.group()
def client():
    """Commandes client."""
    pass


@client.command("list")
def list_clients():
    """Liste les clients."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        client_service = ClientService(session)

        current_user = auth_service.get_current_user()
        clients = client_service.list_clients(current_user)

        if not clients:
            click.echo("Aucun client trouvé.")
            return

        for c in clients:
            click.echo(
                f"[{c.id}] {c.full_name} - {c.company_name} - {c.email} - commercial_id={c.sales_contact_id}"
            )
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


@client.command("create")
@click.option("--full-name", prompt="Nom complet")
@click.option("--email", prompt="Email")
@click.option("--phone", prompt="Téléphone")
@click.option("--company-name", prompt="Entreprise")
def create_client(full_name, email, phone, company_name):
    """Crée un client."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        client_service = ClientService(session)

        current_user = auth_service.get_current_user()

        client = client_service.create_client(
            current_user=current_user,
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
        )

        click.echo(f"Client créé : {client.full_name} (ID {client.id})")
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


@client.command("delete")
@click.option("--client-id", prompt="ID du client", type=int)
def delete_client(client_id):
    """Supprime un client."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        client_service = ClientService(session)

        current_user = auth_service.get_current_user()

        client_service.delete_client(
            current_user=current_user,
            client_id=client_id,
        )

        click.echo("Client supprimé avec succès.")
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


# CONTRACT


@cli.group()
def contract():
    """Commandes contrat."""
    pass


@contract.command("list")
def list_contracts():
    """Liste les contrats."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        contract_service = ContractService(session)

        current_user = auth_service.get_current_user()
        contracts = contract_service.list_contracts(current_user)

        if not contracts:
            click.echo("Aucun contrat trouvé.")
            return

        for c in contracts:
            click.echo(
                f"[{c.id}] client_id={c.client_id} | total={c.total_amount} | dû={c.amount_due} | signé={c.is_signed}"
            )
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


@contract.command("create")
@click.option("--client-id", prompt="ID du client", type=int)
@click.option("--total-amount", prompt="Montant total", type=float)
@click.option("--amount-due", prompt="Montant restant dû", type=float)
@click.option(
    "--is-signed",
    prompt="Contrat signé ? (true/false)",
    type=bool,
)
def create_contract(client_id, total_amount, amount_due, is_signed):
    """Crée un contrat."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        contract_service = ContractService(session)

        current_user = auth_service.get_current_user()

        contract = contract_service.create_contract(
            current_user=current_user,
            client_id=client_id,
            total_amount=total_amount,
            amount_due=amount_due,
            is_signed=is_signed,
        )

        click.echo(f"Contrat créé : ID {contract.id}")
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


@contract.command("update")
@click.option("--contract-id", prompt="ID du contrat", type=int)
def update_contract(contract_id):
    """Modifie un contrat."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        contract_service = ContractService(session)

        current_user = auth_service.get_current_user()

        client_id_input = click.prompt(
            "Nouveau client_id (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        total_amount_input = click.prompt(
            "Nouveau montant total (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        amount_due_input = click.prompt(
            "Nouveau montant restant dû (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        is_signed_input = (
            click.prompt(
                "Nouveau statut signé ? (oui/non/vide)", default="", show_default=False
            )
            .strip()
            .lower()
        )

        client_id = int(client_id_input) if client_id_input else None
        total_amount = float(total_amount_input) if total_amount_input else None
        amount_due = float(amount_due_input) if amount_due_input else None

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

        click.echo(f"Contrat modifié : ID {contract.id}")
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


@contract.command("delete")
@click.option("--contract-id", prompt="ID du contrat", type=int)
def delete_contract(contract_id):
    """Supprime un contrat."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        contract_service = ContractService(session)

        current_user = auth_service.get_current_user()

        contract_service.delete_contract(
            current_user=current_user,
            contract_id=contract_id,
        )

        click.echo("Contrat supprimé avec succès.")
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


# EVENT


@cli.group()
def event():
    """Commandes événement."""
    pass


@event.command("list")
def list_events():
    """Liste les événements."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        event_service = EventService(session)

        current_user = auth_service.get_current_user()
        events = event_service.list_events(current_user)

        if not events:
            click.echo("Aucun événement trouvé.")
            return

        for e in events:
            click.echo(
                f"[{e.id}] {e.name} | contract_id={e.contract_id} | support_id={e.support_contact_id} | {e.location}"
            )
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


@event.command("create")
@click.option("--name", prompt="Nom de l'événement")
@click.option("--contract-id", prompt="ID du contrat", type=int)
@click.option("--event-start", prompt="Date début (YYYY-MM-DD HH:MM)")
@click.option("--event-end", prompt="Date fin (YYYY-MM-DD HH:MM)")
@click.option("--location", prompt="Lieu")
@click.option("--attendees", prompt="Nombre de participants", type=int)
@click.option("--notes", default=None)
@click.option("--support-contact-id", type=int, default=None)
def create_event(
    name,
    contract_id,
    event_start,
    event_end,
    location,
    attendees,
    notes,
    support_contact_id,
):
    """Crée un événement."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        event_service = EventService(session)

        current_user = auth_service.get_current_user()

        start_dt = datetime.strptime(event_start, "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(event_end, "%Y-%m-%d %H:%M")

        event_obj = event_service.create_event(
            current_user=current_user,
            name=name,
            contract_id=contract_id,
            event_start=start_dt,
            event_end=end_dt,
            location=location,
            attendees=attendees,
            notes=notes,
            support_contact_id=support_contact_id,
        )

        click.echo(f"Événement créé : ID {event_obj.id}")
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


@event.command("update")
@click.option("--event-id", prompt="ID de l'événement", type=int)
def update_event(event_id):
    """Modifie un événement."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        event_service = EventService(session)

        current_user = auth_service.get_current_user()

        name_input = click.prompt(
            "Nouveau nom (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        contract_id_input = click.prompt(
            "Nouveau contract_id (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        support_contact_input = click.prompt(
            "Nouveau support_contact_id (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        event_start_input = click.prompt(
            "Nouvelle date début YYYY-MM-DD HH:MM (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        event_end_input = click.prompt(
            "Nouvelle date fin YYYY-MM-DD HH:MM (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        location_input = click.prompt(
            "Nouveau lieu (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        attendees_input = click.prompt(
            "Nouveau nombre de participants (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        notes_input = click.prompt(
            "Nouvelles notes (laisser vide si inchangé)",
            default="",
            show_default=False,
        )

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

        event_obj = event_service.update_event(
            current_user=current_user,
            event_id=event_id,
            name=name_input if name_input else None,
            contract_id=contract_id,
            support_contact_id=support_contact_id,
            event_start=event_start,
            event_end=event_end,
            location=location_input if location_input else None,
            attendees=attendees,
            notes=notes_input if notes_input else None,
        )

        click.echo(f"Événement modifié : ID {event_obj.id}")
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


@event.command("delete")
@click.option("--event-id", prompt="ID de l'événement", type=int)
def delete_event(event_id):
    """Supprime un événement."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        event_service = EventService(session)

        current_user = auth_service.get_current_user()

        event_service.delete_event(
            current_user=current_user,
            event_id=event_id,
        )

        click.echo("Événement supprimé avec succès.")
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


# EMPLOYEE


@cli.group()
def employee():
    """Commandes collaborateur."""
    pass


@employee.command("create")
@click.option("--employee-number", prompt="Numéro employé")
@click.option("--full-name", prompt="Nom complet")
@click.option("--email", prompt="Email")
@click.option("--password", prompt="Mot de passe", hide_input=True)
@click.option("--department-id", prompt="ID du département", type=int)
def create_employee(employee_number, full_name, email, password, department_id):
    """Crée un collaborateur."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        employee_service = EmployeeService(session)

        current_user = auth_service.get_current_user()

        employee_obj = employee_service.create_employee(
            current_user=current_user,
            employee_number=employee_number,
            full_name=full_name,
            email=email,
            password=password,
            department_id=department_id,
        )

        click.echo(
            f"Collaborateur créé : {employee_obj.full_name} ({employee_obj.employee_number})"
        )
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


@employee.command("update")
@click.option("--employee-id", prompt="ID du collaborateur", type=int)
def update_employee(
    employee_id,
):
    """Modifie un collaborateur."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        employee_service = EmployeeService(session)

        current_user = auth_service.get_current_user()

        full_name_input = click.prompt(
            "Nouveau nom complet (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        email_input = click.prompt(
            "Nouvel email (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        department_id_input = click.prompt(
            "Nouveau department_id (laisser vide si inchangé)",
            default="",
            show_default=False,
        )
        password_input = click.prompt(
            "Nouveau mot de passe (laisser vide si inchangé)",
            default="",
            show_default=False,
            hide_input=True,
        )

        department_id = int(department_id_input) if department_id_input else None

        employee_obj = employee_service.update_employee(
            current_user=current_user,
            employee_id=employee_id,
            full_name=full_name_input if full_name_input else None,
            email=email_input if email_input else None,
            department_id=department_id,
            password=password_input if password_input else None,
        )

        click.echo(f"Collaborateur modifié : {employee_obj.full_name}")
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


@employee.command("delete")
@click.option("--employee-id", prompt="ID du collaborateur", type=int)
def delete_employee(employee_id):
    """Supprime un collaborateur."""
    session = SessionLocal()
    try:
        auth_service = AuthService(session)
        employee_service = EmployeeService(session)

        current_user = auth_service.get_current_user()

        employee_service.delete_employee(
            current_user=current_user,
            employee_id=employee_id,
        )

        click.echo("Collaborateur supprimé avec succès.")
    except Exception as error:
        sentry_sdk.capture_exception(error)
        click.echo(f"Erreur : {error}")
    finally:
        session.close()


if __name__ == "__main__":
    cli()
