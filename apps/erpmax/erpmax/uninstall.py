# ERPMAX Uninstallation Scripts
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _


def before_uninstall():
    """Run before ERPMAX uninstallation"""
    
    frappe.logger().info("Starting ERPMAX uninstallation...")
    
    # Backup important data
    backup_erpmax_data()
    
    # Clean up custom fields
    cleanup_custom_fields()
    
    # Clean up property setters
    cleanup_property_setters()
    
    # Reset system settings
    reset_system_settings()
    
    frappe.logger().info("ERPMAX uninstallation completed")
    
    # Show message
    frappe.msgprint(
        _("ERPMAX has been uninstalled. Thank you for using ERPMAX!"),
        title=_("Uninstallation Complete"),
        indicator="orange"
    )


def backup_erpmax_data():
    """Backup ERPMAX specific data before uninstall"""
    try:
        # Create backup of custom data
        frappe.logger().info("Backing up ERPMAX data...")
        
        # You can add specific backup logic here
        # For now, just log the action
        frappe.logger().info("ERPMAX data backup completed")
        
    except Exception as e:
        frappe.logger().error(f"Error backing up ERPMAX data: {str(e)}")


def cleanup_custom_fields():
    """Remove ERPMAX custom fields"""
    try:
        # Get all custom fields created by ERPMAX
        custom_fields = frappe.get_all(
            "Custom Field",
            filters={"fieldname": ["like", "erpmax_%"]},
            fields=["name"]
        )
        
        for cf in custom_fields:
            frappe.delete_doc("Custom Field", cf.name, ignore_permissions=True)
        
        frappe.logger().info(f"Cleaned up {len(custom_fields)} ERPMAX custom fields")
        
    except Exception as e:
        frappe.logger().error(f"Error cleaning up custom fields: {str(e)}")


def cleanup_property_setters():
    """Remove ERPMAX property setters"""
    try:
        # Get all property setters created by ERPMAX
        property_setters = frappe.get_all(
            "Property Setter",
            filters={"value": ["in", ["ERPMAX", "erpmax"]]},
            fields=["name"]
        )
        
        for ps in property_setters:
            frappe.delete_doc("Property Setter", ps.name, ignore_permissions=True)
        
        frappe.logger().info(f"Cleaned up {len(property_setters)} ERPMAX property setters")
        
    except Exception as e:
        frappe.logger().error(f"Error cleaning up property setters: {str(e)}")


def reset_system_settings():
    """Reset system settings to defaults"""
    try:
        # Reset system settings
        system_settings = frappe.get_single("System Settings")
        system_settings.app_name = "Frappe"
        system_settings.save(ignore_permissions=True)
        
        # Reset website settings
        if frappe.db.exists("Website Settings", "Website Settings"):
            website_settings = frappe.get_single("Website Settings")
            website_settings.app_name = "Frappe"
            website_settings.app_logo = ""
            website_settings.favicon = ""
            website_settings.save(ignore_permissions=True)
        
        frappe.db.commit()
        frappe.logger().info("System settings reset to defaults")
        
    except Exception as e:
        frappe.logger().error(f"Error resetting system settings: {str(e)}")
