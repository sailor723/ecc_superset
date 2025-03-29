import os
import psycopg2
import json
from psycopg2.extras import RealDictCursor

# Get PostgreSQL connection details from superset_config.py
pg_uri = "postgresql://superset:superset@localhost:5432/superset"

# Connect to PostgreSQL
conn = psycopg2.connect(pg_uri)
cursor = conn.cursor(cursor_factory=RealDictCursor)

# Get all databases
cursor.execute("SELECT id, database_name, extra FROM dbs")
databases = cursor.fetchall()

# Update each database
for db in databases:
    print(f"Updating database: {db['database_name']}")

    # Parse extra JSON
    try:
        extra = json.loads(db["extra"]) if db["extra"] else {}
    except json.JSONDecodeError:
        extra = {}

    # Update extra configuration
    extra.update(
        {
            "allows_virtual_table_explore": True,
            "allow_multi_schema_metadata_fetch": True,
            "allow_csv_upload": True,
        }
    )

    # Update database settings
    cursor.execute(
        """
        UPDATE dbs 
        SET 
            allow_file_upload = TRUE, 
            allow_ctas = TRUE,
            allow_cvas = TRUE,
            allow_dml = TRUE,
            extra = %s
        WHERE id = %s
        """,
        (json.dumps(extra), db["id"]),
    )

# Commit changes
conn.commit()
cursor.close()
conn.close()

print(f"Updated {len(databases)} databases to allow file uploads")
