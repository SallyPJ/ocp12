from dao.event_dao import EventDAO

class EventController:
    """Gère les événements en lecture seule."""

    def __init__(self, session):
        self.event_dao = EventDAO(session)

    def list_events(self):
        """Retourne la liste de tous les événements."""
        events = self.event_dao.get_all()
        if not events:
            return ["Aucun événement trouvé."]
        return [f"{e.id} - {e.name}, Lieu: {e.location}, Participants: {e.attendees}" for e in events]

    def get_event(self, event_id):
        """Retourne un événement spécifique."""
        event = self.event_dao.get_by_id(event_id)
        if not event:
            return "❌ Événement non trouvé."
        return f"Événement {event.id} - {event.name}, Lieu: {event.location}, Participants: {event.attendees}"
