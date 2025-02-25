import sys
import os

CRM_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(CRM_DIR, ".."))

if CRM_DIR not in sys.path:
    sys.path.insert(0, CRM_DIR)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
