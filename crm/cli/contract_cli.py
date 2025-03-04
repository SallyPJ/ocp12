import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from database.transaction_manager import TransactionManager
from controllers.contract_controller import ContractController

console = Console()


@click.group(invoke_without_command=True)
@click.pass_context
def contract(ctx):
    """📜 [bold cyan]Commandes de gestion des contrats[/bold cyan]."""

    if ctx.invoked_subcommand is None:
        console.print(
            Panel(
                "[bold yellow]Bienvenue dans le menu de gestion des contrats ![/bold yellow]\n\n"
                " Utilisez l'une des commandes suivantes :",
                title="📜 Gestion des contrats",
                style="cyan",
                width=70,
                padding=(1, 2),
            )
        )

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Commande", style="bold magenta")
        table.add_column("Description", style="white")

        table.add_row("[bold]list[/bold]", "Afficher tous les contrats.")
        table.add_row("[bold]get <id>[/bold]", "Afficher un contrat par ID.")
        table.add_row("[bold]create[/bold]", "Créer un nouveau contrat.")
        table.add_row("[bold]update <id>[/bold]", "Modifier un contrat existant.")

        console.print(table)
        console.print("\nℹ️ Tapez `[bold]main.py contract <commande>[/bold]` pour exécuter une commande.")


@contract.command()
def list():
    """📋 Afficher tous les contrats sous forme de tableau."""
    with TransactionManager() as session:
        controller = ContractController(session)
        contracts = controller.list_contracts()

        if not contracts:
            console.print("❌ Aucun contrat trouvé.", style="bold red")
            return

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", style="bold magenta", justify="center")
        table.add_column("Client", style="white", justify="center")
        table.add_column("Commercial", style="white", justify="center")
        table.add_column("Montant Total (€)", style="green", justify="right")
        table.add_column("Montant dû (€)", style="red", justify="right")
        table.add_column("Signé", style="cyan", justify="center")
        table.add_column("Payé", style="green", justify="center")
        table.add_column("Date Création", style="yellow", justify="center")

        for c in contracts:
            # 🛠 Vérifie si c'est un dictionnaire ou un objet SQLAlchemy
            contract_id = c["id"] if isinstance(c, dict) else c.id
            customer_name = c["customer_name"] if isinstance(c, dict) else c.customer.name
            sales_contact_name = (
                c["sales_contact_name"]
                if isinstance(c, dict)
                else f"{c.sales_contact_user.first_name} {c.sales_contact_user.last_name}"
            )
            total_amount = c["total_amount"] if isinstance(c, dict) else c.total_amount
            due_amount = c["due_amount"] if isinstance(c, dict) else c.due_amount
            is_signed = c["is_signed"] if isinstance(c, dict) else c.is_signed
            is_paid = c["is_paid"] if isinstance(c, dict) else c.is_paid
            creation_date = c["creation_date"] if isinstance(c, dict) else c.creation_date.strftime("%Y-%m-%d")

            table.add_row(
                str(contract_id),
                customer_name,
                sales_contact_name,
                f"{total_amount} €",
                f"{due_amount} €",
                "✅ Oui" if is_signed else "❌ Non",
                "✅ Oui" if is_paid else "❌ Non",
                creation_date,
            )

        console.print(table)


@contract.command()
@click.argument("contract_id", type=int)
def get(contract_id):
    """🔍 Afficher un contrat par ID sous forme de tableau."""
    with TransactionManager() as session:
        controller = ContractController(session)
        contract = controller.get_contract(contract_id)  # ⬅️ Ajout des parenthèses ici !

        if isinstance(contract, str):  # Si `contract` est un message d'erreur, on l'affiche directement
            console.print(contract, style="bold red")
            return

        table = Table(show_header=False, header_style="bold cyan")
        table.add_row("[bold]ID[/bold]", str(contract.id))
        table.add_row("[bold]Client[/bold]", contract.customer.name)
        table.add_row(
            "[bold]Commercial[/bold]",
            f"{contract.sales_contact_user.first_name} {contract.sales_contact_user.last_name}",
        )
        table.add_row("[bold]Montant Total (€)[/bold]", f"{contract.total_amount} €")
        table.add_row("[bold]Montant dû (€)[/bold]", f"{contract.due_amount} €")
        table.add_row("[bold]Signé[/bold]", "✅ Oui" if contract.is_signed else "❌ Non")
        table.add_row("[bold]Payé[/bold]", "✅ Oui" if contract.is_paid else "❌ Non")
        table.add_row("[bold]Date de création[/bold]", contract.creation_date.strftime("%Y-%m-%d"))

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
@click.option("--customer-id", type=int, help="Nouvel ID client")
@click.option("--sales-contact", type=int, help="Nouvel ID commercial")
@click.option("--total-amount", type=int, help="Nouveau montant total (€)")
@click.option("--due-amount", type=int, help="Nouveau montant dû (€)")
@click.option(
    "--is-signed", type=click.Choice(["yes", "no"], case_sensitive=False), help="Le contrat est-il signé ? (yes/no)"
)
def update(contract_id, customer_id, sales_contact, total_amount, due_amount, is_signed):
    """Modifier un contrat en affichant ses détails avant modification."""

    with TransactionManager() as session:
        controller = ContractController(session)
        contract = controller.get_contract(contract_id)

        if isinstance(contract, str):  # Cas où le contrat n'est pas trouvé
            console.print(contract, style="bold red")
            return

        # 📋 Afficher les informations actuelles sous forme de tableau
        table = Table(title="📜 Contrat sélectionné", header_style="bold cyan")
        table.add_column("Champ", style="bold")
        table.add_column("Valeur", style="white")

        table.add_row("ID", str(contract.id))
        table.add_row("Client", contract.customer.name)
        table.add_row("Commercial", f"{contract.sales_contact_user.first_name} {contract.sales_contact_user.last_name}")
        table.add_row("Montant Total (€)", f"{contract.total_amount} €")
        table.add_row("Montant dû (€)", f"{contract.due_amount} €")
        table.add_row("Signé", "✅ Oui" if contract.is_signed else "❌ Non")
        table.add_row("Date de création", contract.creation_date.strftime("%Y-%m-%d"))

        console.print(table)

        # 🔄 Demander confirmation avant de modifier
        if not click.confirm("Souhaitez-vous modifier ce contrat ?", default=False):
            console.print("❌ Modification annulée.", style="bold yellow")
            return

        # 🛠 Appliquer uniquement les modifications fournies
        updates = {
            "customer_id": customer_id,
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
