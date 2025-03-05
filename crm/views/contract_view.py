class ContractView:
    """Handles contract display for CLI"""

    @staticmethod
    def no_contracts_found():
        return "❌ Aucun contrat trouvé."

    @staticmethod
    def contract_not_found():
        return "❌ Contrat non trouvé."

    @staticmethod
    def access_denied():
        return "❌ Vous n'êtes pas responsable de ce contrat."

    @staticmethod
    def error_message(message):
        return f"❌ {message}"

    @staticmethod
    def contract_created(contract):
        return f"✅ Contrat {contract.id} créé avec succès."

    @staticmethod
    def contract_updated(contract):
        return f"✅ Contrat {contract.id} mis à jour avec succès."

    @staticmethod
    def format_contracts(contracts):
        """Formate un ou plusieurs contrats en dictionnaire(s)."""

        def format_contract(c):
            """Formate un contrat unique en dictionnaire."""
            return {
                "ID": c.id,
                "Client": c.customer.name if c.customer else "N/A",
                "Commercial": f"{c.sales_contact_user.first_name} {c.sales_contact_user.last_name}" if c.sales_contact_user else "N/A",
                "Montant Total (€)": c.total_amount,
                "Montant dû (€)": c.due_amount,
                "Signé": "Oui" if c.is_signed else "Non",
                "Payé": "Oui" if c.due_amount == 0 else "Non",
                "Date Création": c.creation_date.strftime("%Y-%m-%d"),
                "Événement associé": c.event.name if c.event else "Aucun événement"
            }

        # ✅ Si `contracts` est une liste, appliquer `format_contract` sur chaque élément
        if isinstance(contracts, list):
            return [format_contract(c) for c in contracts]

        # ✅ Si `contracts` est un seul objet, retourner son format unique
        return format_contract(contracts)


