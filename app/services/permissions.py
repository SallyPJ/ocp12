import functools
from services.token_services import require_auth  # ✅ Vérifie l'authentification
from models import Permission  # ✅ Le modèle SQLAlchemy des permissions
from models import department_permissions  # ✅ La table d'association entre départements et permissions

def require_permission(required_permission):
    """Vérifie si l'utilisateur connecté a la permission requise."""
    def decorator(func):
        @require_auth  # ✅ Vérifie l'authentification avant la permission
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            session = kwargs.get("session")
            if session is None:
                # Si elle n'est pas présente, on la crée manuellement
                from db.transaction_manager import db_session
                session = db_session()
                kwargs["session"] = session

            user_payload = kwargs.get("user_payload")
            if not user_payload:
                print("❌ Erreur: user_payload manquant.")
                return None

            department_id = user_payload.get("department_id")
            if not department_id:
                print("❌ Erreur: department_id manquant dans le payload utilisateur.")
                return None

            # ✅ Vérifie si ce département a la permission requise
            permission_exists = (
                session.query(Permission)
                .join(department_permissions, department_permissions.c.permission_id == Permission.id)
                .filter(department_permissions.c.department_id == department_id)
                .filter(Permission.name == required_permission)
                .first()
            )

            if not permission_exists:
                print(f"❌ Permission refusée : Le département n'a pas '{required_permission}'.")
                return None

            return func(*args, **kwargs)
        return wrapper
    return decorator

