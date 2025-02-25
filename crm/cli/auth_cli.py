import click
from services.auth import AuthService
from database.transaction_manager import TransactionManager
from controllers.auth_controller import AuthController
import datetime


@click.group()
def auth():
    """Commandes d'authentification."""
    pass

@auth.command()
def login():
    """Connecte un utilisateur et génère un JWT."""
    email = click.prompt("Email")
    password = click.prompt("Mot de passe", hide_input=True)

    with TransactionManager() as session:
        auth_controller = AuthController(session)
        click.echo(auth_controller.login(email, password))

@auth.command()
def logout():
    """Déconnecte l'utilisateur."""
    with TransactionManager() as session:
        auth_controller = AuthController(session)
        click.echo(auth_controller.logout())

@auth.command()
def status():
    """Affiche le statut de connexion de l'utilisateur."""
    with TransactionManager() as session:
        auth_service = AuthService(session)
        user_info = auth_service.is_logged_in()

        if user_info:
            exp_time = datetime.datetime.utcfromtimestamp(user_info["expires_at"])
            print(f"✅ Connecté en tant que : {user_info['email']}")
            print(f"🔑 ID utilisateur : {user_info['id']}")
            print(f"📅 Expiration du token : {exp_time} UTC")
        else:
            print("❌ Aucun utilisateur connecté.")
