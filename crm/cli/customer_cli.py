import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from database.transaction_manager import TransactionManager
from controllers.customer_controller import CustomerController

console = Console()


@click.group()
def customer():
    """Commandes pour gérer les clients."""
    pass


@customer.command()
def list():
    """Afficher tous les clients."""
    with TransactionManager() as session:
        controller = CustomerController(session)
        customers = controller.list_customers()

        table = Table(title="📋 Liste des Clients")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Nom", style="bold")
        table.add_column("Email", style="magenta")

        for c in customers:
            try:
                customer_id, name_email = c.split(" - ", 1)
                name, email = name_email.rsplit(" (", 1)
                email = email.rstrip(")")
                table.add_row(customer_id, name, email)
            except ValueError:
                console.print(f"❌ Erreur de formatage sur : {c}", style="bold red")
                continue

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
    name = Prompt.ask("Nom du client")
    email = Prompt.ask("Email du client")
    phone = Prompt.ask("Numéro de téléphone")
    enterprise = Prompt.ask("Entreprise")

    with TransactionManager() as session:
        controller = CustomerController(session)
        console.print(controller.create_customer(name, email, phone, enterprise), style="bold green")


@customer.command()
@click.argument("customer_id", type=int)
@click.option("--name", type=str, help="Nouveau nom du client")
@click.option("--email", type=str, help="Nouvel email du client")
@click.option("--phone", type=str, help="Nouveau numéro de téléphone")
@click.option("--enterprise", type=str, help="Nouvelle entreprise du client")
def update(customer_id, name, email, phone, enterprise):
    """Modifier un client."""
    with TransactionManager() as session:
        controller = CustomerController(session)
        console.print(controller.update_customer(customer_id, name=name, email=email, phone=phone, enterprise=enterprise), style="bold green")
