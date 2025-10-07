# ERPMAX Hooks Configuration
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _

# Application metadata
app_name = "erpmax"
app_title = "ERPMAX"
app_publisher = "ERPMAX Team"
app_description = "Enhanced ERP solution built on ERPNext with advanced features and modern UI"
app_email = "info@erpmax.com"
app_license = "GNU General Public License (v3)"
app_logo_url = "/assets/erpmax/images/erpmax-logo.svg"
app_version = "1.0.0"
required_apps = ["frappe", "erpnext"]

# Users (add all users for role and workflow permissions)
users = [
    {
        "name": "administrator",
        "password": "admin"
    }
]

# Website settings
website_generators = ["Item", "BOM", "Customer", "Supplier"]

# Application logo
app_include_css = [
    "/assets/erpmax/css/erpmax.css",
    "/assets/erpmax/css/custom-theme.css"
]

app_include_js = [
    "/assets/erpmax/js/erpmax.js",
    "/assets/erpmax/js/custom-scripts.js"
]

# Boot session
boot_session = "erpmax.boot.boot_session"

# Homepage
home_page = "login"

# Website context
website_context = {
    "favicon": "/assets/erpmax/images/favicon.ico",
    "splash_image": "/assets/erpmax/images/erpmax-logo.svg"
}

# Brand colors and theme
brand_html = '''
<div class="erpmax-brand">
    <img src="/assets/erpmax/images/erpmax-logo.svg" alt="ERPMAX" height="24">
</div>
'''

# Navigation
top_bar_items = [
    {
        "label": _("Home"),
        "url": "/",
        "right": 1
    }
]

# Custom fields to be created
custom_fields = {
    "Company": [
        {
            "fieldname": "erpmax_enhanced_features",
            "label": "Enhanced Features",
            "fieldtype": "Check",
            "default": 1
        }
    ]
}

# Property setters for customization
property_setters = [
    {
        "doctype": "System Settings",
        "property": "app_name",
        "value": "ERPMAX"
    }
]

# Fixtures - data that should be imported to new sites
fixtures = [
    "Custom Field",
    "Property Setter",
    "Custom Script",
    "Print Format",
    "Letter Head",
    "Email Template"
]

# DocTypes to be ignored while clearing transactions of a Company
company_transaction_deletion_doctypes = []

# Request Events
doc_events = {
    "*": {
        "on_update": "erpmax.api.clear_cache",
        "after_insert": "erpmax.api.log_creation"
    }
}

# Scheduled Tasks
scheduler_events = {
    "all": [
        "erpmax.tasks.all"
    ],
    "daily": [
        "erpmax.tasks.daily"
    ],
    "hourly": [
        "erpmax.tasks.hourly"
    ],
    "weekly": [
        "erpmax.tasks.weekly"
    ],
    "monthly": [
        "erpmax.tasks.monthly"
    ]
}

# Testing
test_template = "erpmax.tests.test_template"
test_dependencies = ["Item"]

# Override methods
override_whitelisted_methods = {
    "frappe.desk.doctype.event.event.get_events": "erpmax.api.get_events"
}

# Authentication hooks
authentication_hooks = [
    "erpmax.auth.validate_auth"
]

# Website route rules
website_route_rules = [
    {"from_route": "/erpmax/<path:app_path>", "to_route": "erpmax"},
]

# Generators
website_generators = ["Item", "BOM", "Customer", "Supplier"]

# Installation
after_install = "erpmax.install.after_install"
before_uninstall = "erpmax.uninstall.before_uninstall"

# Desk Notifications
notification_config = "erpmax.notifications.get_notification_config"

# Permissions
permission_query_conditions = {
    "Event": "erpmax.queries.get_permission_query_conditions_for_event",
}

has_permission = {
    "Event": "erpmax.queries.has_permission",
}

# DocType Class
doctype_class = {
    "ToDo": "erpmax.overrides.todo.ToDo"
}

# Document naming
document_naming_series = {
    "Lead": "ERPMAX-LEAD-.YYYY.-",
    "Customer": "ERPMAX-CUST-.YYYY.-",
    "Supplier": "ERPMAX-SUPP-.YYYY.-"
}

# Jinja Environment
jenv = {
    "methods": [
        "erpmax.api.get_company_info",
        "erpmax.api.get_user_info"
    ]
}

# Standard portal menu items
standard_portal_menu_items = [
    {
        "title": _("Personal Details"),
        "route": "/update-profile",
        "reference_doctype": "User",
        "role": "System Manager"
    }
]

# User data protection
user_data_fields = [
    {
        "doctype": "User",
        "filter_by": "name",
        "redact_fields": ["first_name", "last_name", "email", "phone"],
        "rename": True
    }
]

# Global search doctypes
global_search_doctypes = {
    "Default": [
        {"doctype": "Customer", "index": 0},
        {"doctype": "Supplier", "index": 1},
        {"doctype": "Item", "index": 2},
        {"doctype": "Sales Order", "index": 3},
        {"doctype": "Purchase Order", "index": 4},
        {"doctype": "Sales Invoice", "index": 5},
        {"doctype": "Purchase Invoice", "index": 6}
    ]
}
