import click
from database.transaction_manager import TransactionManager
from controllers.user_controller import UserController
from models.user import User

@click.group()
def user():
    """Commandes pour gérer les utilisateurs."""
    pass

@user.command()
def create():
    """Créer un nouvel utilisateur via le CLI."""
    first_name = click.prompt("Prénom")
    last_name = click.prompt("Nom")
    email = click.prompt("Email")
    password = click.prompt("Mot de passe", hide_input=True, confirmation_prompt=True)
    department_id = click.prompt("ID du département", type=int)

    with TransactionManager() as session:
        user_controller = UserController(session)
        message = user_controller.create_user(first_name, last_name, email, password, department_id)
        click.echo(message)

@user.command()
@click.argument("user_id", type=int)
@click.option("--first-name", help="Nouveau prénom")
@click.option("--last-name", help="Nouveau nom")
@click.option("--email", help="Nouvel email")
@click.option("--password", help="Nouveau mot de passe")
@click.option("--department-id", type=int, help="Nouvel ID du département")
@click.option("--active", type=bool, help="L'utilisateur est-il actif ?")
def update(user_id, **kwargs):
    """Modifier un utilisateur existant."""
    with TransactionManager() as session:
        user_controller = UserController(session)
        message = user_controller.update_user(user_id, **kwargs)
        click.echo(message)

@user.command()
@click.argument("user_id", type=int)
def delete(user_id):
    """Supprimer un utilisateur."""
    with TransactionManager() as session:
        user_controller = UserController(session)
        user = user_controller.dao.get_by_id(user_id)

        if not user:
            click.echo("❌ Utilisateur non trouvé.")
            return

        if click.confirm(f"⚠ Voulez-vous vraiment supprimer {user.first_name} {user.last_name} ({user.email}) ?"):
            message = user_controller.delete_user(user_id)
            click.echo(message)
        else:
            click.echo("❌ Suppression annulée.")

@user.command()
def list():
    """Lister tous les utilisateurs."""
    with TransactionManager() as session:
        user_controller = UserController(session)
        users = user_controller.list_users()
        for user in users:
            click.echo(user)

@user.command()
@click.argument("user_id", type=int)
def deactivate(user_id):
    """Désactive un utilisateur par son ID (ex. lors de la démission)."""
    with TransactionManager() as session:
        controller = UserController(session)
        message = controller.deactivate_user(user_id)
        click.echo(message)

