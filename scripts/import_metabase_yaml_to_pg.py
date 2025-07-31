#!/usr/bin/env python3
"""
import_metabase_yaml_to_pg.py

Recharge les objets YAML exportés dans les tables PostgreSQL Metabase.
Attention : ce script suppose que tu TRAVAILLES sur une copie vide/safe !
"""

import psycopg2
import yaml
import os
import pathlib

# 💾 Connexion PostgreSQL (même format que pour l’export)
PG_CONFIG = {
    "host": os.getenv("PG_HOST", "localhost"),
    "port": os.getenv("PG_PORT", "5432"),
    "dbname": os.getenv("PG_DB", "railway"),
    "user": os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASSWORD", "your_password_here"),
    "sslmode": "require"
}

IMPORT_DIR = pathlib.Path("metabase_pg_export")  # Dossier contenant les .yaml
TABLES_ORDER = [
    "collection",
    "metric",
    "segment",
    "native_query_snippet",
    "card",
    "dashboard",
    "pulse"
]

def connect_pg():
    return psycopg2.connect(**PG_CONFIG)

def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def insert_row(cur, table, row):
    columns = list(row.keys())
    values = [row[col] for col in columns]
    placeholders = ','.join(['%s'] * len(columns))
    sql = f"""INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"""
    cur.execute(sql, values)

def import_table(conn, table_name):
    file_path = IMPORT_DIR / f"{table_name}.yaml"
    if not file_path.exists():
        print(f"⚠️ File not found: {file_path}")
        return

    print(f"📥 Importing {table_name} from {file_path}")
    data = load_yaml(file_path)
    with conn.cursor() as cur:
        for row in data:
            try:
                insert_row(cur, table_name, row)
            except psycopg2.errors.UniqueViolation:
                print(f"⚠️ Skipping duplicate in {table_name} for ID={row.get('id')}")
                conn.rollback()
            except Exception as e:
                print(f"❌ Error inserting row in {table_name}: {e}")
                conn.rollback()
            else:
                conn.commit()

def main():
    try:
        conn = connect_pg()
        for table in TABLES_ORDER:
            import_table(conn, table)
        print("\n✅ Import terminé avec succès.")
    except Exception as e:
        print(f"❌ Erreur globale : {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
