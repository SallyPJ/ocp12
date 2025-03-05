from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import DATABASE_URL

# Initialisation de l'engine et de la fabrique de sessions
engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
db_session = scoped_session(SessionFactory)


class TransactionManager:
    """Context manager for handling database transactions.
    It opens a session, commits the transaction if no error occurs,
    otherwise performs a rollback, and then cleans up the session."""

    def __enter__(self):
        """Initialize and return a new database session."""
        self.session = db_session()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Handles transaction closure:
        - If an exception occurs, rollback the transaction.
        - Otherwise, commit the changes.
        - Finally, close the session to free resources.
        """
        try:
            if exc_type:
                self.session.rollback()
                print(f"🔴 Transaction échouée : {exc_value}")
            else:
                self.session.commit()

        finally:
            self.session.close()
