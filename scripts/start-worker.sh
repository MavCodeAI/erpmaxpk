#!/bin/bash
# ERPMAX Worker Start Script

set -e

WORKER_TYPE=${1:-"default"}

cd /home/frappe/frappe-bench

# Wait for site to be ready
while [ ! -f "sites/currentsite.txt" ]; do
    echo "Waiting for site initialization..."
    sleep 5
done

echo "⚡ Starting ERPMAX worker: $WORKER_TYPE"

# Start worker based on type
case $WORKER_TYPE in
    "default")
        exec bench worker --queue default
        ;;
    "long")
        exec bench worker --queue long
        ;;
    "short")
        exec bench worker --queue short
        ;;
    *)
        echo "Unknown worker type: $WORKER_TYPE"
        exit 1
        ;;
esac
