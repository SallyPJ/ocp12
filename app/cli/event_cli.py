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
