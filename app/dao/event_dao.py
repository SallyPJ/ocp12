from models.event import Event

class EventDAO:
    """Accès aux données événements (lecture seule)."""

    def __init__(self, session):
        self.session = session

    def get_all(self):
        """Récupère tous les événements."""
        return self.session.query(Event).all()

    def get_by_id(self, event_id):
        """Récupère un événement par ID."""
        return self.session.query(Event).filter_by(id=event_id).first()