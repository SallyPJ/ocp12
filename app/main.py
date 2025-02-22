import click
from models import Base, Department
from controllers import UserController
from services.seed import seed_permissions, seed_departments, seed_department_permissions
from db.transaction_manager import TransactionManager
from services.auth_service import authenticate_user
from services.token_services import save_token

@click.group()
def cli():
    """EpicEvents CLI Application"""
    pass  # Required to allow multiple commands

@click.command()
def login():
    """Logs in a user and saves authentication token."""
    email = click.prompt("Enter your email")
    password = click.prompt("Enter your password", hide_input=True)

    with TransactionManager() as session:
        token = authenticate_user(session, email, password)

        if token:
            save_token(token)
            click.echo(click.style("✅ Login successful. Token saved.", fg="green"))
        else:
            click.echo(click.style("❌ Login failed.", fg="red"))

@click.command()
def setup():
    """Drops and recreates the database, then seeds default data."""
    with TransactionManager() as session:
        Base.metadata.drop_all(session.bind)
        Base.metadata.create_all(session.bind)

        seed_permissions(session)
        seed_departments(session)
        seed_department_permissions(session)

        sales_department = session.query(Department).filter_by(name="Sales").first()
        user_controller = UserController(session)

        click.echo(user_controller.create_user(
            first_name="Bob",
            last_name="Dupont",
            email="bob.sales@epicevents.com",
            password="password123",
            department_id=sales_department.id
        ))
        click.echo(click.style("✅ Database setup completed!", fg="green"))

# ✅ Add commands to the CLI
cli.add_command(login)
cli.add_command(setup)

if __name__ == "__main__":
    cli()