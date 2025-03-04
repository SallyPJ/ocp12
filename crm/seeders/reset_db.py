from sqlalchemy import create_engine, text
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def reset_database():
    """Supprime et recrée la base de données."""
    # Connexion manuelle pour gérer la création de base de données
    with engine.connect() as conn:
        # Suppression de la base de données existante
        print("⚠️ Suppression de la base de données...")
        conn.execute(text("DROP DATABASE IF EXISTS epic_events_crm_dev;"))


if __name__ == "__main__":
    reset_database()
