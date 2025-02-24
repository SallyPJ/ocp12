import click
from database.transaction_manager import TransactionManager
from controllers.user_controller import UserController

@click.group()
def cli():
    """Interface CLI pour gérer les utilisateurs du CRM."""
    pass

@click.command()
@click.argument("first_name")
@click.argument("last_name")
@click.argument("email")
@click.argument("password")
@click.argument("department_id", type=int)
def create_user(first_name, last_name, email, password, department_id):
    """Créer un nouvel utilisateur."""
    with TransactionManager() as session:
        user_controller = UserController(session)
        message = user_controller.create_user(first_name, last_name, email, password, department_id)
        click.echo(message)

@click.command()
@click.argument("user_id", type=int)
@click.option("--first_name", help="Nouveau prénom")
@click.option("--last_name", help="Nouveau nom")
@click.option("--email", help="Nouvel email")
@click.option("--password", help="Nouveau mot de passe")
@click.option("--department_id", type=int, help="Nouvelle ID de département")
def update_user(user_id, first_name, last_name, email, password, department_id):
    """Mettre à jour un utilisateur existant."""
    with TransactionManager() as session:
        user_controller = UserController(session)
        message = user_controller.update_user(user_id, first_name=first_name, last_name=last_name, email=email, password=password, department_id=department_id)
        click.echo(message)

@click.command()
@click.argument("user_id", type=int)
def delete_user(user_id):
    """Supprimer un utilisateur."""
    with TransactionManager() as session:
        user_controller = UserController(session)
        message = user_controller.delete_user(user_id)
        click.echo(message)

@click.command()
def list_users():
    """Afficher la liste de tous les utilisateurs."""
    with TransactionManager() as session:
        user_controller = UserController(session)
        users = user_controller.list_users()
        for user in users:
            click.echo(user)

cli.add_command(create_user)
cli.add_command(update_user)
cli.add_command(delete_user)
cli.add_command(list_users)