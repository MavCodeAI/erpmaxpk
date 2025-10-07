#!/bin/bash
# ERPMAX Start Script - Railway Deployment

set -e

echo "🚀 Starting ERPMAX deployment..."

# Environment variables
export FRAPPE_SITE_NAME_HEADER=${FRAPPE_SITE_NAME_HEADER:-"erpmax"}
export APP_NAME=${APP_NAME:-"erpmax"}
export APP_TITLE=${APP_TITLE:-"ERPMAX"}
export FRAPPE_DB_HOST=${FRAPPE_DB_HOST:-"localhost"}
export FRAPPE_DB_NAME=${FRAPPE_DB_NAME:-"erpmax"}
export FRAPPE_DB_USER=${FRAPPE_DB_USER:-"root"}
export FRAPPE_DB_PASSWORD=${FRAPPE_DB_PASSWORD:-""}

# Wait for database
echo "⏳ Waiting for database connection..."
wait-for-it.sh $FRAPPE_DB_HOST:3306 --timeout=60 --strict -- echo "✅ Database is ready"

# Wait for Redis
echo "⏳ Waiting for Redis..."
wait-for-it.sh redis-cache:6379 --timeout=30 --strict -- echo "✅ Redis cache is ready"
wait-for-it.sh redis-queue:6379 --timeout=30 --strict -- echo "✅ Redis queue is ready"

# Change to frappe user and bench directory
cd /home/frappe/frappe-bench

# Initialize bench if not exists
if [ ! -f "/home/frappe/frappe-bench/sites/currentsite.txt" ]; then
    echo "🔧 Initializing ERPMAX site..."
    
    # Create new site
    bench new-site $FRAPPE_SITE_NAME_HEADER \
        --db-host $FRAPPE_DB_HOST \
        --db-name $FRAPPE_DB_NAME \
        --db-user $FRAPPE_DB_USER \
        --db-password $FRAPPE_DB_PASSWORD \
        --admin-password admin123 \
        --verbose
    
    # Set as current site
    bench use $FRAPPE_SITE_NAME_HEADER
    
    # Install ERPMAX app
    echo "📦 Installing ERPMAX app..."
    bench install-app erpmax
    
    # Enable developer mode
    bench set-config developer_mode 1
    
    # Set maintenance mode off
    bench set-maintenance-mode off
    
    echo "✅ ERPMAX site initialized successfully!"
else
    echo "📋 ERPMAX site already exists, updating..."
    
    # Migrate existing site
    bench --site $FRAPPE_SITE_NAME_HEADER migrate
fi

# Build assets
echo "🎨 Building assets..."
bench build --app erpmax

# Clear cache
echo "🧹 Clearing cache..."
bench --site $FRAPPE_SITE_NAME_HEADER clear-cache

# Start services based on environment
if [ "$RAILWAY_ENVIRONMENT" = "production" ]; then
    echo "🚀 Starting ERPMAX in production mode..."
    exec supervisord -c /etc/supervisor/conf.d/supervisord.conf
else
    echo "🔧 Starting ERPMAX in development mode..."
    bench start
fi
