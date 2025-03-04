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
@click.option("--name", type=str, help="Nouveau nom du client")
@click.option("--email", type=str, help="Nouvel email du client")
@click.option("--phone", type=str, help="Nouveau numéro de téléphone")
@click.option("--enterprise", type=str, help="Nouvelle entreprise du client")
def update(customer_id, name, email, phone, enterprise):
    """🛠️ Modifier un client avec confirmation."""
    with TransactionManager() as session:
        controller = CustomerController(session)

        # 🔍 Récupérer les informations actuelles du client
        client = controller.get_customer(customer_id)
        if isinstance(client, str):  # Vérifie si c'est un message d'erreur
            console.print(client, style="bold red")
            return

        # 📋 Affichage des informations actuelles du client sous forme de tableau
        table = Table(show_header=False, title=f"📜 Client ID: {customer_id}", header_style="bold cyan")
        table.add_row("Nom:", client.name)
        table.add_row("Email:", client.email)
        table.add_row("Téléphone:", client.phone)
        table.add_row("Entreprise:", client.enterprise if client.enterprise else "N/A")
        console.print(table)

        # 📌 Création du dictionnaire des mises à jour (seuls les champs fournis sont mis à jour)
        update_fields = {
            k: v
            for k, v in {"name": name, "email": email, "phone": phone, "enterprise": enterprise}.items()
            if v is not None
        }

        if not update_fields:
            console.print("❌ Aucun changement spécifié.", style="bold red")
            return

        # ✅ Confirmation avant mise à jour
        console.print("\n📌 [bold yellow]Résumé des modifications :[/bold yellow]")
        confirm_table = Table(show_header=False)
        for field, value in update_fields.items():
            confirm_table.add_row(field.capitalize(), value)
        console.print(confirm_table)

        if not Confirm.ask("Voulez-vous appliquer ces modifications ?", default=True):
            console.print("❌ Mise à jour annulée.", style="bold red")
            return

        # 🔄 Exécution de la mise à jour
        result = controller.update_customer(customer_id, **update_fields)
        console.print(result, style="bold green")
