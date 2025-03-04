import click
from database.transaction_manager import TransactionManager
from controllers.event_controller import EventController


@click.group()
def event():
    """Commandes pour gérer les événements."""
    pass


@event.command()
@click.option("--all", is_flag=True, help="Afficher tous les événements sans appliquer de filtre.")
@click.option("--no_support", is_flag=True, help="Filtrer les événements sans support.")
@click.option("--location", type=str, help="Filtrer les événements par lieu.")
@click.option("--start_date", type=str, help="Filtrer les événements à partir de cette date (YYYY-MM-DD).")
@click.option("--end_date", type=str, help="Filtrer les événements jusqu'à cette date (YYYY-MM-DD).")
def list(all, no_support, location, start_date, end_date):
    """Afficher les événements selon les filtres spécifiés ou tous les événements si --all est activé."""
    filters = {}
    if no_support:
        filters["no_support"] = True
    if location:
        filters["location"] = location
    if start_date:
        filters["start_date"] = start_date
    if end_date:
        filters["end_date"] = end_date

    with TransactionManager() as session:
        controller = EventController(session)
        events = controller.list_events(all=all, **filters)
        if not events:
            click.echo("Aucun événement trouvé.")
        for event in events:
            click.echo(event)


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
    support_contact = click.prompt(
        "ID du support (laisser vide si non assigné)", type=int, default=None, show_default=False
    )
    location = click.prompt("Lieu de l'événement", type=str)
    attendees = click.prompt("Nombre de participants", type=int)
    notes = click.prompt("Notes (laisser vide si aucune note)", type=str, default=None, show_default=False)

    with TransactionManager() as session:
        controller = EventController(session)
        try:
            event = controller.create_event(
                name, contract_id, customer_id, start_date, end_date, support_contact, location, attendees, notes
            )
            click.secho(f"✅ Événement '{event.name}' créé avec succès.", fg="green")
        except ValueError as e:
            click.secho(f"❌ {e}", fg="red")


@event.command()
@click.argument("event_id", type=int)
@click.option("--name", type=str, default=None, help="Nouveau nom de l'événement")
@click.option("--contract_id", type=int, default=None, help="Nouveau ID du contrat")
@click.option("--customer_id", type=int, default=None, help="Nouveau ID du client")
@click.option("--start_date", type=str, default=None, help="Nouvelle date de début (YYYY-MM-DD HH:MM)")
@click.option("--end_date", type=str, default=None, help="Nouvelle date de fin (YYYY-MM-DD HH:MM)")
@click.option("--support_contact", type=int, default=None, help="Nouveau ID du support")
@click.option("--location", type=str, default=None, help="Nouveau lieu")
@click.option("--attendees", type=int, default=None, help="Nouveau nombre de participants")
@click.option("--notes", type=str, default=None, help="Nouvelles notes")
def update(event_id, name, contract_id, customer_id, start_date, end_date, support_contact, location, attendees, notes):
    """Modifier un événement avec les options fournies. Format : python main.py event update 1 --name "Nouvel événement" --location "Paris" --start_date "2025-05-01 10:00" --attendees 100"""

    # Rassembler les changements dans un dictionnaire
    updates = {
        "name": name,
        "contract_id": contract_id,
        "customer_id": customer_id,
        "start_date": start_date,
        "end_date": end_date,
        "support_contact": support_contact,
        "location": location,
        "attendees": attendees,
        "notes": notes,
    }

    # Filtrer les options qui ne sont pas `None`
    updates = {k: v for k, v in updates.items() if v is not None}

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
