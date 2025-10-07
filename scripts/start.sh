#!/bin/bash
# ERPMAX Start Script - Railway Deployment (Fixed Version)
# This script handles site creation, app installation, and asset building at runtime

set -e

echo "🚀 Starting ERPMAX deployment (Fixed Version)..."

# Environment variables with Railway defaults
export FRAPPE_SITE_NAME_HEADER=${FRAPPE_SITE_NAME_HEADER:-"erpmax"}
export APP_NAME=${APP_NAME:-"erpmax"}
export APP_TITLE=${APP_TITLE:-"ERPMAX"}
export FRAPPE_DB_HOST=${FRAPPE_DB_HOST:-"localhost"}
export FRAPPE_DB_NAME=${FRAPPE_DB_NAME:-"erpmax"}
export FRAPPE_DB_USER=${FRAPPE_DB_USER:-"root"}
export FRAPPE_DB_PASSWORD=${FRAPPE_DB_PASSWORD:-""}
export ADMIN_PASSWORD=${ADMIN_PASSWORD:-"admin123"}

# Wait for database with better error handling
echo "⏳ Waiting for database connection..."
timeout 120s /home/frappe/scripts/wait-for-it.sh $FRAPPE_DB_HOST:3306 --timeout=60 --strict -- echo "✅ Database is ready" || {
    echo "❌ Database connection failed after 120 seconds"
    exit 1
}

# Wait for Redis services
echo "⏳ Waiting for Redis services..."
timeout 60s /home/frappe/scripts/wait-for-it.sh redis-cache:6379 --timeout=30 --strict -- echo "✅ Redis cache is ready" || {
    echo "❌ Redis cache connection failed"
    exit 1
}

timeout 60s /home/frappe/scripts/wait-for-it.sh redis-queue:6379 --timeout=30 --strict -- echo "✅ Redis queue is ready" || {
    echo "❌ Redis queue connection failed"
    exit 1
}

# Change to frappe user and bench directory
cd /home/frappe/frappe-bench

# Function to check if site exists
site_exists() {
    bench --site $FRAPPE_SITE_NAME_HEADER status >/dev/null 2>&1
}

# Initialize bench if not exists
if ! site_exists; then
    echo "🔧 Initializing ERPMAX site..."
    
    # Create new site with better error handling
    bench new-site $FRAPPE_SITE_NAME_HEADER \
        --db-host $FRAPPE_DB_HOST \
        --db-name $FRAPPE_DB_NAME \
        --db-user $FRAPPE_DB_USER \
        --db-password $FRAPPE_DB_PASSWORD \
        --admin-password $ADMIN_PASSWORD \
        --verbose || {
            echo "❌ Failed to create site"
            exit 1
        }
    
    # Set as current site
    bench use $FRAPPE_SITE_NAME_HEADER
    
    # Install ERPMAX app (this avoids the Git repository error)
    echo "📦 Installing ERPMAX app..."
    bench --site $FRAPPE_SITE_NAME_HEADER install-app erpmax || {
        echo "❌ Failed to install ERPMAX app"
        exit 1
    }
    
    # Enable developer mode for easier debugging
    bench --site $FRAPPE_SITE_NAME_HEADER set-config developer_mode 1
    
    # Set maintenance mode off
    bench --site $FRAPPE_SITE_NAME_HEADER set-maintenance-mode off
    
    echo "✅ ERPMAX site initialized successfully!"
else
    echo "📋 ERPMAX site already exists, checking for updates..."
    
    # Migrate existing site
    bench --site $FRAPPE_SITE_NAME_HEADER migrate || {
        echo "❌ Migration failed"
        exit 1
    }
    
    # Check if app is installed, if not install it
    if ! bench --site $FRAPPE_SITE_NAME_HEADER list-apps | grep -q "erpmax"; then
        echo "📦 Installing missing ERPMAX app..."
        bench --site $FRAPPE_SITE_NAME_HEADER install-app erpmax || {
            echo "❌ Failed to install missing ERPMAX app"
            exit 1
        }
    fi
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
