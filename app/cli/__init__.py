import click
from cli.user_cli import user


@click.group()
def cli():
    """Interface CLI principale."""
    pass

# Ajouter les groupes de commandes
cli.add_command(user)
