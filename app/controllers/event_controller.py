from dao.event_dao import EventDAO
from models.event import Event
from services.permissions import require_permission
from controllers.base_controller import BaseController


class EventController(BaseController):
    """Gère les événements en lecture seule."""

    def __init__(self, session):
        super().__init__(session, EventDAO)

    @require_permission("read_all_events")
    def list_events(self):
        """Retourne la liste de tous les événements."""
        events = self.event_dao.get_all()
        if not events:
            return ["Aucun événement trouvé."]
        return [f"{e.id} - {e.name}, Lieu: {e.location}, Participants: {e.attendees}" for e in events]

    @require_permission("read_all_events")
    def get_event(self, event_id):
        """Retourne un événement spécifique."""
        event = self.event_dao.get_by_id(event_id)
        if not event:
            return "❌ Événement non trouvé."
        return f"Événement {event.id} - {event.name}, Lieu: {event.location}, Participants: {event.attendees}"

    @require_permission("create_event_for_client")
    def create_event(self, name, contract_id, customer_id, start_date, end_date, support_contact, location, attendees,
                     notes):
        """Crée un nouvel événement."""
        new_event = Event(
            name=name,
            contract_id=contract_id,
            customer_id=customer_id,
            start_date=start_date,
            end_date=end_date,
            support_contact=support_contact,
            location=location,
            attendees=attendees,
            notes=notes
        )
        self.dao.save(new_event)
        return f"✅ Événement '{name}' créé avec succès."

    @require_permission("edit_own_event")
    def update_event(self, event_id, **kwargs):
        """Met à jour un événement existant."""
        event = self.dao.get_by_id(event_id)
        if not event:
            return "❌ Événement non trouvé."

        self.dao.update(event, **kwargs)
        return f"✅ Événement {event.id} mis à jour avec succès."

    @require_permission("delete_event")
    def delete_event(self, event_id):
        """Supprime un événement."""
        event = self.dao.get_by_id(event_id)
        if not event:
            return "❌ Événement non trouvé."

        self.dao.delete(event)
        return f"✅ Événement {event.id} supprimé."