class EventView:
    """Manage event display for CLI"""

    @staticmethod
    def no_events_found():
        return "Aucun événement trouvé."

    @staticmethod
    def format_events(event):
        """Formats a single event into a dictionary for display"""
        return {
            "ID": event.id,
            "Nom": event.name,
            "Lieu": event.location,
            "Début": event.start_date.strftime("%Y-%m-%d %H:%M"),
            "Fin": event.end_date.strftime("%Y-%m-%d %H:%M"),
            "Participants": event.attendees,
            "Support": f"{event.support.first_name} {event.support.last_name}" if event.support else "Non assigné",
        }

    @staticmethod
    def display_events(events):
        """Formats a list of events for display in the CLI"""
        return [EventView.format_events(event) for event in events]

    @staticmethod
    def display_event(event):
        """Formats a single event for display.
        This method calls `format_event` to convert the event object into
        a readable string format.
        """
        return EventView.format_event(event)

    @staticmethod
    def format_event(event):
        """Converts an event object into a human-readable string"""
        return (
            f"📅 ID: {event.id} - {event.name}\n"
            f"📍 Lieu: {event.location}\n"
            f"👥 Participants: {event.attendees}\n"
            f"🕒 Début: {event.start_date.strftime('%Y-%m-%d %H:%M')}\n"
            f"🕕 Fin: {event.end_date.strftime('%Y-%m-%d %H:%M')}\n"
            f"📝 Notes: {event.notes or 'Aucune'}\n"
            f"🛠 Support: {event.support.first_name} {event.support.last_name}"
            if event.support
            else ""

        )

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
        return ("❌ Accès refusé : seuls le support responsable, "
                "l'équipe management et l'admin peuvent modifier un évènement")

    @staticmethod
    def event_updated(event_name):
        return f"✅ Événement '{event_name}' mis à jour avec succès."

    @staticmethod
    def event_deleted(event_name):
        return f"✅ Événement '{event_name}' supprimé."
