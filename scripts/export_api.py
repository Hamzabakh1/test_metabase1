#!/usr/bin/env python3
"""
export_api.py

Export Metabase objects (collections, dashboards, cards) via API
and save them as YAML files in the metabase_yaml_api/ directory.
"""

import os
import requests
import yaml
import pathlib
import sys

# Configuration via variables d'environnement
MB_HOST = os.getenv("MB_HOST")
MB_USER = os.getenv("MB_USER")
MB_PASS = os.getenv("MB_PASS")

if not all([MB_HOST, MB_USER, MB_PASS]):
    print("Error: Please set MB_HOST, MB_USER and MB_PASS environment variables.", file=sys.stderr)
    sys.exit(1)

API_BASE = f"{MB_HOST.rstrip('/')}/api"

# Authentification et récupération du token de session
resp = requests.post(
    f"{API_BASE}/session",
    json={"username": MB_USER, "password": MB_PASS},
    timeout=30
)
resp.raise_for_status()
session_id = resp.json().get("id")
HEADERS = {"X-Metabase-Session": session_id}

def fetch(endpoint: str):
    """Fetch JSON data from a Metabase API endpoint."""
    r = requests.get(f"{API_BASE}/{endpoint}", headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

# Dossier de sortie
EXPORT_DIR = pathlib.Path("metabase_yaml_api")
EXPORT_DIR.mkdir(exist_ok=True)

# Liste des objets à exporter : (nom_fichier, endpoint_API)
OBJECTS = [
    ("collections", "collection"),
    ("dashboards",  "dashboard"),
    ("cards",       "card"),
]

# Exécution de l'export
for name, endpoint in OBJECTS:
    print(f"Exporting {name}...")
    data = fetch(endpoint)
    out_file = EXPORT_DIR / f"{name}.yaml"
    with open(out_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    print(f" -> {out_file}")

print("✅ Export terminé dans", EXPORT_DIR.resolve())
