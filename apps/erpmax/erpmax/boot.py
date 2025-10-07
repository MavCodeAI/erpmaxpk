# ERPMAX Boot Configuration
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _


def boot_session(bootinfo):
    """Boot session with ERPMAX customizations"""
    
    # Add ERPMAX branding
    bootinfo["app_name"] = "erpmax"
    bootinfo["app_title"] = "ERPMAX"
    bootinfo["app_version"] = "1.0.0"
    bootinfo["app_logo_url"] = "/assets/erpmax/images/erpmax-logo.svg"
    
    # Add custom user preferences
    if frappe.session.user != "Guest":
        bootinfo["user_info"] = {
            "full_name": frappe.db.get_value("User", frappe.session.user, "full_name"),
            "email": frappe.session.user,
            "language": frappe.db.get_value("User", frappe.session.user, "language") or "en"
        }
    
    # Add ERPMAX specific settings
    bootinfo["erpmax_settings"] = {
        "theme_color": "#1976D2",
        "secondary_color": "#FFC107",
        "enable_animations": True,
        "enable_dark_mode": True,
        "show_app_launcher": True
    }
    
    # Add custom navbar items
    bootinfo["navbar_settings"] = {
        "title": "ERPMAX",
        "logo": "/assets/erpmax/images/erpmax-logo.svg",
        "favicon": "/assets/erpmax/images/favicon.ico"
    }
    
    # Add custom desk settings
    bootinfo["desk_settings"] = {
        "background_color": "#f5f5f5",
        "card_shadow": True,
        "rounded_corners": True
    }
    
    # Add ERPMAX modules
    bootinfo["erpmax_modules"] = [
        "Dashboard",
        "Sales", 
        "Purchase",
        "Inventory",
        "Accounting",
        "HR",
        "CRM",
        "Reports",
        "Settings"
    ]
