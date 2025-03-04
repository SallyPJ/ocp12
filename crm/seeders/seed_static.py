from sqlalchemy.orm import Session
from models.permission import Permission
from models.department import Department
from models.department import department_permissions
from services.constants import PERMISSIONS, DEPARTMENTS, DEPARTMENT_PERMISSIONS


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
    print("✅ Department permissions seeded")


def seed_static_data(session: Session):
    """Seed departments, permissions, and department-permission relationships."""
    seed_permissions(session)
    seed_departments(session)
    seed_department_permissions(session)
    print("✅ Static data seeded successfully.")
