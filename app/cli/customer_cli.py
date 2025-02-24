import click
from database.transaction_manager import TransactionManager
from controllers.customer_controller import CustomerController

@click.group()
def customer():
    """Commandes pour gérer les clients."""
    pass

@customer.command()
def list():
    """Afficher tous les clients."""
    with TransactionManager() as session:
        controller = CustomerController(session)
        for c in controller.list_customers():
            click.echo(c)

@customer.command()
@click.argument("customer_id", type=int)
def get(customer_id):
    """Afficher un client par ID."""
    with TransactionManager() as session:
        controller = CustomerController(session)
        click.echo(controller.get_customer(customer_id))