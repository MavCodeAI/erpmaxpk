# ERPMAX Production Dockerfile - 2025 Best Practices
FROM frappe/erpnext:v15.43.1

# Metadata
LABEL maintainer="ERPMAX Team <info@erpmax.com>"
LABEL version="1.0.0"
LABEL description="ERPMAX - Enhanced ERPNext with modern features"
LABEL org.opencontainers.image.title="ERPMAX"
LABEL org.opencontainers.image.description="Enhanced ERP solution built on ERPNext"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="ERPMAX Team"
LABEL org.opencontainers.image.licenses="GPL-3.0"

# Environment variables
ENV FRAPPE_SITE_NAME_HEADER=erpmax \
    APP_NAME=erpmax \
    APP_TITLE="ERPMAX" \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    NODE_ENV=production

# Switch to root for system packages
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    supervisor \
    nginx \
    redis-tools \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create directory structure
RUN mkdir -p /home/frappe/frappe-bench/apps/erpmax \
    && mkdir -p /home/frappe/frappe-bench/sites/erpmax \
    && mkdir -p /var/log/supervisor \
    && mkdir -p /home/frappe/scripts \
    && mkdir -p /home/frappe/config

# Copy application files
COPY --chown=frappe:frappe apps/erpmax /home/frappe/frappe-bench/apps/erpmax/
COPY --chown=frappe:frappe scripts/ /home/frappe/scripts/
COPY --chown=frappe:frappe config/ /home/frappe/config/

# Copy configuration files
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/nginx.conf /etc/nginx/sites-available/default

# Copy requirements and install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Make scripts executable
RUN chmod +x /home/frappe/scripts/*.sh

# Fix permissions
RUN chown -R frappe:frappe /home/frappe/

# Switch to frappe user
USER frappe

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Install ERPMAX app
RUN bench get-app --skip-assets erpmax ./apps/erpmax \
    && bench build --app erpmax

# Switch back to root for final setup
USER root

# Configure nginx
RUN nginx -t

# Create health check script
RUN echo '#!/bin/bash\ncurl -f http://localhost:8000/api/method/ping || exit 1' > /healthcheck.sh \
    && chmod +x /healthcheck.sh

# Expose ports
EXPOSE 80 8000 9000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=120s --retries=3 \
    CMD /healthcheck.sh

# Set entrypoint
ENTRYPOINT ["/home/frappe/scripts/start.sh"]

# Default command
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
