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
    def display_contracts(contracts):
        """Formate une liste de contrats"""
        return [
            {
                "ID": c.id,
                "Client": c.customer.name if c.customer else "N/A",
                "Commercial": f"{c.sales_contact_user.first_name} {c.sales_contact_user.last_name}" if c.sales_contact_user else "N/A",
                "Montant Total (€)": c.total_amount,
                "Montant dû (€)": c.due_amount,
                "Signé": "Oui" if c.is_signed else "Non",
                "Payé": "Oui" if c.due_amount == 0 else "Non",
                "Date Création": c.creation_date.strftime("%Y-%m-%d"),
            }
            for c in contracts
        ]

    @staticmethod
    def display_contract(contract):
        """Formate un contrat unique"""
        return {
            "ID": contract.id,
            "Client": contract.customer.name if contract.customer else "N/A",
            "Commercial": f"{contract.sales_contact_user.first_name} {contract.sales_contact_user.last_name}" if contract.sales_contact_user else "N/A",
            "Montant Total (€)": contract.total_amount,
            "Montant dû (€)": contract.due_amount,
            "Signé": "Oui" if contract.is_signed else "Non",
            "Payé": "Oui" if contract.due_amount == 0 else "Non",
            "Date Création": contract.creation_date.strftime("%Y-%m-%d"),
        }


