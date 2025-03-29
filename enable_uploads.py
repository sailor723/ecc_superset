from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

# Initialize Flask app with the configuration
app = Flask(__name__)
app.config.from_object("superset_config")

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Define Database model
class Database(db.Model):
    __tablename__ = "dbs"
    id = db.Column(db.Integer, primary_key=True)
    database_name = db.Column(db.String(250))
    sqlalchemy_uri = db.Column(db.String(1024))
    allow_file_upload = db.Column(db.Boolean, default=False)
    allow_ctas = db.Column(db.Boolean, default=False)
    allow_cvas = db.Column(db.Boolean, default=False)
    allow_dml = db.Column(db.Boolean, default=False)
    allow_csv_upload = db.Column(db.Boolean, default=False)
    expose_in_sqllab = db.Column(db.Boolean, default=False)
    extra = db.Column(db.Text)


with app.app_context():
    # Get all databases
    databases = Database.query.all()

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
        try:
            extra = json.loads(database.extra) if database.extra else {}
        except:
            extra = {}

        extra.update(
            {
                "allows_virtual_table_explore": True,
                "allow_multi_schema_metadata_fetch": True,
            }
        )
        database.extra = json.dumps(extra)

    # Commit changes
    db.session.commit()
    print(f"Updated {len(databases)} databases to allow file uploads")
