import functools
from services.token_service import TokenService
from config import SECRET_KEY


def require_auth(func):
    """Decorator that checks the validity of the token before executing a function."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        session_data = TokenService.read_session()
        access_token = session_data.get("access_token")
        refresh_token = session_data.get("refresh_token")

        if not access_token or not refresh_token:
            print("❌ Aucun token trouvé. Veuillez vous connecter.")
            return None

        decoded = TokenService.decode_token(access_token, SECRET_KEY)

        if decoded:
            self.user_id = decoded.get("user_id")  #
            return func(self, *args, **kwargs)

        # 🔄 Tentative de refresh si le token est expiré
        print("🔄 Tentative de refresh du token...")
        new_access_token = TokenService.refresh_access_token()

        if new_access_token:
            print("🔄 Token rafraîchi automatiquement !")
            decoded = TokenService.decode_token(new_access_token, SECRET_KEY)
            if decoded:
                self.user_id = decoded.get("user_id")
                return func(self, *args, **kwargs)

        print("❌ Aucun token valide disponible après rafraîchissement.")
        return None

    return wrapper


def require_permission(permission_name):
    """Decorator that check permissions by department."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "user_id") or self.user_id is None:  # ✅ Vérification propre
                print("🔴 Action refusée : Vous devez être connecté pour effectuer cette action.")
                return
            # ✅ Debug
            if not self.permission_service.has_permission(self.user_id, permission_name):
                return ["❌ Permission refusée."]

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
