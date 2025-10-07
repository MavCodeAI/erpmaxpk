# ERPMAX Installation Scripts
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def after_install():
    """Run after ERPMAX installation"""
    
    frappe.logger().info("Starting ERPMAX installation...")
    
    # Create custom fields
    create_erpmax_custom_fields()
    
    # Set property setters
    create_erpmax_property_setters()
    
    # Create default data
    create_default_data()
    
    # Set app settings
    set_app_settings()
    
    # Create default user roles
    create_default_roles()
    
    frappe.logger().info("ERPMAX installation completed successfully!")
    
    # Show success message
    frappe.msgprint(
        _("ERPMAX has been installed successfully! Enjoy your enhanced ERP experience."),
        title=_("Installation Complete"),
        indicator="green"
    )


def create_erpmax_custom_fields():
    """Create custom fields for ERPMAX"""
    
    custom_fields = {
        "Company": [
            {
                "fieldname": "erpmax_enhanced_features",
                "label": "Enhanced Features",
                "fieldtype": "Check",
                "default": 1,
                "description": "Enable ERPMAX enhanced features"
            },
            {
                "fieldname": "erpmax_theme_color", 
                "label": "Theme Color",
                "fieldtype": "Color",
                "default": "#1976D2"
            }
        ],
        "User": [
            {
                "fieldname": "erpmax_dashboard_preference",
                "label": "Dashboard Preference",
                "fieldtype": "Select",
                "options": "Standard\nAdvanced\nCustom",
                "default": "Standard"
            }
        ],
        "Customer": [
            {
                "fieldname": "erpmax_customer_score",
                "label": "Customer Score",
                "fieldtype": "Rating",
                "default": 5
            }
        ],
        "Item": [
            {
                "fieldname": "erpmax_popularity_score",
                "label": "Popularity Score",
                "fieldtype": "Float",
                "default": 0
            }
        ]
    }
    
    try:
        create_custom_fields(custom_fields, update=True)
        frappe.logger().info("ERPMAX custom fields created successfully")
    except Exception as e:
        frappe.logger().error(f"Error creating custom fields: {str(e)}")


def create_erpmax_property_setters():
    """Create property setters for ERPMAX"""
    
    property_setters = [
        {
            "doctype": "System Settings",
            "property": "app_name",
            "value": "ERPMAX"
        },
        {
            "doctype": "Website Settings",
            "property": "app_name",
            "value": "ERPMAX"
        },
        {
            "doctype": "Website Settings",
            "property": "app_logo",
            "value": "/assets/erpmax/images/erpmax-logo.svg"
        }
    ]
    
    for ps in property_setters:
        try:
            make_property_setter(
                ps["doctype"],
                None,
                ps["property"],
                ps["value"],
                "Data"
            )
        except Exception as e:
            frappe.logger().error(f"Error creating property setter: {str(e)}")


def create_default_data():
    """Create default data for ERPMAX"""
    
    # Create default company if not exists
    if not frappe.db.exists("Company", "ERPMAX Company"):
        company = frappe.get_doc({
            "doctype": "Company",
            "company_name": "ERPMAX Company",
            "abbr": "ERPMAX",
            "default_currency": "USD",
            "country": "United States",
            "erpmax_enhanced_features": 1,
            "erpmax_theme_color": "#1976D2"
        })
        company.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.logger().info("Default ERPMAX company created")


def set_app_settings():
    """Set application settings"""
    
    # Set system settings
    system_settings = frappe.get_single("System Settings")
    system_settings.app_name = "ERPMAX"
    system_settings.save(ignore_permissions=True)
    
    # Set website settings
    if frappe.db.exists("Website Settings", "Website Settings"):
        website_settings = frappe.get_single("Website Settings")
        website_settings.app_name = "ERPMAX"
        website_settings.app_logo = "/assets/erpmax/images/erpmax-logo.svg"
        website_settings.favicon = "/assets/erpmax/images/favicon.ico"
        website_settings.save(ignore_permissions=True)
    
    frappe.db.commit()
    frappe.logger().info("ERPMAX app settings configured")


def create_default_roles():
    """Create default user roles for ERPMAX"""
    
    roles = [
        {
            "role_name": "ERPMAX Manager",
            "description": "Full access to ERPMAX features"
        },
        {
            "role_name": "ERPMAX User",
            "description": "Standard user access to ERPMAX"
        }
    ]
    
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_data["role_name"],
                "description": role_data["description"]
            })
            role.insert(ignore_permissions=True)
    
    frappe.db.commit()
    frappe.logger().info("ERPMAX default roles created")
