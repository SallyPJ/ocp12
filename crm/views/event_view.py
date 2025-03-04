class EventView:
    """Gère l'affichage des événements pour le CLI"""

    @staticmethod
    def no_events_found():
        return "Aucun événement trouvé."

    @staticmethod
    def display_events(events):
        """Formate une liste d'événements"""
        return "\n".join([EventView.format_event(event) for event in events])

    @staticmethod
    def display_event(event):
        """Formate un événement unique"""
        return EventView.format_event(event)

    @staticmethod
    def format_event(event):
        """Transforme un objet événement en chaîne de caractères lisible"""
        return f"{event.id} - {event.name}, Lieu: {event.location}, Participants: {event.attendees}"

    @staticmethod
    def contract_not_found():
        return "❌ Contrat non trouvé."

    @staticmethod
    def contract_not_signed():
        return "❌ Le contrat n'est pas signé, impossible de créer l'événement."

    @staticmethod
    def event_created(event_name):
        return f"✅ Événement '{event_name}' créé avec succès."

    @staticmethod
    def no_changes_provided():
        return "❌ Aucun changement fourni."

    @staticmethod
    def event_not_found():
        return "❌ Événement non trouvé."

    @staticmethod
    def access_denied():
        return "❌ Accès refusé : seul le commercial responsable ou un admin peut créer un événement."
    @staticmethod
    def access_for_modif_denied():
        return "❌ Accès refusé : seuls le support responsable, l'équipe management et l'admin peuvent modifier un évènement"
    @staticmethod
    def event_updated(event_name):
        return f"✅ Événement '{event_name}' mis à jour avec succès."

    @staticmethod
    def event_deleted(event_name):
        return f"✅ Événement '{event_name}' supprimé."
