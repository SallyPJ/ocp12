class EventView:
    """Manage event display for CLI"""

    @staticmethod
    def no_events_found():
        return "Aucun événement trouvé."

    @staticmethod
    def display_events(events):
        """Formats a list of events for display.

        This method takes a list of event objects and converts each event
        into a human-readable string using the `format_event` method.
        The formatted events are then joined into a single string, separated by new lines.

        Args:
            events (list): A list of event objects.

        Returns:
            str: A formatted string containing all events, each on a new line.
        """
        return "\n".join([EventView.format_event(event) for event in events])

    @staticmethod
    def display_event(event):
        """Formats a single event for display.

    This method calls `format_event` to convert the event object into
    a readable string format.

    Args:
        event: The event object to be formatted.

    Returns:
        str: Formatted event details.
    """
        return EventView.format_event(event)

    @staticmethod
    def format_event(event):
        """Converts an event object into a human-readable string"""
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
