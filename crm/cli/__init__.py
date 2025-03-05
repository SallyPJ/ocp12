import rich_click as rclick
from rich_click import RichGroup
import click
from cli.user_cli import user
from cli.contract_cli import contract
from cli.customer_cli import customer
from cli.event_cli import event
from cli.auth_cli import auth

rclick.rich_click.USE_MARKDOWN = True
rclick.rich_click.MAX_WIDTH = 100


@click.group(cls=RichGroup, help="🚀 **CLI principale du CRM Epic Events** : Gérer les employés, clients, contrats et événements.")
def cli():
    """Main CLI interface."""
    pass

cli.add_command(user)
cli.add_command(contract)
cli.add_command(customer)
cli.add_command(event)
cli.add_command(auth)
