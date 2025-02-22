from dao import UserDAO
from db.transaction_manager import TransactionManager
from models import User

class UserController:
    """Manages user-related operations and business logic."""

    def __init__(self, session):
        """Takes a session instance to ensure proper session management."""
        self.session = session  # ✅ Store session in the controller
        self.user_dao = UserDAO(self.session)  # ✅ Pass session to DAO

    def create_user(self, first_name, last_name, email, password, department_id):
        """Creates a new user and ensures transaction integrity."""
        with TransactionManager() as session:  # ✅ Use TransactionManager
            user_dao = UserDAO(session)

            if user_dao.get_by_email(email):
                return "❌ A user with this email already exists."

            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                department_id=department_id
            )
            user.set_password(password)  # ✅ Hash the password

            user_dao.save(user)  # ✅ Auto-commit or rollback handled
            return f"✅ User {user.email} created successfully."

