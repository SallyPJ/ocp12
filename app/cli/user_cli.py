import click
from database.transaction_manager import TransactionManager
from controllers.user_controller import UserController

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
def update(user_id):
    """Mettre à jour un utilisateur."""
    with TransactionManager() as session:
        user_controller = UserController(session)
        user = user_controller.user_dao.get_by_id(user_id)

        if not user:
            click.echo("❌ Utilisateur non trouvé.")
            return

        first_name = click.prompt("Nouveau prénom", default=user.first_name, show_default=True)
        last_name = click.prompt("Nouveau nom", default=user.last_name, show_default=True)
        email = click.prompt("Nouvel email", default=user.email, show_default=True)
        password = click.prompt("Nouveau mot de passe (laisser vide pour ne pas changer)", hide_input=True, default="", show_default=False)
        department_id = click.prompt("Nouvelle ID du département", type=int, default=user.department_id, show_default=True)

        updates = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "department_id": department_id
        }
        if password:
            updates["password"] = password

        message = user_controller.update_user(user_id, **updates)
        click.echo(message)

@user.command()
@click.argument("user_id", type=int)
def delete(user_id):
    """Supprimer un utilisateur."""
    with TransactionManager() as session:
        user_controller = UserController(session)
        user = user_controller.user_dao.get_by_id(user_id)

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