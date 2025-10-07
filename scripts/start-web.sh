#!/bin/bash
# ERPMAX Web Server Start Script

set -e

cd /home/frappe/frappe-bench

# Wait for site to be ready
while [ ! -f "sites/currentsite.txt" ]; do
    echo "Waiting for site initialization..."
    sleep 5
done

echo "🌐 Starting ERPMAX web server..."

# Start Frappe web server
exec bench serve \
    --host 0.0.0.0 \
    --port 8000 \
    --noreload \
    --nothreading
