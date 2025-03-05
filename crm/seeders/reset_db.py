from sqlalchemy import create_engine, text
from models.base import Base
from config import DATABASE_URL  # Ton URL de base de données

# Connexion à l'engine initial (avant de supprimer la base)
engine = create_engine(DATABASE_URL, echo=True)


def reset_database():
    """Supprime et recrée la base de données."""
    # Connexion manuelle pour gérer la création de base de données
    with engine.connect() as conn:
        # Suppression de la base de données existante
        print("⚠️ Suppression de la base de données...")
        conn.execute(text("DROP DATABASE IF EXISTS epic_events_crm_dev;"))

        # Création de la base de données
        print("🚀 Création de la base de données...")
        conn.execute(text("CREATE DATABASE epic_events_crm_dev;"))

    # Assurez-vous que l'URL pointe vers la base créée
    new_database_url = DATABASE_URL.replace(
        "epic_events_crm_dev", "epic_events_crm_dev"
    )  # Remplacer le nom de la DB ici si nécessaire
    new_engine = create_engine(new_database_url, echo=True)  # Connexion à la nouvelle base

    # Recréation des tables
    print("🔄 Recréation des tables...")
    try:
        Base.metadata.create_all(new_engine)
        print("✅ Tables recréées avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {str(e)}")

    # Vérification des tables dans la base
    with new_engine.connect() as conn:
        result = conn.execute(text("SHOW TABLES"))
        print(f"🛠️ Tables dans la base de données après création : {[row[0] for row in result]}")


if __name__ == "__main__":
    reset_database()
