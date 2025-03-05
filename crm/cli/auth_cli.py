import rich_click as click
from rich_click import RichGroup
import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from services.auth_service import AuthService
from database.transaction_manager import TransactionManager
from controllers.auth_controller import AuthController

console = Console()


@click.group(invoke_without_command=True)
@click.pass_context
def auth(ctx):
    """🔑 Commandes d'authentification."""

    if ctx.invoked_subcommand is None:
        console.print(
            Panel(
                "[bold yellow]Bienvenue dans le menu d'authentification ![/bold yellow]\n\n"
                " Utilisez l'une des commandes suivantes :",
                title="🔑 Authentification",
                style="cyan",
                width=60,
                padding=(1, 2),
            )
        )

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Commande", style="bold magenta")
        table.add_column("Description", style="white")

        table.add_row("[bold]login[/bold]", "Connecte un utilisateur.")
        table.add_row("[bold]logout[/bold]", "Déconnecte l'utilisateur.")
        table.add_row("[bold]status[/bold]", "Affiche le statut de connexion de l'utilisateur.")

        console.print(table)
        console.print("\nℹ️ Tapez `[bold]main.py auth <commande>[/bold]` pour exécuter une commande.")


@auth.command()
def login():
    """🚀 Connecte un utilisateur et génère un JWT."""
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
