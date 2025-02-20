from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Sales, Support, Admin, Customer, Contract, Event

# Connexion à la base MySQL
DATABASE_URL = "mysql+pymysql://root:RAqxOFRMOrmEJkY@localhost/epic_events_crm_dev"
engine = create_engine(DATABASE_URL, echo=True)

# Création de la session
Session = sessionmaker(bind=engine)
session = Session()

# Supprimer et recréer les tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
# Supprimer toutes les données des tables (dans l'ordre des dépendances)
session.query(Event).delete()
session.query(Contract).delete()
session.query(Customer).delete()
session.query(User).delete()
session.commit()

print("✅ Toutes les entrées ont été supprimées.")
# Création des tables
Base.metadata.create_all(engine)

# Ajouter un commercial (Sales)
sales_user = Sales(first_name="Alice", last_name="Dupont", email="alice.dupont@email.com", role="sales")
sales_user.set_password("password123")

# Ajouter un membre support
support_user = Support(first_name="Bob", last_name="Martin", email="bob.martin@email.com", role="support")
support_user.set_password("password123")

# Ajouter un administrateur
admin_user = Admin(
    first_name="Bernadette",
    last_name="Pougnat",
    email="berna.pougnat@email.com",
    role="admin",
)
admin_user.set_password("password123")
# Insérer dans la base
session.add_all([sales_user, support_user, admin_user])
session.commit()

print(f"Sales ID: {sales_user.id}, Support ID: {support_user.id}, Admin ID: {admin_user.id}")

new_customer = Customer(
    name="Marie Vernard",
    email="mariv@startup.io",
    phone="+6 22336655",
    enterprise="Super Startup LLC",
    sales_contact=sales_user.id,
)

session.add(new_customer)
session.commit()

print(f"Customer ajouté avec ID {new_customer.id}")

new_contract = Contract(
    customer_id=new_customer.id,
    sales_contact=sales_user.id,
    total_amount=11000,
    due_amount=2000,
    status="signed",
)

session.add(new_contract)
session.commit()

print(f"Contrat ajouté avec ID {new_contract.id}")

new_event = Event(
    name="Fête du vin",
    contract_id=new_contract.id,
    customer_id=new_customer.id,
    start_date="2025-03-01 14:30:00",
    end_date="2025-03-01 18:00:00",
    support_contact=support_user.id,  # Associe cet événement à Bob du Support
    location="Marseille, France",
    attendees=30,
    notes="Prévoir au moins 10 tonneaux.",
)

session.add(new_event)
session.commit()

print(f"Événement '{new_event.name}' ajouté avec ID {new_event.id}")
