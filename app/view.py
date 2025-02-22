from dao.user_dao import UserDAO
from sqlalchemy.orm import sessionmaker
from config import engine
from models.user import User


Session = sessionmaker(bind=engine)

class UserController:
    """Handles user-related operations and business logic."""

    def __init__(self):
        self.session = Session()
        self.user_dao = UserDAO(self.session)

    def create_user(self, first_name, last_name, email, password, department_id):
        """Creates a new user with a hashed password."""
        if self.user_dao.get_by_email(email):
            return "❌ A user with this email already exists."

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department_id=department_id
        )
        user.set_password(password)  # ✅ Hashing the password before storing

        self.user_dao.save(user)
        return f"✅ User {user.email} created successfully."

    def get_user_info(self, email):
        """Retrieves user details."""
        user = self.user_dao.get_by_email(email)
        if not user:
            return "❌ User not found."

        return f"👤 {user.first_name} {user.last_name} | Email: {user.email} | Department: {user.department.name}"

    def delete_user(self, email):
        """Deletes a user from the system."""
        user = self.user_dao.get_by_email(email)
        if not user:
            return "❌ User not found."

        self.user_dao.delete(user)
        return f"✅ User {user.email} deleted successfully."

    def authenticate_user(self, email, password):
        """Authenticates a user by verifying the password."""
        user = self.user_dao.get_by_email(email)
        if not user or not user.check_password(password):
            return "❌ Incorrect email or password."

        return f"✅ Login successful! Welcome {user.first_name}."
