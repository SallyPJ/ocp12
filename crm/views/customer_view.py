class CustomerView:
    """Handles customer display for CLI"""

    @staticmethod
    def no_customers_found():
        return "Aucun client trouvé."

    @staticmethod
    def customer_not_found():
        return "❌ Client non trouvé."

    @staticmethod
    def access_denied():
        return "❌ Vous n'êtes pas responsable de ce client."

    @staticmethod
    def no_changes_provided():
        return "❌ Aucun changement spécifié."

    @staticmethod
    def update_cancelled():
        return "❌ Mise à jour annulée."

    @staticmethod
    def display_customers(customers):
        """Formate une liste d'objets clients en chaînes lisibles"""
        return [f"{customer.id} - {customer.name} ({customer.email})" for customer in customers]

    @staticmethod
    def display_customer(customer):
        """Formats and displays a single customer"""
        return CustomerView.format_customer(customer)

    @staticmethod
    def customer_created(customer):
        return f"✅ Client {customer.name} ({customer.email}) ajouté avec succès."

    @staticmethod
    def customer_updated(customer):
        return f"✅ Client {customer.name} mis à jour avec succès."

    @staticmethod
    def format_customer(customer):
        """Formats a customer object into a readable string"""
        return f"{customer.id} - {customer.name} ({customer.email})"

    @staticmethod
    def update_summary(update_fields):
        """Génère un résumé des mises à jour"""
        from rich.table import Table
        from rich.console import Console

        console = Console()
        table = Table(show_header=False, title="📌 Modifications prévues", header_style="bold cyan")
        for field, value in update_fields.items():
            table.add_row(field.capitalize(), str(value))

        console.print(table)
        return table

    @staticmethod
    def confirm_update(summary):
        """Demande confirmation avant de procéder à la mise à jour"""
        from rich.prompt import Confirm
        return Confirm.ask("Voulez-vous appliquer ces modifications ?", default=True)

