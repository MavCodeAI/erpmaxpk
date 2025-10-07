# 🚀 ERPMAX Complete Deployment Guide

Welcome to ERPMAX! This guide will help you deploy your complete ERPNext clone with custom branding in minutes.

## 🎯 What You Get

✅ **Complete ERPNext Clone** - Full functionality with ERPMAX branding  
✅ **Modern UI/UX** - 2025 design standards with responsive interface  
✅ **Railway Ready** - Optimized for Railway deployment  
✅ **Docker Containerized** - Production-ready containers  
✅ **Auto Deployment** - GitHub Actions CI/CD pipeline  
✅ **Best Practices** - Security, performance, and scalability  

## 🚀 Quick Deploy (1-Click)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/deploy)

### Steps:
1. **Click Deploy Button** ⬆️
2. **Connect GitHub** - Fork this repo automatically
3. **Set Environment Variables** (see below)
4. **Deploy & Enjoy!** 🎉

## 🔧 Environment Variables

Copy these to Railway dashboard:

```bash
# 🎯 Core Settings
FRAPPE_SITE_NAME_HEADER=erpmax
APP_NAME=erpmax
APP_TITLE=ERPMAX
RAILWAY_ENVIRONMENT=production

# 🔐 Security (CHANGE THESE!)
MYSQL_ROOT_PASSWORD=your-super-secure-password-123
ENCRYPTION_KEY=your-32-character-encryption-key-here
SECRET_KEY=your-secret-key-for-sessions

# 📧 Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@domain.com
MAIL_PASSWORD=your-app-password

# 💾 Database
FRAPPE_DB_HOST=${DATABASE_PRIVATE_URL}
FRAPPE_DB_NAME=erpmax
FRAPPE_DB_USER=root
FRAPPE_DB_PASSWORD=${MYSQL_ROOT_PASSWORD}

# 📦 Redis
REDIS_CACHE_URL=redis://redis-cache:6379
REDIS_QUEUE_URL=redis://redis-queue:6379
```

## 📋 Manual Deployment Steps

### 1. 📁 Clone Repository
```bash
git clone https://github.com/yourusername/erpmax.git
cd erpmax
```

### 2. 🔧 Configure Environment
```bash
# Copy environment file
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. 🐳 Docker Deployment
```bash
# Build and start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f erpmax
```

### 4. 🌐 Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

## 🎨 Customization Options

### 🏷️ Change Branding
All branding is already changed to ERPMAX, but you can modify:

```python
# apps/erpmax/hooks.py
app_name = "your_name"
app_title = "Your Title"
app_publisher = "Your Company"
```

### 🎨 Custom Logo
Replace logo files:
```bash
apps/erpmax/public/images/
├── erpmax-logo.svg     # Main logo
├── favicon.ico         # Browser icon
└── screenshots/        # App screenshots
```

### 🎨 Custom Colors
Modify CSS variables:
```css
/* apps/erpmax/public/css/erpmax.css */
:root {
  --erpmax-primary: #your-color;
  --erpmax-secondary: #your-secondary;
}
```

## 🔒 Security Setup

### 🔑 Generate Secure Keys
```bash
# Generate encryption key (32 characters)
openssl rand -hex 16

# Generate secret key
openssl rand -base64 32
```

### 🛡️ Security Headers
Already configured in nginx.conf:
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Content-Security-Policy

### 🔐 Database Security
```bash
# Change default passwords
MYSQL_ROOT_PASSWORD=Complex-Password-123!
DB_PASSWORD=Another-Secure-Password-456!
```

## 📊 Performance Optimization

### 🚀 Production Settings
```json
{
  "background_workers": 2,
  "gunicorn_workers": 4,
  "auto_update": false,
  "developer_mode": 0,
  "logging": 1
}
```

### 📦 Caching
- Redis for session storage
- Database query caching
- Static file caching with nginx

### 📈 Monitoring
Built-in health checks:
- `/health` - Application health
- `/api/method/ping` - API health

## 🔄 Updates & Maintenance

### 🔄 Auto Updates
Configured via GitHub Actions:
- Push to main branch triggers deployment
- Automatic testing before deployment
- Zero-downtime deployments

### 🔧 Manual Updates
```bash
# Update code
git pull origin main

# Rebuild and deploy
railway up

# Or with Docker
docker-compose up -d --build
```

### 💾 Database Migration
```bash
# Access container
railway shell

# Run migrations
cd /home/frappe/frappe-bench
bench migrate
```

## 📈 Scaling

### 🔄 Horizontal Scaling
Railway auto-scaling available:
- CPU-based scaling
- Memory-based scaling
- Custom metrics scaling

### 💪 Vertical Scaling
Upgrade Railway plan for:
- More CPU cores
- More RAM
- More storage
- Higher bandwidth

## 🆘 Troubleshooting

### 🐛 Common Issues

#### Database Connection Error
```bash
# Check database status
railway status

# Check environment variables
railway variables

# Restart database
railway restart --service database
```

#### Site Not Loading
```bash
# Check logs
railway logs --service erpmax

# Check health endpoint
curl https://your-domain.railway.app/health
```

#### Memory Issues
```bash
# Check memory usage
railway metrics

# Reduce workers if needed
railway variables set WORKERS=1
```

### 🔍 Debug Mode
```bash
# Enable debug mode
railway shell
bench set-config developer_mode 1
bench restart
```

## 📞 Support

🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/erpmax/issues)  
📚 **Documentation**: [ERPMAX Docs](https://docs.erpmax.com)  
💬 **Community**: [Discord Server](https://discord.gg/erpmax)  
📧 **Email**: support@erpmax.com  

## ✅ Production Checklist

Before going live:

- [ ] 🔐 Changed all default passwords
- [ ] 🔑 Set encryption keys
- [ ] 📧 Configured email settings
- [ ] 🌐 Set up custom domain
- [ ] 📜 Configured SSL certificate
- [ ] 💾 Enabled backups
- [ ] 📊 Set up monitoring
- [ ] 🧪 Tested all functionality
- [ ] 📱 Tested mobile responsiveness
- [ ] 👥 Created admin user
- [ ] 🏢 Set up company information

## 🎉 Success!

Your ERPMAX deployment is now ready! 

🌟 **Default Login**:
- URL: `https://your-domain.railway.app`
- Username: `Administrator`
- Password: `admin123` (change immediately!)

---

**Built with ❤️ using latest 2025 best practices**

*Happy ERPing! 🚀*
