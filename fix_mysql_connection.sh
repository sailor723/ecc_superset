#!/bin/bash

echo "MySQL Connection Fix Script"
echo "==========================="
echo

# Check if Superset virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup_superset.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if MySQL container is running
if ! docker ps --format '{{.Names}}' | grep -q "^superset-mysql$"; then
    echo "MySQL container is not running. Starting it now..."
    docker start superset-mysql
    sleep 5
fi

# Get MySQL container IP
MYSQL_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' superset-mysql)
echo "MySQL container IP: $MYSQL_IP"

# Create Python script to update database connection
cat > update_mysql_connection.py << EOF
import os
from sqlalchemy import create_engine
import json

# Connect to Superset metadata database
conn_string = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://superset:superset@localhost:5432/superset')
engine = create_engine(conn_string)

# Get MySQL container IP
mysql_ip = "$MYSQL_IP"

# Update MySQL connection in Superset
with engine.connect() as connection:
    # Get existing MySQL database in Superset
    result = connection.execute("SELECT id, database_name, sqlalchemy_uri, extra FROM dbs WHERE database_name LIKE '%mysql%'")
    dbs = result.fetchall()
    
    if not dbs:
        print("No MySQL database found in Superset. Creating one...")
        
        # Create new MySQL database connection
        extra = json.dumps({
            "allows_virtual_table_explore": True,
            "allow_multi_schema_metadata_fetch": True,
            "allow_csv_upload": True,
            "schemas_allowed_for_csv_upload": ["superset"],
            "allow_ctas": True,
            "allow_cvas": True,
            "allow_dml": True,
            "allow_file_upload": True
        })
        
        sql = """
        INSERT INTO dbs (database_name, sqlalchemy_uri, expose_in_sqllab, allow_ctas, allow_cvas, allow_dml, allow_run_async, allow_file_upload, extra)
        VALUES ('MySQL Upload Database', 'mysql://superset:superset@{mysql_ip}:3306/superset', 
                true, true, true, true, true, true, '{extra}')
        """.format(mysql_ip=mysql_ip, extra=extra)
        
        connection.execute(sql)
        print("Created new MySQL connection to {mysql_ip}".format(mysql_ip=mysql_ip))
    else:
        # Update existing MySQL connections
        for db in dbs:
            db_id = db[0]
            db_name = db[1]
            
            # Parse current extra JSON
            try:
                extra = json.loads(db[3]) if db[3] else {}
            except:
                extra = {}
            
            # Update extra with required settings for file upload
            extra.update({
                "allows_virtual_table_explore": True,
                "allow_multi_schema_metadata_fetch": True,
                "allow_csv_upload": True,
                "schemas_allowed_for_csv_upload": ["superset"],
                "allow_ctas": True,
                "allow_cvas": True,
                "allow_dml": True,
                "allow_file_upload": True
            })
            
            # Update database URI to use container IP
            new_uri = f"mysql://superset:superset@{mysql_ip}:3306/superset"
            
            # Update database
            sql = """
            UPDATE dbs 
            SET 
                sqlalchemy_uri = '{uri}',
                allow_file_upload = TRUE, 
                allow_ctas = TRUE,
                allow_cvas = TRUE,
                allow_dml = TRUE,
                allow_run_async = TRUE,
                extra = '{extra}'
            WHERE id = {id}
            """.format(uri=new_uri, extra=json.dumps(extra), id=db_id)
            
            connection.execute(sql)
            print(f"Updated database '{db_name}' to use container IP: {mysql_ip}")

print("MySQL connection setup complete!")
EOF

# Export the required environment variables
export PYTHONPATH=$PYTHONPATH:$PWD
export FLASK_APP=superset
export FLASK_ENV=development
export SUPERSET_CONFIG_PATH=$PWD/superset_config.py
export SQLALCHEMY_DATABASE_URI='postgresql://superset:superset@localhost:5432/superset'

# Run the script
echo "Updating MySQL connection in Superset..."
python update_mysql_connection.py

# Clean up
rm update_mysql_connection.py

# Ensure MySQL has proper permissions
echo "Configuring MySQL permissions..."
docker exec -i superset-mysql mysql -uroot -psuperset << EOF
CREATE USER IF NOT EXISTS 'superset'@'%' IDENTIFIED BY 'superset';
GRANT ALL PRIVILEGES ON *.* TO 'superset'@'%' WITH GRANT OPTION;
ALTER USER 'superset'@'%' IDENTIFIED WITH mysql_native_password BY 'superset';
FLUSH PRIVILEGES;
EOF

echo "Creating test database if it doesn't exist..."
docker exec -i superset-mysql mysql -uroot -psuperset << EOF
CREATE DATABASE IF NOT EXISTS superset;
GRANT ALL PRIVILEGES ON superset.* TO 'superset'@'%';
FLUSH PRIVILEGES;
EOF

echo
echo "MySQL connection fix complete!"
echo "Please restart Superset using ./start_superset.sh"
echo "Then try uploading your CSV file again"
echo "If issues persist, make sure to select the correct database when uploading (MySQL Upload Database)"