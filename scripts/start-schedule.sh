#!/bin/bash
# ERPMAX Scheduler Start Script

set -e

cd /home/frappe/frappe-bench

# Wait for site to be ready
while [ ! -f "sites/currentsite.txt" ]; do
    echo "Waiting for site initialization..."
    sleep 5
done

echo "⏰ Starting ERPMAX scheduler..."

# Start Frappe scheduler
exec bench schedule
