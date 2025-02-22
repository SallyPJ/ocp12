from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from sqlalchemy import create_engine

# Initialize database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

class TransactionManager:
    """Handles database transactions with automatic commit/rollback."""

    def __enter__(self):
        """Starts a new database session."""
        self.session = SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        """Commits or rolls back the transaction and closes the session."""
        if exc_type:
            self.session.rollback()  # ❌ Rollback on error
            print(f"🔴 Transaction failed: {exc_value}")
        else:
            self.session.commit()  # ✅ Commit on success
            print("✅ Transaction committed successfully.")
        self.session.close()  # 🔄 Ensure session is closed