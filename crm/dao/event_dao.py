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

    def save(self, event):
        """Ajoute un nouvel événement à la base de données."""
        self.session.add(event)
        self.session.commit()

    def update(self, event, **kwargs):
        """Met à jour un événement existant."""
        for key, value in kwargs.items():
            setattr(event, key, value)
        self.session.commit()

    def delete(self, event):
        """Supprime un événement."""
        self.session.delete(event)
        self.session.commit()