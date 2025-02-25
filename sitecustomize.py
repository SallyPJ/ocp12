import sys
import os

# Détermine le répertoire du projet
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Ajoute automatiquement crm au sys.path
CRM_DIR = os.path.join(BASE_DIR, "crm")
if CRM_DIR not in sys.path:
    sys.path.insert(0, CRM_DIR)