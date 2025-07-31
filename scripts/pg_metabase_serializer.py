#!/usr/bin/env python3
"""
pg_metabase_serializer.py

Exporte les objets BI Metabase directement depuis PostgreSQL
et les sauvegarde en fichiers YAML pour une sérialisation propre.
"""

import psycopg2
import yaml
import os
import pathlib

# 💾 Connexion PostgreSQL (remplace par les vraies valeurs Railway)
PG_CONFIG = {
    "host": os.getenv("PG_HOST", "containers-us-west-24.railway.app"),
    "port": os.getenv("PG_PORT", "5432"),
    "dbname": os.getenv("PG_DB", "railway"),
    "user": os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASSWORD", "your_password_here"),
    "sslmode": "require"
}

# 📁 Dossier de sortie
EXPORT_DIR = pathlib.Path("metabase_pg_export")
EXPORT_DIR.mkdir(exist_ok=True)

# 📌 Tables essentielles à exporter (tu peux en ajouter d'autres)
TABLES_TO_EXPORT = [
    "collection",
    "dashboard",
    "card",
    "metric",
    "segment",
    "native_query_snippet",
    "pulse"
]

def connect_pg():
    """Connexion PostgreSQL."""
    return psycopg2.connect(**PG_CONFIG)

def export_table_to_yaml(conn, table_name):
    """Export les données d'une table PostgreSQL vers un fichier YAML."""
    with conn.cursor() as cur:
        print(f"📤 Exporting table: {table_name}")
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]

        output_file = EXPORT_DIR / f"{table_name}.yaml"
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

        print(f"✅ Exported {table_name} -> {output_file}")

def main():
    try:
        conn = connect_pg()
        for table in TABLES_TO_EXPORT:
            export_table_to_yaml(conn, table)
        print(f"\n🎉 Export terminé avec succès dans : {EXPORT_DIR.resolve()}")
    except Exception as e:
        print(f"❌ Erreur lors de l'export : {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
