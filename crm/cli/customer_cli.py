import click
import rich_click as rclick
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from database.transaction_manager import TransactionManager
from controllers.customer_controller import CustomerController

console = Console()


@click.group(cls=rclick.RichGroup)
def customer():
    """👤 Commandes pour gérer les clients."""
    pass


@customer.command()
def list():
    """Afficher tous les clients."""
    with TransactionManager() as session:
        controller = CustomerController(session)
        customers = controller.list_customers()

        if not customers or isinstance(customers, str):  # ✅ Vérifie si `events` est vide ou une erreur
            return
        table = Table(title="📋 Liste des Clients")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Nom", style="bold")
        table.add_column("Email", style="magenta")
        table.add_column("Téléphone")
        table.add_column("Entreprise")
        table.add_column("Date de création")
        table.add_column("Dernier contact")
        table.add_column("Contact Sales")

        for customer in customers:
            table.add_row(
                str(customer["ID"]),
                customer["Nom"],
                customer["Email"],
                customer["Téléphone"],
                customer["Entreprise"],
                customer["Date de création"],
                customer["Dernier contact"],
                customer["Contact Sales"],
            )

        console.print(table)


@customer.command()
@click.argument("customer_id", type=int)
def get(customer_id):
    """Afficher un client par ID."""
    with TransactionManager() as session:
        controller = CustomerController(session)
        console.print(controller.get_customer(customer_id), style="bold cyan")


@customer.command()
def create():
    """Créer un nouveau client."""
    first_name = Prompt.ask("Prénom du client")
    last_name = Prompt.ask("Nom du client")
    email = Prompt.ask("Email du client")
    phone = Prompt.ask("Numéro de téléphone")
    enterprise = Prompt.ask("Entreprise")

    with TransactionManager() as session:
        controller = CustomerController(session)
        console.print(controller.create_customer(first_name, last_name, email, phone, enterprise), style="bold green")


@customer.command()
@click.argument("customer_id", type=int)
@click.option("--name", type=str, help="Nouveau nom du client")
@click.option("--email", type=str, help="Nouvel email du client")
@click.option("--phone", type=str, help="Nouveau numéro de téléphone")
@click.option("--enterprise", type=str, help="Nouvelle entreprise du client")
@click.option("--last-update", type=click.DateTime(formats=["%Y-%m-%d"]), help="Date du dernier contact (YYYY-MM-DD)")
def update(customer_id, name, email, phone, enterprise, last_update):
    """Modifier un client."""
    with TransactionManager() as session:
        controller = CustomerController(session)
        console.print(
            controller.update_customer(
                customer_id, name=name, email=email, phone=phone, enterprise=enterprise, last_update=last_update
            ),
            style="bold green",
        )
