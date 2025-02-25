import click
from database.transaction_manager import TransactionManager
from controllers.event_controller import EventController

@click.group()
def event():
    """Commandes pour gérer les événements."""
    pass

@event.command()
def list():
    """Afficher tous les événements."""
    with TransactionManager() as session:
        controller = EventController(session)
        for e in controller.list_events():
            click.echo(e)

@event.command()
@click.argument("event_id", type=int)
def get(event_id):
    """Afficher un événement par ID."""
    with TransactionManager() as session:
        controller = EventController(session)
        click.echo(controller.get_event(event_id))


@event.command()
def create():
    """Créer un événement avec saisie interactive."""
    name = click.prompt("Nom de l'événement", type=str)
    contract_id = click.prompt("ID du contrat lié", type=int)
    customer_id = click.prompt("ID du client", type=int)
    start_date = click.prompt("Date de début (YYYY-MM-DD HH:MM)", type=str)
    end_date = click.prompt("Date de fin (YYYY-MM-DD HH:MM)", type=str)
    support_contact = click.prompt("ID du support (laisser vide si non assigné)", type=int, default=None,
                                   show_default=False)
    location = click.prompt("Lieu de l'événement", type=str)
    attendees = click.prompt("Nombre de participants", type=int)
    notes = click.prompt("Notes (laisser vide si aucune note)", type=str, default="", show_default=False)

    with TransactionManager() as session:
        controller = EventController(session)
        click.echo(
            controller.create_event(name, contract_id, customer_id, start_date, end_date, support_contact, location,
                                    attendees, notes))


@event.command()
@click.argument("event_id", type=int)
def update(event_id):
    """Modifier un événement avec saisie interactive."""

    click.echo("Laissez vide si vous ne souhaitez pas modifier un champ.")

    name = click.prompt("Nouveau nom de l'événement", type=str, default=None, show_default=False)
    contract_id = click.prompt("Nouveau ID du contrat", type=int, default=None, show_default=False)
    customer_id = click.prompt("Nouveau ID du client", type=int, default=None, show_default=False)
    start_date = click.prompt("Nouvelle date de début (YYYY-MM-DD HH:MM)", type=str, default=None, show_default=False)
    end_date = click.prompt("Nouvelle date de fin (YYYY-MM-DD HH:MM)", type=str, default=None, show_default=False)
    support_contact = click.prompt("Nouveau ID du support (laisser vide si inchangé)", type=int, default=None,
                                   show_default=False)
    location = click.prompt("Nouveau lieu", type=str, default=None, show_default=False)
    attendees = click.prompt("Nouveau nombre de participants", type=int, default=None, show_default=False)
    notes = click.prompt("Nouvelles notes (laisser vide si inchangé)", type=str, default=None, show_default=False)

    updates = {k: v for k, v in {
        "name": name,
        "contract_id": contract_id,
        "customer_id": customer_id,
        "start_date": start_date,
        "end_date": end_date,
        "support_contact": support_contact,
        "location": location,
        "attendees": attendees,
        "notes": notes
    }.items() if v is not None}

    if not updates:
        click.echo("❌ Aucun changement fourni.")
        return

    with TransactionManager() as session:
        controller = EventController(session)
        click.echo(controller.update_event(event_id, **updates))


@event.command()
@click.argument("event_id", type=int)
def delete(event_id):
    """Supprimer un événement."""
    with TransactionManager() as session:
        controller = EventController(session)
        click.echo(controller.delete_event(event_id))