from sqlalchemy.orm import Session
from models import Department, User
from models import Permission
from models import department_permissions
from services.constants import DEPARTMENTS, PERMISSIONS, DEPARTMENT_PERMISSIONS
from passlib.hash import argon2
from controllers import UserController
from services.token_services import save_tokens


def seed_permissions(session: Session):
    """Seeds the database with fixed permission IDs and names."""
    for perm_data in PERMISSIONS.values():
        perm_id = perm_data["id"]
        perm_name = perm_data["name"]

        exists = session.query(Permission).filter_by(id=perm_id).first()
        if not exists:
            session.add(Permission(id=perm_id, name=perm_name))

    session.commit()
    print("✅ Permissions seeded")


def seed_departments(session: Session):
    """Seeds the database with fixed department IDs and names."""
    for dept_data in DEPARTMENTS.values():
        dept_id = dept_data["id"]
        dept_name = dept_data["name"]

        exists = session.query(Department).filter_by(id=dept_id).first()
        if not exists:
            session.add(Department(id=dept_id, name=dept_name))

    session.commit()
    print("✅ Departments seeded")


def seed_department_permissions(session: Session):
    """Links departments to permissions using fixed IDs from constants.py."""

    for department_name, permission_keys in DEPARTMENT_PERMISSIONS.items():
        # Get department ID
        department_id = DEPARTMENTS[department_name]["id"]

        for permission_key in permission_keys:
            permission_id = PERMISSIONS[permission_key]["id"]

            # Check if the entry already exists
            exists = session.execute(
                department_permissions.select().where(
                    (department_permissions.c.department_id == department_id)
                    & (department_permissions.c.permission_id == permission_id)
                )
            ).first()

            if not exists:
                session.execute(
                    department_permissions.insert().values(department_id=department_id, permission_id=permission_id)
                )

    session.commit()
    print("✅ Department permissions seeded ")


def ensure_admin_exists(session: Session):
    """Vérifie s'il existe au moins un administrateur, sinon en crée un."""
    # ✅ Vérifier si au moins un administrateur est présent
    admin_count = session.query(User).join(Department).filter(Department.name == "Admin").count()

    if admin_count == 0:
        print("🚨 Aucun administrateur trouvé ! Création d'un Super Admin...")

        # ✅ Vérifier si le département Admin existe, sinon le créer
        admin_department = session.query(Department).filter_by(name="Admin").first()
        if not admin_department:
            admin_department = Department(name="Admin")
            session.add(admin_department)
            session.commit()

        # ✅ Création d'un Super Admin par défaut
        super_admin = User(
            first_name="Admin",
            last_name="EpicEvents",
            email="admin@epicevents.com",
            department_id=admin_department.id,
            password=argon2.hash("AdminPass123!"),  # ✅ Mot de passe sécurisé
        )

        session.add(super_admin)
        session.commit()
        print("✅ Super Admin créé avec succès.")
    else:
        print("✅ Un administrateur est déjà présent.")


def populate_db(session: Session):
    """Ajoute les utilisateurs à la base avec les bons départements."""

    # ✅ Récupérer les départements
    sales_department = session.query(Department).filter_by(name="Sales").first()
    management_department = session.query(Department).filter_by(name="Management").first()
    support_department = session.query(Department).filter_by(name="Support").first()

    # ✅ Vérifier que les départements existent bien
    if not sales_department or not management_department or not support_department:
        print("❌ Erreur: Les départements ne sont pas créés.")
        return

    # ✅ Instancier le contrôleur utilisateur
    user_controller = UserController(session)

    # ✅ Ajouter des utilisateurs
    user_controller.create_user("Alice", "Dupont", "alice.sales@epicevents.com", "SalesPass123!", sales_department.id)
    user_controller.create_user("Bob", "Martin", "bob.sales@epicevents.com", "SalesPass123!", sales_department.id)
    user_controller.create_user(
        "Carla", "Durand", "carla.management@epicevents.com", "MgmtPass123!", management_department.id
    )
    user_controller.create_user(
        "David", "Bernard", "david.support@epicevents.com", "SupportPass123!", support_department.id
    )

    print("✅ Base de données peuplée avec succès.")
