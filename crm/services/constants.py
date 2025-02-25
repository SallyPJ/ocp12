# Department IDs and Names
DEPARTMENTS = {
    "MANAGEMENT": {"id": 1, "name": "Management"},
    "SALES": {"id": 2, "name": "Sales"},
    "SUPPORT": {"id": 3, "name": "Support"},
    "ADMIN": {"id": 4, "name": "Admin"},
}

# Permission IDs and Names
PERMISSIONS = {
    "READ_ALL_CLIENTS": {"id": 1, "name": "read_all_clients"},
    "READ_ALL_CONTRACTS": {"id": 2, "name": "read_all_contracts"},
    "READ_ALL_EVENTS": {"id": 3, "name": "read_all_events"},

    "MANAGE_EMPLOYEES": {"id": 4, "name": "manage_employees"},
    "CREATE_CONTRACTS": {"id": 5, "name": "create_contracts"},
    "EDIT_ALL_CONTRACTS": {"id": 6, "name": "edit_all_contracts"},
    "FILTER_EVENTS": {"id": 7, "name": "filter_events"},
    "EDIT_ALL_EVENTS": {"id": 8, "name": "edit_all_events"},

    "CREATE_CLIENTS": {"id": 9, "name": "create_clients"},
    "EDIT_OWN_CLIENTS": {"id": 10, "name": "edit_own_clients"},
    "EDIT_OWN_CONTRACTS": {"id": 11, "name": "edit_own_contracts"},
    "FILTER_CONTRACTS": {"id": 12, "name": "filter_unsigned_contracts"},
    "CREATE_EVENT_FOR_CLIENT": {"id": 13, "name": "create_event_for_client"},

    "FILTER_OWN_EVENTS": {"id": 14, "name": "filter_own_events"},
    "EDIT_OWN_EVENTS": {"id": 15, "name": "edit_own_events"},
}

# ✅ Department-Permission Mapping (Now in Constants)
DEPARTMENT_PERMISSIONS = {
    "MANAGEMENT": ["READ_ALL_CLIENTS", "READ_ALL_CONTRACTS", "READ_ALL_EVENTS","MANAGE_EMPLOYEES", "CREATE_CONTRACTS", "EDIT_ALL_CONTRACTS", "FILTER_EVENTS", "EDIT_ALL_EVENTS"],
    "SALES": ["READ_ALL_CLIENTS", "READ_ALL_CONTRACTS", "READ_ALL_EVENTS","CREATE_CLIENTS", "EDIT_OWN_CLIENTS", "EDIT_OWN_CONTRACTS", "FILTER_CONTRACTS", "CREATE_EVENT_FOR_CLIENT"],
    "SUPPORT": ["READ_ALL_CLIENTS", "READ_ALL_CONTRACTS", "READ_ALL_EVENTS","FILTER_OWN_EVENTS", "EDIT_OWN_EVENTS"],
    "ADMIN": list(PERMISSIONS.keys())
}

