import click
import rich_click as rclick
from rich.console import Console
from rich.table import Table
from database.transaction_manager import TransactionManager
from controllers.contract_controller import ContractController

console = Console()


@click.group(cls=rclick.RichGroup)
def contract():
    """📜 Commandes de gestion des contrats"""


@contract.command()
@click.option("--customer-id", type=int, help="ID du client")
@click.option("--is-signed", type=bool, help="Afficher les contrats signés (True) ou non signé (False)")
@click.option("--start-date", type=str, help="Date de début (format YYYY-MM-DD)")
@click.option("--end-date", type=str, help="Date de fin (format YYYY-MM-DD)")
@click.option("--sales-contact", type=int, help="ID du commercial responsable")
@click.option("--is-paid", type=bool, help="Afficher les contrats payés (True) ou non payés (False)")
def list(customer_id, is_signed, start_date, end_date, sales_contact, is_paid):
    filters = {}
    if customer_id:
        filters["customer_id"] = customer_id
    if is_signed is not None:
        filters["is_signed"] = is_signed
    if start_date:
        filters["start_date"] = start_date
    if end_date:
        filters["end_date"] = end_date
    if sales_contact:
        filters["sales_contact"] = sales_contact
    if is_paid is not None:
        filters["is_paid"] = is_paid

    """📋 Afficher tous les contrats sous forme de tableau."""
    with TransactionManager() as session:
        controller = ContractController(session)
        contracts = controller.list_contracts(**filters)

        if isinstance(contracts, str):  # if error message
            console.print(contracts, style="bold red")
            return

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", justify="center")
        table.add_column("Client")
        table.add_column("Commercial")
        table.add_column("Montant Total (€)", justify="right")
        table.add_column("Montant dû (€)", justify="right")
        table.add_column("Signé", justify="center")
        table.add_column("Payé", justify="center")
        table.add_column("Date Création", justify="center")
        table.add_column("Événement", style="yellow", justify="center")

        if not contracts or isinstance(contract, str):
            return
        for c in contracts:
            table.add_row(
                str(c["ID"]),
                c["Client"],
                c["Commercial"],
                f"{c['Montant Total (€)']} €",
                f"{c['Montant dû (€)']} €",
                "✅" if c["Signé"] == "Oui" else "❌",
                "✅" if c["Payé"] == "Oui" else "❌",
                c["Date Création"],
                c["Événement associé"],
            )

        console.print(table)


@contract.command()
@click.argument("contract_id", type=int)
def get(contract_id):
    """🔍 Afficher un contrat par ID sous forme de tableau."""
    with TransactionManager() as session:
        controller = ContractController(session)
        contract = controller.get_contract(contract_id)

        if not contract or isinstance(contract, str):
            console.print(contract, style="bold red")
            return


        table = Table(title="📜 Détails du Contrat", header_style="bold cyan")
        for key, value in contract.items():
            table.add_row(key, str(value))

        console.print(table)


@contract.command()
def create():
    """Créer un contrat avec saisie interactive."""
    customer_id = click.prompt("ID du client", type=int)
    total_amount = click.prompt("Montant total (€)", type=int)
    due_amount = click.prompt("Montant dû (€)", type=int)
    is_signed = click.confirm("Le contrat est-il signé ?")

    with TransactionManager() as session:
        controller = ContractController(session)
        click.echo(controller.create_contract(customer_id, total_amount, due_amount, is_signed))


@contract.command()
@click.argument("contract_id", type=int)
@click.option("--sales-contact", type=int, help="Nouvel ID commercial")
@click.option("--total-amount", type=int, help="Nouveau montant total (€)")
@click.option("--due-amount", type=int, help="Nouveau montant dû (€)")
@click.option(
    "--is-signed", type=click.Choice(["yes", "no"], case_sensitive=False), help="Le contrat est-il signé ? (yes/no)"
)
def update(contract_id, sales_contact, total_amount, due_amount, is_signed):
    """Modifier un contrat en affichant ses détails avant modification."""

    with TransactionManager() as session:
        controller = ContractController(session)
        contract = controller.get_contract(contract_id)

        if not contract or isinstance(contract, str):  # Cas où le contrat n'est pas trouvé
            console.print(contract, style="bold red")
            return

        # 📋 Afficher les informations actuelles sous forme de tableau
        table = Table(title="📜 Contrat sélectionné", header_style="bold cyan")
        table.add_column("Champ", style="bold")
        table.add_column("Valeur", style="white")

        table.add_row("ID", str(contract["ID"]))  # ✅ Accès via le dictionnaire
        table.add_row("Client", contract["Client"])
        table.add_row("Commercial", contract["Commercial"])
        table.add_row("Montant Total (€)", f"{contract['Montant Total (€)']} €")
        table.add_row("Montant dû (€)", f"{contract['Montant dû (€)']} €")
        table.add_row("Signé", contract["Signé"])
        table.add_row("Payé", contract["Payé"])
        table.add_row("Date Création", contract["Date Création"])
        table.add_row("Événement associé", contract["Événement associé"])

        console.print(table)

        # 🔄 Demander confirmation avant de modifier
        if not click.confirm("Souhaitez-vous modifier ce contrat ?", default=False):
            console.print("❌ Modification annulée.", style="bold yellow")
            return

        # 🛠 Appliquer uniquement les modifications fournies
        updates = {
            "sales_contact": sales_contact,
            "total_amount": total_amount,
            "due_amount": due_amount,
            "is_signed": is_signed == "yes" if is_signed else None,  # Convertir en booléen
        }

        updates = {k: v for k, v in updates.items() if v is not None}

        if not updates:
            console.print("❌ Aucun changement fourni.", style="bold red")
            return

        result = controller.update_contract(contract_id, **updates)
        console.print(result, style="bold green" if "✅" in result else "bold red")
