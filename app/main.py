from models import Base, Department
from controllers import UserController
from services.seed import seed_departments
from db.transaction_manager import TransactionManager  # ✅ Uses centralized session management
from services.seed import seed_permissions, seed_departments, seed_department_permissions

# ✅ Use TransactionManager for session handling
with TransactionManager() as session:
    # Drop and recreate tables (inside transaction scope)
    Base.metadata.drop_all(session.bind)
    Base.metadata.create_all(session.bind)

    # Seed departments
    seed_permissions(session)  # ✅ Step 1: Seed permissions
    seed_departments(session)  # ✅ Step 2: Seed departments
    seed_department_permissions(session)  # ✅ Step 3: Assign permissions using fixed IDs

    # Fetch department ID
    sales_department = session.query(Department).filter_by(name="Sales").first()

    # Initialize UserController with session
    user_controller = UserController(session)  # ✅ Pass managed session

    # 🔹 Create a new user
    print(user_controller.create_user(
        first_name="Bob",
        last_name="Dupont",
        email="bob.sales@epicevents.com",
        password="password123",
        department_id=sales_department.id
    ))
