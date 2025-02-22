from sqlalchemy.orm import sessionmaker, scoped_session
from config import DATABASE_URL
from sqlalchemy import create_engine

# ✅ Initialize database engine
engine = create_engine(DATABASE_URL, echo=True)

# ✅ Create a session factory
SessionFactory = sessionmaker(bind=engine)

# ✅ Use `scoped_session` for managing session lifecycle per thread
session = scoped_session(SessionFactory)

class TransactionManager:
    """Manages database transactions globally using context management."""

    def __enter__(self):
        """Starts a new session when entering the context."""
        self.session = session  # ✅ Use the global session
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        """Commits or rolls back transactions and closes session."""
        if exc_type:
            self.session.rollback()  # ❌ Rollback if an error occurs
            print(f"🔴 Transaction failed: {exc_value}")
        else:
            self.session.commit()  # ✅ Commit changes if no errors
            print("✅ Transaction committed successfully.")
        self.session.remove()  # 🔄 Ensure session cleanup