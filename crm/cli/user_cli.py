import click
import rich_click as rclick
from rich.console import Console
from rich.table import Table
from database.transaction_manager import TransactionManager
from controllers.user_controller import UserController
from models.user import User


console = Console()


@click.group(cls=rclick.RichGroup)
def user():
    """Commandes pour gérer les utilisateurs."""
    pass


@user.command(cls=rclick.RichCommand)
def list():
    """Lister tous les utilisateurs."""
    with TransactionManager() as session:
        user_controller = UserController(session)
        users = user_controller.list_users()
        if not users or isinstance(users, str):  # ✅ Vérifie si `events` est vide ou une erreur
            return
        table = Table(
            title="📋 Liste des Utilisateurs" if len(users) > 1 else "👤 Détails de l'utilisateur", show_lines=True
        )
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Prénom", style="bold")
        table.add_column("Nom", style="bold")
        table.add_column("Email", style="magenta")
        table.add_column("Département", style="yellow")
        table.add_column("Statut", style="green")

        for user in users:
            department_info = f"{user.department.id} - {user.department.name}" if user.department else "N/A"
            table.add_row(
                str(user.id),
                user.first_name,
                user.last_name,
                user.email,
                department_info,
                "✅ Actif" if user.active else "❌ Inactif",
            )
        console.print(table)


@user.command()
@click.argument("user_id", type=int)
def get(user_id):
    """Afficher les informations d'un utilisateur par ID."""
    with TransactionManager() as session:
        controller = UserController(session)
        click.echo(controller.get_user(user_id))


@user.command(cls=rclick.RichCommand)
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


@user.command(cls=rclick.RichCommand)
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


@user.command(cls=rclick.RichCommand)
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


@user.command(cls=rclick.RichCommand)
@click.argument("user_id", type=int)
def deactivate(user_id):
    """Désactive un utilisateur par son ID (ex. lors de la démission)."""
    with TransactionManager() as session:
        controller = UserController(session)
        message = controller.deactivate_user(user_id)
        click.echo(message)
