#!/bin/bash

echo "Superset Cleanup Script"
echo "======================="
echo

# Kill all Superset processes
echo "Stopping any running Superset processes..."
pkill -f "python fix_superset.py"
pkill -f "superset"

# Check if port 8088 is still in use
if lsof -Pi :8088 -sTCP:LISTEN -t >/dev/null ; then
    echo "Force killing processes on port 8088..."
    lsof -ti:8088 | xargs kill -9
fi

# Clean temporary files
echo "Cleaning temporary files..."
rm -rf /tmp/superset_uploads/* 2>/dev/null
mkdir -p /tmp/superset_uploads/
chmod 777 /tmp/superset_uploads/

# Clean up Flask session files
echo "Cleaning Flask session files..."
find /tmp -name "flask_session_*" -delete 2>/dev/null

echo "Cleanup complete! You can now run ./start_superset.sh to restart Superset." 