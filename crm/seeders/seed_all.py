import os
from database.transaction_manager import TransactionManager
from seeders.seed_static import seed_static_data
from seeders.seed_dynamic import seed_dynamic_data
from models.base import Base
from crm.config import DATABASE_URL
from sqlalchemy import create_engine


def run_seed():
    os.environ["SEEDING"] = "true"  # ✅ Active le mode seeding

    # Connexion à l'engine
    engine = create_engine(DATABASE_URL, echo=True)

    # Utilisation du TransactionManager pour gérer la création des tables
    with TransactionManager() as session:
        # Recréation des tables
        print("🔄 Recréation des tables...")
        Base.metadata.create_all(engine)
        print("✅ Tables créées avec succès.")

        # Seeder les données statiques
        print("\n🔹 Seeding des données statiques (Départements, Permissions)...")
        seed_static_data(session)

        # Seeder les données dynamiques
        print("\n📊 Seeding des données dynamiques (Utilisateurs, Clients, Contrats, Événements)...")
        seed_dynamic_data(session)

    os.environ["SEEDING"] = "false"  # ✅ Désactive après seeding
    print("\n🎉 ✅ SEED COMPLET : La base est prête à l'emploi !")


if __name__ == "__main__":
    run_seed()
