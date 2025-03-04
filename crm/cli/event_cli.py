import click
from database.transaction_manager import TransactionManager
from controllers.event_controller import EventController
from cli.contract_cli import list as contract_list
from cli.user_cli import list as user_list


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
        click.echo(controller.list_events(all=all, **filters))


@event.command()
@click.argument("event_id", type=int)
def get(event_id):
    """Afficher un événement par ID."""
    with TransactionManager() as session:
        controller = EventController(session)
        click.echo(controller.get_event(event_id))


@event.command()
@click.pass_context
def create(ctx):
    """Créer un événement avec saisie interactive."""
    with TransactionManager() as session:
        controller = EventController(session)

        name = click.prompt("Nom de l'événement", type=str)
        click.echo("\n📜 Liste des contrats disponibles :")
        ctx.invoke(contract_list)
        contract_id = click.prompt("ID du contrat lié", type=int)
        start_date = click.prompt("Date de début (YYYY-MM-DD HH:MM)", type=str)
        end_date = click.prompt("Date de fin (YYYY-MM-DD HH:MM)", type=str)
        location = click.prompt("Lieu de l'événement", type=str)
        attendees = click.prompt("Nombre de participants", type=int)
        notes = click.prompt("Notes (optionnel)", type=str, default="", show_default=False)
        notes = notes if notes.strip() else None
        click.echo(
            controller.create_event(name, contract_id, start_date, end_date, location, attendees, notes))





@event.command()
@click.argument("event_id", type=int)
@click.option("--name", type=str, default=None, help="Nouveau nom de l'événement")
@click.option("--location", type=str, default=None, help="Nouveau lieu")
@click.option("--support-contact", type=int, default=None, help="Ajout d'un contact support")
@click.option("--attendees", type=int, default=None, help="Nouveau nombre de participants")
@click.option("--notes", type=str, default=None, help="Nouvelles notes")
def update(event_id, name, location, support_contact, attendees, notes):
    """Modifier un événement."""
    with TransactionManager() as session:
        controller = EventController(session)
        click.echo(controller.update_event(event_id, name=name, location=location, support_contact=support_contact, attendees=attendees, notes=notes))


@event.command()
@click.argument("event_id", type=int)
def delete(event_id):
    """Supprimer un événement."""
    with TransactionManager() as session:
        controller = EventController(session)
        click.echo(controller.delete_event(event_id))

