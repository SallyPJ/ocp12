from models.event import Event


class EventDAO:
    """Accès aux données événements (lecture seule)."""

    def __init__(self, session):
        self.session = session

    def get_all(self):
        """Retrieves all events."""
        return self.session.query(Event).all()

    def get_by_id(self, event_id):
        """Retrieves an event by ID"""
        return self.session.query(Event).filter_by(id=event_id).first()

    def get_event_by_contract_id(self, contract_id):
        """Retrieves an event by contract"""
        return self.session.query(Event).filter_by(contract_id=contract_id).first()

    def get_filtered_events(self, all_events=False, **filters):
        """
        Retrieves events based on optional filters
        """
        query = self.session.query(Event)

        if not all_events:
            if filters.get("no_support"):
                query = query.filter(Event.support_contact == None)
            if filters.get("location"):
                query = query.filter(Event.location.ilike(f"%{filters['location']}%"))
            if filters.get("start_date"):
                query = query.filter(Event.start_date >= filters["start_date"])
            if filters.get("end_date"):
                query = query.filter(Event.end_date <= filters["end_date"])
            if filters.get("support_contact"):
                query = query.filter(Event.support_contact == filters["support_contact"])

        return query.all()

    def create_event(
        self, name, contract_id, customer_id, start_date, end_date, support_contact, location, attendees, notes
    ):
        """Creates a new event and adds it to the database"""
        new_event = Event(
            name=name,
            contract_id=contract_id,
            customer_id=customer_id,
            start_date=start_date,
            end_date=end_date,
            support_contact=support_contact,
            location=location,
            attendees=attendees,
            notes=notes,
        )
        self.session.add(new_event)

        return new_event

    def update(self, event, **kwargs):
        """Updates an existing event."""
        for key, value in kwargs.items():
            setattr(event, key, value)


    def delete(self, event):
        """Deletes an event from the database"""
        self.session.delete(event)



