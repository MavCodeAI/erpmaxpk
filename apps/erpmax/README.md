# ERPMAX - Enhanced ERPNext Application

![ERPMAX Logo](public/images/erpmax-logo.svg)

ERPMAX is an enhanced ERP solution built on top of ERPNext with modern UI/UX, advanced features, and improved performance.

## Features

✨ **Modern Interface**
- Clean, responsive design
- Enhanced user experience
- Mobile-first approach
- Dark mode support

🚀 **Performance Optimized**
- Faster loading times
- Optimized database queries
- Enhanced caching
- Improved search functionality

🔒 **Security Enhanced**
- Advanced authentication
- Role-based permissions
- Audit trails
- Data encryption

📈 **Advanced Analytics**
- Real-time dashboards
- Custom reports
- Data visualization
- Business intelligence

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- MariaDB 10.3+
- Redis 5+

### Quick Install

```bash
# Install ERPMAX app
bench get-app erpmax https://github.com/yourusername/erpmax.git
bench install-app erpmax

# Create new site with ERPMAX
bench new-site erpmax.local
bench --site erpmax.local install-app erpmax
```

### Docker Installation

```bash
# Clone repository
git clone https://github.com/yourusername/erpmax.git
cd erpmax

# Start with Docker Compose
docker-compose up -d
```

## Configuration

### Site Configuration

```json
{
  "app_name": "erpmax",
  "app_title": "ERPMAX",
  "developer_mode": 1,
  "maintenance_mode": 0
}
```

### Environment Variables

```bash
FRAPPE_SITE_NAME_HEADER=erpmax
APP_NAME=erpmax
APP_TITLE=ERPMAX
```

## Development

### Setup Development Environment

```bash
# Create development branch
git checkout -b develop

# Install in development mode
bench get-app erpmax /path/to/erpmax --branch develop
bench install-app erpmax

# Enable developer mode
bench set-config developer_mode 1
```

### Build Assets

```bash
# Build CSS and JS
bench build --app erpmax

# Watch for changes (development)
bench watch
```

### Running Tests

```bash
# Run unit tests
bench run-tests --app erpmax

# Run specific test
bench run-tests --app erpmax --test test_customer
```

## Customization

### Adding Custom Fields

```python
# In hooks.py
custom_fields = {
    "Customer": [
        {
            "fieldname": "custom_field",
            "label": "Custom Field",
            "fieldtype": "Data"
        }
    ]
}
```

### Custom CSS/JS

```python
# In hooks.py
app_include_css = [
    "/assets/erpmax/css/custom.css"
]

app_include_js = [
    "/assets/erpmax/js/custom.js"
]
```

## API Usage

### REST API

```javascript
// Get customer data
fetch('/api/resource/Customer/CUST-00001')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Python API

```python
import frappe

# Get document
customer = frappe.get_doc('Customer', 'CUST-00001')

# Create document
new_customer = frappe.get_doc({
    'doctype': 'Customer',
    'customer_name': 'New Customer'
})
new_customer.insert()
```

## Deployment

### Railway Deployment

1. Fork this repository
2. Connect to Railway
3. Set environment variables
4. Deploy!

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/deploy)

### Production Settings

```bash
# Disable developer mode
bench set-config developer_mode 0

# Enable maintenance mode during updates
bench set-maintenance-mode on

# Update and migrate
bench update
bench migrate

# Disable maintenance mode
bench set-maintenance-mode off
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Documentation

- [User Guide](docs/user-guide.md)
- [Developer Guide](docs/developer-guide.md)
- [API Reference](docs/api-reference.md)
- [Deployment Guide](docs/deployment.md)

## Support

- 📧 Email: support@erpmax.com
- 💬 Discord: [ERPMAX Community](https://discord.gg/erpmax)
- 📚 Documentation: [docs.erpmax.com](https://docs.erpmax.com)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/erpmax/issues)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on [ERPNext](https://erpnext.com/)
- Powered by [Frappe Framework](https://frappe.io/)
- UI inspired by modern design principles
- Community contributions and feedback

---

**ERPMAX** - Enhanced Business Solutions 🚀