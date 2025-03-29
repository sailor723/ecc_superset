#!/usr/bin/env python
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Connect to the PostgreSQL metadata database
print("Connecting to Superset metadata database...")
engine = create_engine("postgresql://superset:superset@localhost:5432/superset")
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Check for MySQL connection
    result = session.execute(
        text("SELECT id, database_name, extra FROM dbs WHERE database_name = 'MySQL'")
    )
    rows = result.fetchall()

    if rows:
        db_id = rows[0][0]
        print(f"Found MySQL connection with ID: {db_id}")

        # Parse the existing extras
        try:
            old_extras = json.loads(rows[0][2]) if rows[0][2] else {}
            print(f"Current extras: {json.dumps(old_extras, indent=2)}")

            # Create new extras without the problematic parameters
            new_extras = {
                "allows_virtual_table_explore": True,
                "schemas_allowed_for_csv_upload": ["superset", "test_schema"],
                "allow_csv_upload": True,
                "engine_params": {"connect_args": {"charset": "utf8mb4"}},
            }

            # Update the database connection
            session.execute(
                text("""
                UPDATE dbs SET
                    extra = :extras
                WHERE id = :id
                """),
                {"extras": json.dumps(new_extras), "id": db_id},
            )
            session.commit()

            print(
                f"Updated MySQL connection extras. Removed problematic pooling parameters."
            )
            print(f"New extras: {json.dumps(new_extras, indent=2)}")

        except json.JSONDecodeError:
            print("Error: Could not parse existing extras JSON")
    else:
        print("No MySQL connection found in the database.")
finally:
    session.close()

print("\nMySQL connection fix complete!")
print("Please restart Superset and try connecting to MySQL again.")
