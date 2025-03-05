from dao.user_dao import UserDAO
from services.permissions import require_permission
from controllers.base_controller import BaseController
from views.user_view import UserView


class UserController(BaseController):
    """Manage user's actions without interaction with DB"""

    def __init__(self, session):
        super().__init__(session, UserDAO)
        self.view = UserView()

    @require_permission("read_all_employees")
    def list_users(self):
        """Lists all users"""
        users = self.dao.get_all()
        if not users:
            return self.view.no_user_found()
        return users



    @require_permission("create_employees")
    def create_user(self, first_name, last_name, email, password, department_id, active=True):
        """Creates a new user with business rules"""
        if self.dao.exists(email):
            return self.view.user_exists()

        user = self.dao.create(first_name, last_name, email, password, department_id, active)
        return self.view.user_created(user)

    @require_permission("edit_employees")
    def update_user(self, user_id, **kwargs):
        """Updates an existing user's information"""
        user = self.dao.get_by_id(user_id)
        if not user:
            return self.view.user_not_found()

        updates = {k: v for k, v in kwargs.items() if v is not None}
        self.dao.update(user, **updates)
        return self.view.user_updated(user)

    @require_permission("delete_employees")
    def delete_user(self, user_id):
        """Deletes a user"""
        user = self.dao.get_by_id(user_id)
        if not user:
            return self.view.user_not_found()

        self.dao.delete(user)
        return self.view.user_deleted(user)

    @require_permission("edit_employees")
    def deactivate_user(self, user_id):
        """Deactivates a user"""
        user = self.dao.get_by_id(user_id)
        if not user:
            return self.view.user_not_found()

        self.dao.deactivate_user(user_id)
        return self.view.user_deactivated(user)

