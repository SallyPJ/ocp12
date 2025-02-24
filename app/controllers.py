from dao import UserDAO, CustomerDAO
from sqlalchemy.orm import Session
from database.transaction_manager import TransactionManager
from models import User
from services.token_services import require_auth
from services.permissions import require_permission
from database.transaction_manager import TransactionManager
from services.auth_service import authenticate_user
from services.token_services import save_tokens
class AuthController:
    def login(self, email, password):
        """Authentifie l’utilisateur et sauvegarde les tokens via token_services.
        La gestion de la transaction se fait ici, dans le contrôleur."""
        with TransactionManager() as session:
            access_token, refresh_token = authenticate_user(session, email, password)
            if access_token:
                save_tokens(access_token, refresh_token)
                return True, "✅ Login successful. Token saved."
            else:
                return False, "❌ Login failed."

class UserController:
    def __init__(self, session):
        self.session = session
        self.user_dao = UserDAO(self.session)

    def create_user(self, first_name, last_name, email, password, department_id, **kwargs):
        if self.user_dao.exists(email):
            return "❌ Un utilisateur avec cet email existe déjà."
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department_id=department_id,
            password=password
        )
        self.user_dao.save(new_user)
        return f"✅ L'utilisateur {new_user.email} a été créé avec succès."

class CustomerController:
    """Gère la logique métier pour les clients."""

    def __init__(self):
        pass  # ✅ Plus besoin de stocker la session ici, elle vient des kwargs

    @require_auth
    @require_permission("READ_ALL")  # ✅ Vérifie si l'utilisateur peut voir tous les clients
    def get_all_customers(self, **kwargs):
        """Récupère tous les clients pour l'utilisateur authentifié."""
        session = kwargs["session"]
        customer_dao = CustomerDAO(session)
        return customer_dao.get_all_customers()

    @require_permission("CREATE_CUSTOMER")  # ✅ Vérifie si l'utilisateur peut ajouter un client
    def add_customer(self, name, email, phone, enterprise, **kwargs):
        """Ajoute un client à la base de données."""
        session = kwargs["session"]
        customer_dao = CustomerDAO(session)

        new_customer = customer_dao.save_customer(name, email, phone, enterprise)

        if new_customer:
            return f"✅ Client '{name}' ajouté avec succès !"
        else:
            return "❌ Erreur lors de l'ajout du client."

class ContractController:
    """Gère la logique métier pour les contrats."""

    def __init__(self):
        pass


    @require_permission("READ_ALL")
    def get_all_contracts(self, **kwargs):
        """Récupère tous les contrats pour l'utilisateur authentifié."""
        session = kwargs["session"]
        contract_dao = ContractDAO(session)
        return contract_dao.get_all_contracts()

class EventController:
    """Gère la logique métier pour les événements."""

    def __init__(self):
        pass


    @require_permission("READ_ALL")
    def get_all_events(self, **kwargs):
        """Récupère tous les événements pour l'utilisateur authentifié."""
        session = kwargs["session"]
        event_dao = EventDAO(session)
        return event_dao.get_all_events()

class EventController:
    """Gère la logique métier pour les événements."""

    def __init__(self):
        pass

    @require_permission("READ_ALL")
    def get_all_events(self, **kwargs):
        """Récupère tous les événements pour l'utilisateur authentifié."""
        session = kwargs["session"]
        event_dao = EventDAO(session)
        return event_dao.get_all_events()