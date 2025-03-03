# Department IDs and Names
DEPARTMENTS = {
    "MANAGEMENT": {"id": 1, "name": "Management"},
    "SALES": {"id": 2, "name": "Sales"},
    "SUPPORT": {"id": 3, "name": "Support"},
    "ADMIN": {"id": 4, "name": "Admin"},
}

# Permission IDs and Names
PERMISSIONS = {
    "READ_ALL_EMPLOYEES": {"id": 1, "name": "read_all_employees"},
    "CREATE_EMPLOYEES": {"id": 2, "name": "create_employees"},
    "EDIT_EMPLOYEES": {"id": 3, "name":"edit_employees"},
    "DELETE_EMPLOYEES": {"id": 4, "name": "delete_employees"},


    "READ_ALL_CLIENTS": {"id": 5, "name": "read_all_clients"},
    "CREATE_CLIENTS": {"id": 6, "name": "create_clients"},
    "EDIT_CLIENTS": {"id": 7, "name": "edit_clients"},
    "DELETE_CLIENTS": {"id": 8, "name": "delete_clients"},

    "READ_ALL_CONTRACTS": {"id": 9, "name": "read_all_contracts"},
    "CREATE_CONTRACTS": {"id": 10, "name": "create_contracts"},
    "EDIT_CONTRACTS": {"id": 11, "name": "edit_contracts"},
    "DELETE_CONTRACTS": {"id": 12, "name": "delete_contracts"},

    "READ_ALL_EVENTS": {"id": 13, "name": "read_all_events"},
    "CREATE_EVENTS": {"id": 14, "name": "create_events"},
    "EDIT_EVENTS": {"id": 15, "name": "edit_events"},
    "DELETE_EVENTS": {"id": 16, "name": "delete_events"},


}

# ✅ Department-Permission Mapping (Now in Constants)
DEPARTMENT_PERMISSIONS = {
    "MANAGEMENT": ["READ_ALL_CLIENTS", "READ_ALL_CONTRACTS", "READ_ALL_EVENTS","READ_ALL_EMPLOYEES", "CREATE_EMPLOYEES", "EDIT_EMPLOYEES", "DELETE_EMPLOYEES", "CREATE_CONTRACTS", "EDIT_CONTRACTS", "EDIT_EVENTS"],
    "SALES": ["READ_ALL_CLIENTS", "READ_ALL_CONTRACTS", "READ_ALL_EVENTS","CREATE_CLIENTS", "EDIT_CLIENTS", "EDIT_CONTRACTS", "CREATE_EVENTS"],
    "SUPPORT": ["READ_ALL_CLIENTS", "READ_ALL_CONTRACTS", "READ_ALL_EVENTS", "EDIT_EVENTS"],
    "ADMIN": list(PERMISSIONS.keys())
}

