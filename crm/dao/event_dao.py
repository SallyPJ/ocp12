from models.event import Event


class EventDAO:
    """Accès aux données événements (lecture seule)."""

    def __init__(self, session):
        self.session = session

    def get_all(self):
        """Récupère tous les événements."""
        return self.session.query(Event).all()

    def get_by_name(self, name):
        """Récupère un événement par nom."""
        return self.session.query(Event).filter_by(name=name).first()


    def get_filtered_events(self, all_events=False, **filters):
        """
        Récupère les événements selon les filtres.
        - Si `all_events=True`, retourne tous les événements.
        - Sinon, applique les filtres disponibles.
        """
        query = self.session.query(Event)

        if not all_events:
            if filters.get('no_support'):
                query = query.filter(Event.support_contact == None)
            if filters.get('location'):
                query = query.filter(Event.location.ilike(f"%{filters['location']}%"))
            if filters.get('start_date'):
                query = query.filter(Event.start_date >= filters['start_date'])
            if filters.get('end_date'):
                query = query.filter(Event.end_date <= filters['end_date'])
            if filters.get('support_contact'):
                query = query.filter(Event.support_contact == filters['support_contact'])

        return query.all()

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