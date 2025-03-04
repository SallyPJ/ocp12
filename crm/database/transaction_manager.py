from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import DATABASE_URL

# Initialisation de l'engine et de la fabrique de sessions
engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
db_session = scoped_session(SessionFactory)


class TransactionManager:
    """Gestionnaire de transaction contextuel.
    Ouvre une session, effectue commit en l'absence d'erreur, sinon rollback,
    puis nettoie la session."""

    def __enter__(self):
        self.session = db_session()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type:
                self.session.rollback()
                print(f"🔴 Transaction échouée : {exc_value}")
            else:
                self.session.commit()
                print("✅ Transaction validée avec succès.")
        finally:
            self.session.close()
