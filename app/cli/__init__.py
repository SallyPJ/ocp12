import click
from cli.user_cli import user
from cli.contract_cli import contract
from cli.customer_cli import customer
from cli.event_cli import event


@click.group()
def cli():
    """Interface CLI principale."""
    pass

# Ajouter les groupes de commandes
cli.add_command(user)
cli.add_command(contract)
cli.add_command(customer)
cli.add_command(event)