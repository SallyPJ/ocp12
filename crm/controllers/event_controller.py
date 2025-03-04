from dao.event_dao import EventDAO
from dao.contract_dao import ContractDAO
from services.permissions import require_permission
from controllers.base_controller import BaseController


class EventController(BaseController):
    """Gère les événements en lecture seule."""

    def __init__(self, session):
        super().__init__(session, EventDAO)
        self.contract_dao = ContractDAO(session)

    @require_permission("read_all_events")
    def list_events(self, all=False, **filters):
        """Lists filtered events (if all = True, retrieve all events"""
        events = self.dao.get_filtered_events(all_events=all, **filters)
        if not events:
            return ["Aucun événement trouvé."]

        return [f"{e.id} - {e.name}, Lieu: {e.location}, Participants: {e.attendees}" for e in events]

    @require_permission("read_all_events")
    def get_event(self, event_id):
        """Retrieves a specific event by id"""
        event = self.dao.get_by_id(event_id)
        if not event:
            return "❌ Événement non trouvé."
        return f"Événement {event.id} - {event.name}, Lieu: {event.location}, Participants: {event.attendees}"

    @require_permission("create_events")
    def create_event(
        self, name, contract_id, customer_id, start_date, end_date, support_contact, location, attendees, notes
    ):
        """Creates a new event if associated contract is signed"""
        contract = self.contract_dao.get_by_id(contract_id)
        if not contract:
            raise ValueError("❌ Contrat non trouvé.")

        if not contract.is_signed:
            raise ValueError("❌ Le contrat n'est pas signé, impossible de créer l'événement.")

        event = self.dao.create_event(
            name, contract_id, customer_id, start_date, end_date, support_contact, location, attendees, notes
        )
        return event  # ✅ Retourne l'événement créé

    @require_permission("edit_events")
    def update_event(self, event_id, **kwargs):
        """Updates an existing event"""
        event = self.event_dao.get_by_id(event_id)
        if not event:
            return "❌ Événement non trouvé."
        if event.support_contact != self.user_id or self.user.department_id != 4:
            return "�� Accès refusé : seul le commercial responsable ou un admin peut modifier un événement."

        for key, value in kwargs.items():
            if value is not None:
                setattr(event, key, value)

        self.event_dao.update(event, **kwargs)
        return f"✅ Événement {event.id} mis à jour avec succès."

    @require_permission("delete_event")
    def delete_event(self, event_id):
        """Deletes an event"""
        event = self.dao.get_by_id(event_id)
        if not event:
            return "❌ Événement non trouvé."

        self.dao.delete(event)
        return f"✅ Événement {event.id} supprimé."
