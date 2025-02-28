from dao.event_dao import EventDAO
from models.event import Event
from services.permissions import require_permission
from controllers.base_controller import BaseController


class EventController(BaseController):
    """Gère les événements en lecture seule."""

    def __init__(self, session):
        super().__init__(session, EventDAO)

    @require_permission("read_all_events")
    def list_events(self, all=False, **filters):
        """Retourne une liste d'événements filtrés par les critères fournis ou tous les événements si 'all' est True."""
        query = self.dao.session.query(Event)

        if not all:
            # Application dynamique des filtres
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

        events = query.all()

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



    def can_edit_event(self, event_id):
        """Vérifie si l'utilisateur a la permission de modifier un événement."""

        if self.permission_service.has_permission(self.user_id, "edit_all_events"):
            return True

        # Vérifier si l'utilisateur a la permission d'éditer son propre événement
        event = self.event_dao.get_by_id(event_id)
        if event and event.support_contact == self.user_id:
            if self.permission_service.has_permission(self.user_id, "edit_own_events"):
                return True
        # Si aucune condition n'est remplie, l'utilisateur n'a pas les droits
        return False

    @require_permission("edit_all_events")
    def update_event(self, event_id, **kwargs):
        """Met à jour un événement avec vérification des permissions."""
        if not self.can_edit_event(event_id):
            return "❌ Vous n'avez pas la permission de modifier cet événement."

        event = self.event_dao.get_by_id(event_id)
        if not event:
            return "❌ Événement non trouvé."

        for key, value in kwargs.items():
            if value is not None:
                setattr(event, key, value)

        self.event_dao.update(event, **kwargs)
        return f"✅ Événement {event.id} mis à jour avec succès."

    @require_permission("delete_event")
    def delete_event(self, event_id):
        """Supprime un événement."""
        event = self.dao.get_by_id(event_id)
        if not event:
            return "❌ Événement non trouvé."

        self.dao.delete(event)
        return f"✅ Événement {event.id} supprimé."
