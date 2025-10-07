# ERPMAX Dockerfile - Latest 2025 Best Practices
FROM frappe/erpnext:v15.43.1

# Set labels for better container management
LABEL maintainer="ERPMAX Team"
LABEL version="1.0.0"
LABEL description="ERPMAX - Enhanced ERPNext with custom branding"

# Set environment variables
ENV FRAPPE_SITE_NAME_HEADER=erpmax \
    APP_NAME=erpmax \
    APP_TITLE="ERPMAX" \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Switch to root for installations
USER root

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    supervisor \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Create custom directory structure
RUN mkdir -p /home/frappe/frappe-bench/apps/erpmax \
    && mkdir -p /home/frappe/frappe-bench/sites/erpmax \
    && mkdir -p /var/log/supervisor

# Copy custom app files
COPY --chown=frappe:frappe apps/erpmax /home/frappe/frappe-bench/apps/erpmax/
COPY --chown=frappe:frappe scripts/ /home/frappe/scripts/
COPY --chown=frappe:frappe config/ /home/frappe/config/

# Copy supervisor configuration
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/sites-available/default

# Make scripts executable
RUN chmod +x /home/frappe/scripts/*.sh

# Switch back to frappe user
USER frappe

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Initialize Git repo and install ERPMAX app
RUN cd /home/frappe/frappe-bench && \
    cd ./apps/erpmax && \
    git init && \
    git config --global user.email "erpmax@example.com" && \
    git config --global user.name "ERPMAX" && \
    git add . && \
    git commit -m "Initial commit" && \
    cd /home/frappe/frappe-bench && \
    bench get-app --skip-assets erpmax ./apps/erpmax && \
    bench build --app erpmax

# Expose ports
EXPOSE 80 8000 9000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/method/ping || exit 1

# Default command
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
