# ERPMAX API Functions
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import nowdate, now, get_url


@frappe.whitelist()
def get_app_info():
    """Get ERPMAX application information"""
    return {
        "app_name": "erpmax",
        "app_title": "ERPMAX",
        "version": "1.0.0",
        "description": "Enhanced ERP solution with modern features",
        "status": "active",
        "timestamp": now()
    }


@frappe.whitelist()
def get_company_info():
    """Get company information for templates"""
    company = frappe.defaults.get_user_default("Company")
    if not company:
        company = frappe.get_all("Company", limit=1)
        company = company[0].name if company else "ERPMAX Company"
    
    company_doc = frappe.get_doc("Company", company) if frappe.db.exists("Company", company) else None
    
    return {
        "company_name": company,
        "company_abbr": company_doc.abbr if company_doc else "ERPMAX",
        "default_currency": company_doc.default_currency if company_doc else "USD",
        "country": company_doc.country if company_doc else "United States"
    }


@frappe.whitelist()
def get_user_info():
    """Get current user information"""
    user = frappe.session.user
    user_doc = frappe.get_doc("User", user)
    
    return {
        "user_id": user,
        "full_name": user_doc.full_name,
        "email": user_doc.email,
        "role_profile": user_doc.role_profile_name,
        "language": user_doc.language or "en",
        "time_zone": user_doc.time_zone or "UTC"
    }


@frappe.whitelist()
def clear_cache():
    """Clear application cache"""
    frappe.clear_cache()
    return {"message": "Cache cleared successfully"}


@frappe.whitelist()
def log_creation(doc, method):
    """Log document creation for audit"""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return
    
    # Log creation event
    frappe.logger().info(f"ERPMAX: {doc.doctype} {doc.name} created by {frappe.session.user}")


@frappe.whitelist()
def get_events(start, end, user=None, for_reminder=False, filters=None):
    """Enhanced event fetching with ERPMAX customizations"""
    from frappe.desk.doctype.event.event import get_events as get_frappe_events
    
    # Get standard events
    events = get_frappe_events(start, end, user, for_reminder, filters)
    
    # Add ERPMAX customizations
    for event in events:
        event['app'] = 'erpmax'
        event['enhanced'] = True
    
    return events


@frappe.whitelist()
def get_dashboard_data():
    """Get dashboard data for ERPMAX"""
    return {
        "total_customers": frappe.db.count("Customer"),
        "total_suppliers": frappe.db.count("Supplier"),
        "total_items": frappe.db.count("Item"),
        "total_sales_orders": frappe.db.count("Sales Order", {"docstatus": 1}),
        "total_purchase_orders": frappe.db.count("Purchase Order", {"docstatus": 1}),
        "app_info": get_app_info()
    }
