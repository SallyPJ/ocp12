import click
from rich.console import Console
from rich.prompt import Prompt
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
            customer_id, name_email = c.split(" - ", 1)
            table.add_row(customer_id, *name_email.split(" ("))

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
    enterprise = Prompt.ask("Entreprise (optionnel)", default="")

    with TransactionManager() as session:
        controller = CustomerController(session)
        console.print(controller.create_customer(name, email, phone, enterprise), style="bold green")

@customer.command()
@click.argument("customer_id", type=int)
def update(customer_id):
    """Mettre à jour un client."""
    with TransactionManager() as session:
        controller = CustomerController(session)

        # Vérifie si le client existe
        client_info = controller.get_customer(customer_id)
        if "❌" in client_info:
            console.print(client_info, style="bold red")
            return

        console.print(f"🛠️ Mise à jour du client : {client_info}", style="bold yellow")

        name = Prompt.ask("Nouveau nom (laisser vide pour ne pas modifier)", default=None)
        email = Prompt.ask("Nouvel email (laisser vide pour ne pas modifier)", default=None)
        phone = Prompt.ask("Nouveau téléphone (laisser vide pour ne pas modifier)", default=None)
        enterprise = Prompt.ask("Nouvelle entreprise (laisser vide pour ne pas modifier)", default=None)

        # Création d'un dictionnaire des champs à mettre à jour
        update_fields = {k: v for k, v in {
            "name": name,
            "email": email,
            "phone": phone,
            "enterprise": enterprise
        }.items() if v is not None}

        if not update_fields:
            console.print("❌ Aucun changement spécifié.", style="bold red")
            return

        console.print(controller.update_customer(customer_id, **update_fields), style="bold green")
