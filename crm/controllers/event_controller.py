from dao.event_dao import EventDAO
from dao.contract_dao import ContractDAO
from dao.user_dao import UserDAO
from decorators.auth_decorators import require_auth, require_permission
from controllers.base_controller import BaseController
from views.event_view import EventView


class EventController(BaseController):
    """Gère les événements en lecture seule."""

    def __init__(self, session):
        super().__init__(session, EventDAO)
        self.contract_dao = ContractDAO(session)
        self.user_dao = UserDAO(session)
        self.view = EventView()

    @require_auth
    @require_permission("read_all_events")
    def list_events(self, all=False, **filters):
        """Lists filtered events (if all = True, retrieve all events)"""
        events = self.dao.get_filtered_events(all_events=all, **filters)
        if not events:
            return self.view.no_events_found()
        return self.view.display_events(events)

    @require_auth

    @require_permission("read_all_events")
    def get_event(self, event_id):
        """Retrieves a specific event by ID"""
        event = self.dao.get_by_id(event_id)
        if not event:
            return self.view.no_event_found()
        return self.view.display_event(event)

    @require_auth

    @require_permission("create_events")
    def create_event(self, name, contract_id, start_date, end_date, support_contact, location, attendees, notes):
        """Creates a new event if associated contract is signed"""
        contract = self.contract_dao.get_by_id(contract_id)
        if not contract:
            return self.view.contract_not_found()

        if not contract.is_signed:
            return self.view.contract_not_signed()

        customer_id = contract.customer_id

        user = self.user_dao.get_by_id(self.user_id)
        if user.id != contract.sales_contact and user.department_id != 4:
            return self.view.access_denied()
        else:
            event = self.dao.create_event(
                name, contract_id, customer_id, start_date, end_date, support_contact, location, attendees, notes
            )
            return self.view.event_created(event.name)


    @require_auth

    @require_permission("edit_events")
    def update_event(self, event_id, **kwargs):
        """Updates an existing event"""
        event = self.dao.get_by_id(event_id)
        if not event:
            return self.view.event_not_found()

        user = self.user_dao.get_by_id(self.user_id)

        if event.support_contact != user.id and user.department_id not in (1, 4) :
            return self.view.access_for_modif_denied()

        valid_updates = {k: v for k, v in kwargs.items() if v is not None}

        if not valid_updates:
            return self.view.no_changes_provided()

        self.dao.update(event, **valid_updates)
        return self.view.event_updated(event.name)

    @require_auth

    @require_permission("delete_event")
    def delete_event(self, event_id):
        """Deletes an event"""
        event = self.dao.get_by_id(event_id)
        if not event:
            return self.view.event_not_found()

        self.dao.delete(event)
        return self.view.event_deleted(event.name)

