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
        return [
            {
                "ID": customer.id,
                "Prénom": customer.first_name,
                "Nom": customer.last_name,
                "Email": customer.email,
                "Téléphone": customer.phone or "N/A",
                "Entreprise": customer.enterprise or "N/A",
                "Date de création": customer.creation_date.strftime("%Y-%m-%d"),
                "Dernier contact": customer.last_update.strftime("%Y-%m-%d") if customer.last_update else "N/A",
                "Contact Sales": (
                    f"{customer.sales_rep.first_name} {customer.sales_rep.last_name}"
                    if customer.sales_rep
                    else "Aucun commercial assigné"
                ),
            }
            for customer in customers
        ]

    @staticmethod
    def display_customer(customer):
        return CustomerView.format_customer(customer)

    @staticmethod
    def customer_created(customer):
        return f"✅ Client {customer.first_name} {customer.last_name} ({customer.email}) ajouté avec succès."

    @staticmethod
    def customer_updated(customer):
        return f"✅ Client {customer.first_name} {customer.last_name} mis à jour avec succès."

    @staticmethod
    def format_customer(customer):
        """Format a single customer with all relevant details."""
        return (
            f"📌 ID : {customer.id}\n"
            f"👤 Prénom : {customer.fist_name}\n"
            f"👤 Nom : {customer.last_name}\n"
            f"📧 Email : {customer.email}\n"
            f"📞 Téléphone : {customer.phone or 'N/A'}\n"
            f"🏢 Entreprise : {customer.enterprise or 'N/A'}\n"
            f"📅 Date de création : {customer.creation_date.strftime('%Y-%m-%d')}\n"
            f"🔄 Dernier contact : {customer.last_update.strftime('%Y-%m-%d') if customer.last_update else 'N/A'}\n"
            f"🧑‍💼 Contact commercial : {customer.sales_rep.first_name} {customer.sales_rep.last_name} "
            if customer.sales_rep
            else "Aucun commercial assigné"
        )

    @staticmethod
    def update_summary(update_fields):
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
        from rich.prompt import Confirm

        return Confirm.ask("Voulez-vous appliquer ces modifications ?", default=True)
