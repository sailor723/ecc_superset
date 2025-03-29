from superset import app, db
from superset.models.core import Database

with app.app_context():
    # Get all databases
    databases = db.session.query(Database).all()

    # Enable file upload for all databases
    for database in databases:
        print(f"Updating database: {database.database_name}")
        database.allow_file_upload = True
        database.allow_csv_upload = True
        database.allow_ctas = True
        database.allow_cvas = True
        database.allow_dml = True
        database.expose_in_sqllab = True

        # Update extra configuration
        extra = database.get_extra() or {}
        if isinstance(extra, str):
            import json

            try:
                extra = json.loads(extra)
            except json.JSONDecodeError:
                extra = {}

        extra.update(
            {
                "allows_virtual_table_explore": True,
                "allow_multi_schema_metadata_fetch": True,
            }
        )
        database.extra = extra

    # Commit changes
    db.session.commit()
    print(f"Updated {len(databases)} databases to allow file uploads")
