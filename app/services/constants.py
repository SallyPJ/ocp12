# Department IDs and Names
DEPARTMENTS = {
    "MANAGEMENT": {"id": 1, "name": "Management"},
    "SALES": {"id": 2, "name": "Sales"},
    "SUPPORT": {"id": 3, "name": "Support"},
}

# Permission IDs and Names
PERMISSIONS = {
    "VIEW_ASSIGNED_EVENTS": {"id": 1, "name": "view_assigned_events"},
    "EDIT_ASSIGNED_EVENTS": {"id": 2, "name": "edit_assigned_events"},
    "CREATE_CONTRACT": {"id": 3, "name": "create_contract"},
    "EDIT_OWN_CONTRACTS": {"id": 4, "name": "edit_own_contracts"},
    "DELETE_CONTRACT": {"id": 5, "name": "delete_contracts"},
}

# ✅ Department-Permission Mapping (Now in Constants)
DEPARTMENT_PERMISSIONS = {
    "SALES": ["CREATE_CONTRACT", "EDIT_OWN_CONTRACTS"],
    "SUPPORT": ["VIEW_ASSIGNED_EVENTS", "EDIT_ASSIGNED_EVENTS"]
}

