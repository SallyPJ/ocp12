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