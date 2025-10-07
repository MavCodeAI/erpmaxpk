# 🚀 ERPMAX Railway Deployment Guide

Complete guide to deploy ERPMAX on Railway with one-click deployment.

## ⚡ Quick Deploy (Recommended)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/deploy)

### Steps:
1. Click the deploy button above
2. Connect your GitHub account
3. Fork this repository
4. Set environment variables (see below)
5. Deploy!

## 🔧 Environment Variables

Set these in Railway dashboard:

```bash
# Required
FRAPPE_SITE_NAME_HEADER=erpmax
APP_NAME=erpmax
APP_TITLE=ERPMAX
MYSQL_ROOT_PASSWORD=your-secure-password
ENCRYPTION_KEY=your-encryption-key

# Optional
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## 📋 Manual Deployment Steps

### 1. Fork Repository
- Fork this repository to your GitHub
- Clone locally if needed

### 2. Railway Setup
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Link to your repo
railway link
```

### 3. Add Services
```bash
# Add MariaDB
railway add mariadb

# Add Redis
railway add redis

# Deploy main app
railway up
```

### 4. Configure Domain
- Go to Railway dashboard
- Click on your service
- Go to Settings → Domains
- Add custom domain or use Railway subdomain

## 🔐 Security Configuration

### SSL Certificate
- Railway automatically provides SSL
- Custom domains get Let's Encrypt certificates

### Database Security
```bash
# Set strong passwords
MYSQL_ROOT_PASSWORD=complex-password-123
ENCRYPTION_KEY=32-character-random-string
```

### Firewall Rules
- Railway handles firewall automatically
- Only exposed ports are accessible

## 📊 Monitoring & Logs

### View Logs
```bash
# View deployment logs
railway logs

# View specific service logs
railway logs --service erpmax
```

### Monitoring
- CPU and Memory usage in Railway dashboard
- Custom metrics available via API
- Health checks configured automatically

## 🔄 Updates & Maintenance

### Auto-deployment
- Configured via GitHub webhooks
- Pushes to main branch trigger deployment
- Zero-downtime deployments

### Manual Updates
```bash
# Update code
git pull origin main

# Redeploy
railway up
```

### Database Migrations
```bash
# Access container
railway shell

# Run migrations
cd /home/frappe/frappe-bench
bench migrate
```

## 💾 Backup & Recovery

### Automated Backups
- Railway volumes are backed up automatically
- Point-in-time recovery available

### Manual Backup
```bash
# Database backup
railway connect mariadb
mysqldump -u root -p erpmax > backup.sql

# Site backup
railway shell
bench backup --with-files
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```bash
# Check database status
railway status

# Restart database
railway restart --service mariadb
```

#### 2. Site Not Loading
```bash
# Check logs
railway logs --service erpmax

# Restart application
railway restart --service erpmax
```

#### 3. Memory Issues
```bash
# Upgrade plan in Railway dashboard
# Or optimize memory usage
bench set-config background_workers 1
```

### Debug Mode
```bash
# Enable debug mode
railway shell
cd /home/frappe/frappe-bench
bench set-config developer_mode 1
```

## 📈 Performance Optimization

### Scaling
- Upgrade Railway plan for more resources
- Configure auto-scaling in dashboard

### Caching
- Redis cache enabled by default
- CDN available for static assets

### Database Optimization
```sql
-- Run in database
OPTIMIZE TABLE `tabCustomer`;
OPTIMIZE TABLE `tabSales Invoice`;
```

## 🛡️ Production Checklist

- [ ] Set strong passwords
- [ ] Configure SSL/TLS
- [ ] Enable backups
- [ ] Set up monitoring
- [ ] Configure email
- [ ] Test all functionality
- [ ] Set up custom domain
- [ ] Configure DNS
- [ ] Enable auto-scaling
- [ ] Document admin credentials

## 📞 Support

If you face any issues:
1. Check Railway logs
2. Review environment variables
3. Test database connectivity
4. Open issue on GitHub
5. Contact Railway support

---

**Happy Deploying! 🎉**
