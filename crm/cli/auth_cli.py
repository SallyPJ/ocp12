import rich_click as rclick
import click
from rich.console import Console
from rich.panel import Panel
from services.auth_service import AuthService
from database.transaction_manager import TransactionManager
from controllers.auth_controller import AuthController

console = Console()


@click.group(cls=rclick.RichGroup)
def auth():
    """🔑 Commandes d'authentification."""


@auth.command()
def login():
    """Connecte un utilisateur et génère un JWT."""
    console.print(Panel("🔑 [bold cyan]Connexion à votre compte[/bold cyan]", style="blue", width=60))

    email = click.prompt("Email")
    password = click.prompt("Mot de passe", hide_input=True)

    with TransactionManager() as session:
        auth_controller = AuthController(session)
        click.echo(auth_controller.login(email, password))


@auth.command()
def logout():
    """Déconnecte l'utilisateur."""
    with TransactionManager() as session:
        auth_controller = AuthController(session)
        click.echo(auth_controller.logout())


@auth.command()
def status():
    """Affiche le statut de connexion de l'utilisateur."""
    with TransactionManager() as session:
        auth_controller = AuthController(session)
        user_info = auth_controller.is_logged_in()

        if user_info:

            print(f"✅ Connecté en tant que : {user_info['email']}")
            print(f"🔑 ID utilisateur : {user_info['id']}")

        else:
            print("❌ Aucun utilisateur connecté.")
