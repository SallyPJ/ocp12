class ContractView:
    """Handles contract display for CLI interactions."""

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
    def contract_signed_message(contract):
        return f"📜 Contrat signé : ID {contract.id} - Client {contract.customer.name}"

    @staticmethod
    def customer_not_found_message(customer_id):
        return f"❌ Client ID {customer_id} introuvable."

    @staticmethod
    def customer_no_sales_contact_message(customer_id):
        return f"❌ Le client ID {customer_id} n'a pas de commercial assigné."

    @staticmethod
    def format_contracts(contracts):
        """Formats one or multiple contracts into dictionaries for display.

        Args:
            contracts: A single contract object or a list of contracts.

        Returns:
            dict or list: Formatted contract details.
        """

        def format_contract(c):
            """Formats a single contract into a dictionary.

            Args:
                c: The contract object to be formatted.

            Returns:
                dict: Formatted contract details.
            """
            return {
                "ID": c.id,
                "Client": c.customer.name if c.customer else "N/A",
                "Commercial": (
                    f"{c.sales_contact_user.first_name} {c.sales_contact_user.last_name}"
                    if c.sales_contact_user
                    else "N/A"
                ),
                "Montant Total (€)": c.total_amount,
                "Montant dû (€)": c.due_amount,
                "Signé": "Oui" if c.is_signed else "Non",
                "Payé": "Oui" if c.due_amount == 0 else "Non",
                "Date Création": c.creation_date.strftime("%Y-%m-%d"),
                "Événement associé": c.event.name if c.event else "Aucun événement",
            }

        # If `contracts` is a list, apply `format_contract` to each item
        if isinstance(contracts, list):
            return [format_contract(c) for c in contracts]

        #  If `contracts` is a single object, return its formatted version
        return format_contract(contracts)
