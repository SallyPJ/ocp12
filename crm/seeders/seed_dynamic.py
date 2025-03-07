import yaml
from sqlalchemy.orm import Session
from models.user import User
from models.customer import Customer
from models.contract import Contract
from models.event import Event


def load_yaml_data(file_path):
    """Charge les données dynamiques depuis un fichier YAML."""
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def seed_dynamic_data(session: Session):
    """Insère les données dynamiques depuis un fichier YAML."""
    data = load_yaml_data("crm/seeders/seed_data.yaml")

    # 🔹 Seed des utilisateurs (Commence par les utilisateurs)
    print("⚙️ Insertion des utilisateurs...")
    users = {}
    for user_data in data["users"]:
        # Vérifiez si l'email de l'utilisateur existe déjà
        existing_user = session.query(User).filter_by(email=user_data["email"]).first()
        if existing_user:
            print(f"Utilisateur avec l'email {user_data['email']} déjà existant. Passage à l'utilisateur suivant.")
            continue
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
            department_id=user_data["department_id"],
            active=True,
        )
        session.add(user)
        session.flush()
        users[user_data["email"]] = user.id

    session.commit()  # Commit après avoir inséré tous les utilisateurs pour que les IDs soient générés
    print("✅ Utilisateurs insérés")

    # 🔹 Seed des clients (Assurez-vous que les utilisateurs commerciaux sont créés avant)
    print("⚙️ Insertion des clients...")
    for customer_data in data["customers"]:
        customer = Customer(
            first_name=customer_data["first_name"],
            last_name=customer_data["last_name"],
            email=customer_data["email"],
            phone=customer_data["phone"],
            enterprise=customer_data.get("enterprise", ""),
            sales_contact=customer_data["sales_contact"],  # Référence à un commercial existant
        )
        session.add(customer)

    session.commit()  # Commit après avoir inséré tous les clients
    print("✅ Clients insérés")

    # 🔹 Seed des contrats (Les contrats sont associés à des clients existants)
    print("⚙️ Insertion des contrats...")
    for contract_data in data["contracts"]:
        contract = Contract(
            customer_id=contract_data["customer_id"],
            total_amount=contract_data["total_amount"],
            due_amount=contract_data["due_amount"],
            is_signed=contract_data["is_signed"],
            sales_contact=contract_data["sales_contact"],  # Référence à un commercial existant
        )
        session.add(contract)

    session.commit()  # Commit après avoir inséré tous les contrats
    print("✅ Contrats insérés")

    # 🔹 Seed des événements (Les événements sont associés à des contrats et clients existants)
    print("⚙️ Insertion des événements...")
    for event_data in data["events"]:
        event = Event(
            name=event_data["name"],
            contract_id=event_data["contract_id"],
            customer_id=event_data["customer_id"],
            start_date=event_data["start_date"],
            end_date=event_data["end_date"],
            support_contact=event_data.get("support_contact", None),  # support_contact peut être None
            location=event_data["location"],
            attendees=event_data["attendees"],
            notes=event_data["notes"],
        )
        session.add(event)

    session.commit()  # Commit après avoir inséré tous les événements
    print("✅ Événements insérés avec succès.")
