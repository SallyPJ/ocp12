import json
import os
import jwt
import datetime
import uuid
from dao.user_dao import UserDAO
from passlib.hash import argon2
from config import SECRET_KEY, REFRESH_SECRET_KEY, ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN

try:
    import keyring
    from keyring.errors import PasswordDeleteError

    # 🔐 Utilisation de keyring pour un stockage sécurisé
    SECURE_STORAGE = True
except ImportError:
    SECURE_STORAGE = False

SESSION_FILE = ".session"
ISSUER = "EpicEvents"
AUDIENCE = "epic-events-cli"


class AuthService:
    """Gère l'authentification et la gestion sécurisée des tokens JWT."""

    def __init__(self, session):
        self.user_dao = UserDAO(session)

    ## 🔹 UTILITAIRES PRIVÉS 🔹 ##



    def _read_session(self):
        """Lit les tokens stockés en session de manière sécurisée."""
        if SECURE_STORAGE:
            data = keyring.get_password("EpicEvents", "session")
            return json.loads(data) if data else {}
        elif os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as f:
                return json.load(f)
        return {}

    def _write_session(self, session_data):
        """Écrit les tokens de manière sécurisée."""
        data = json.dumps(session_data)
        if SECURE_STORAGE:
            keyring.set_password("EpicEvents", "session", data)
        else:
            with open(SESSION_FILE, "w") as f:
                f.write(data)

    def _clear_session(self):
        """Supprime le fichier de session sécurisé."""
        if SECURE_STORAGE:
            try:
                if keyring.delete_password("EpicEvents", "session") is not None:
                    keyring.delete_password("EpicEvents", "session")
            except PasswordDeleteError:
                pass  # ✅ Empê
        elif os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

    ## 🔹 GÉNÉRATION DES TOKENS 🔹 ##

    def _generate_token(self, user, expires_in, secret_key, token_type):
        """Génère un token JWT avec des mesures de sécurité renforcées."""
        payload = {
            "user_id": user.id,
            "password_hash": user._password[:10],  # Ajout d'une vérification d'intégrité
            "iss": ISSUER,
            "aud": AUDIENCE,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
            "type": token_type,
        }
        return jwt.encode(payload, secret_key, algorithm="HS256")

    def generate_tokens(self, user):
        """Génère un access_token et un refresh_token avec protection renforcée."""
        return (
            self._generate_token(user, ACCESS_TOKEN_EXPIRES_IN, SECRET_KEY, "access"),
            self._generate_token(user, REFRESH_TOKEN_EXPIRES_IN, REFRESH_SECRET_KEY, "refresh"),
        )

    ## 🔹 AUTHENTIFICATION 🔹 ##

    def login(self, email, password):
        """Vérifie les identifiants et connecte l'utilisateur de manière sécurisée."""
        user = self.user_dao.get_by_email(email)
        if not user or not argon2.verify(password, user._password):
            return "❌ Email ou mot de passe incorrect."

        access_token, refresh_token = self.generate_tokens(user)
        self._write_session({"access_token": access_token, "refresh_token": refresh_token})

        return "✅ Connexion réussie !"

    def logout(self):
        """Déconnecte l'utilisateur en supprimant les tokens."""
        self._clear_session()
        return "✅ Déconnexion réussie."

    ## 🔹 VALIDATION & RAFRAÎCHISSEMENT DES TOKENS 🔹 ##

    def _decode_token(self, token, secret_key):
        """Décode un JWT et applique des contrôles de sécurité."""
        try:
            decoded = jwt.decode(token, secret_key, algorithms=["HS256"], issuer=ISSUER, audience=AUDIENCE)
            return decoded
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None  # Token invalide ou expiré

    def decode_access_token(self, access_token):
        """Décode un access_token et retourne l'ID utilisateur."""
        return self._decode_token(access_token, SECRET_KEY)

    def refresh_token(self):
        """Génère un nouvel access_token avec validation stricte."""
        session_data = self._read_session()
        refresh_token = session_data.get("refresh_token")

        if not refresh_token:
            return None

        decoded = self._decode_token(refresh_token, REFRESH_SECRET_KEY)
        if not decoded or datetime.datetime.utcnow() > datetime.datetime.fromtimestamp(decoded["exp"]):
            return None  # Token expiré

        user = self.user_dao.get_by_id(decoded["user_id"])
        if not user or user._password[:10] != decoded["password_hash"]:
            return None  # Sécurité renforcée

        new_access_token, _ = self.generate_tokens(user)
        session_data["access_token"] = new_access_token
        self._write_session(session_data)

        return new_access_token

    def get_valid_access_token(self, refresh=True):
        """Vérifie si le token d'accès est valide, sinon tente un refresh automatique."""
        session_data = self._read_session()
        access_token = session_data.get("access_token")

        if not access_token:
            print("❌ Aucun access_token trouvé en session.")
            return None

        decoded = self._decode_token(access_token, SECRET_KEY)
        if decoded:
            return access_token  # ✅ Le token est encore valide

        # 🔄 Si expiré, on tente un refresh
        if refresh:  # ✅ On ne tente un refresh QUE si c’est autorisé
            print("🔄 Tentative de refresh du token...")
            new_access_token = self.refresh_token()
            if new_access_token:
                session_data["access_token"] = new_access_token
                self._write_session(session_data)
                print(f"✅ Nouveau token généré ")  # 🔍 Vérification
                return new_access_token

        print("❌ Aucun token valide disponible après refresh.")  # 🔍 Vérification
        return None

    def is_logged_in(self):
        """Vérifie si un utilisateur est connecté et retourne ses informations."""
        session_data = self._read_session()
        access_token = session_data.get("access_token")

        if not access_token:
            return None  # Aucun utilisateur connecté

        decoded = self._decode_token(access_token, SECRET_KEY)
        if not decoded:
            return None  # Token invalide ou expiré

        user_id = decoded.get("user_id")
        user = self.user_dao.get_by_id(user_id)

        if user:
            return {
                "id": user.id,
                "email": user.email,
                "expires_at": decoded["exp"],
            }
        return None
