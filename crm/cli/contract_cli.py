import click
from database.transaction_manager import TransactionManager
from controllers.contract_controller import ContractController

@click.group()
def contract():
    """Commandes pour gérer les contrats."""
    pass

@contract.command()
@click.option("--customer-id", type=int, help="ID du client")
@click.option("--is-signed", type=bool, help="Filtrer par statut signé/non signé")
@click.option("--start-date", type=str, help="Date de début (format YYYY-MM-DD)")
@click.option("--end-date", type=str, help="Date de fin (format YYYY-MM-DD)")
@click.option("--sales-contact", type=int, help="ID du commercial responsable")
@click.option("--is-paid", type=bool, help="Afficher les contrats payés (True) ou non payés (False)")
def list(customer_id, is_signed, start_date, end_date, sales_contact, is_paid):
    """Afficher les contrats avec filtres optionnels."""
    with TransactionManager() as session:
        controller = ContractController(session)
        results = controller.list_contracts(
            customer_id=customer_id,
            is_signed=is_signed,
            start_date=start_date,
            end_date=end_date,
            sales_contact=sales_contact,
            is_paid=is_paid
        )
        for r in results:
            click.echo(r)

@contract.command()
@click.argument("contract_id", type=int)
def get(contract_id):
    """Afficher un contrat par ID."""
    with TransactionManager() as session:
        controller = ContractController(session)
        click.echo(controller.get_contract(contract_id))


@contract.command()
def create():
    """Créer un contrat avec saisie interactive."""
    customer_id = click.prompt("ID du client", type=int)
    sales_contact = click.prompt("ID du commercial responsable", type=int)
    total_amount = click.prompt("Montant total (€)", type=int)
    due_amount = click.prompt("Montant dû (€)", type=int)
    is_signed = click.confirm("Le contrat est-il signé ?")

    with TransactionManager() as session:
        controller = ContractController(session)
        click.echo(controller.create_contract(customer_id, sales_contact, total_amount, due_amount, is_signed))


@contract.command()
@click.argument("contract_id", type=int)
def update(contract_id):
    """Modifier un contrat avec saisie interactive."""

    click.echo("Laissez vide si vous ne souhaitez pas modifier un champ.")

    customer_id = click.prompt("Nouveau ID client", type=int, default=None, show_default=False)
    sales_contact = click.prompt("Nouvel ID commercial", type=int, default=None, show_default=False)
    total_amount = click.prompt("Nouveau montant total (€)", type=int, default=None, show_default=False)
    due_amount = click.prompt("Nouveau montant dû (€)", type=int, default=None, show_default=False)
    is_signed = click.confirm("Le contrat est-il signé ?", default=None)  # Saisie booléenne

    updates = {k: v for k, v in {
        "customer_id": customer_id,
        "sales_contact": sales_contact,
        "total_amount": total_amount,
        "due_amount": due_amount,
        "is_signed": is_signed
    }.items() if v is not None}

    if not updates:
        click.echo("❌ Aucun changement fourni.")
        return

    with TransactionManager() as session:
        controller = ContractController(session)
        click.echo(controller.update_contract(contract_id, **updates))