import click
from database.transaction_manager import TransactionManager
from controllers.contract_controller import ContractController

@click.group()
def contract():
    """Commandes pour gérer les contrats."""
    pass

@contract.command()
def list():
    """Afficher tous les contrats."""
    with TransactionManager() as session:
        controller = ContractController(session)
        for c in controller.list_contracts():
            click.echo(c)

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
    status = click.prompt("Statut du contrat (signed / not_signed)", type=click.Choice(["signed", "not_signed"]))

    with TransactionManager() as session:
        controller = ContractController(session)
        click.echo(controller.create_contract(customer_id, sales_contact, total_amount, due_amount, status))


@contract.command()
@click.argument("contract_id", type=int)
def update(contract_id):
    """Modifier un contrat avec saisie interactive."""

    click.echo("Laissez vide si vous ne souhaitez pas modifier un champ.")

    customer_id = click.prompt("Nouveau ID client", type=int, default=None, show_default=False)
    sales_contact = click.prompt("Nouvel ID commercial", type=int, default=None, show_default=False)
    total_amount = click.prompt("Nouveau montant total (€)", type=int, default=None, show_default=False)
    due_amount = click.prompt("Nouveau montant dû (€)", type=int, default=None, show_default=False)
    status = click.prompt("Nouveau statut (signed / not_signed)", type=click.Choice(["signed", "not_signed"]),
                          default=None, show_default=False)

    updates = {k: v for k, v in {
        "customer_id": customer_id,
        "sales_contact": sales_contact,
        "total_amount": total_amount,
        "due_amount": due_amount,
        "status": status
    }.items() if v is not None}

    if not updates:
        click.echo("❌ Aucun changement fourni.")
        return

    with TransactionManager() as session:
        controller = ContractController(session)
        click.echo(controller.update_contract(contract_id, **updates))