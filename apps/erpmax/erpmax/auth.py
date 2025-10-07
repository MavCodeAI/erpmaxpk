# ERPMAX Authentication Enhancements
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import now


def validate_auth(doc, method):
    """Enhanced authentication validation for ERPMAX"""
    
    # Log authentication attempts
    frappe.logger().info(f"ERPMAX: Authentication attempt for user {doc.name}")
    
    # Add custom validation logic here
    if doc.name != "Administrator":
        # Check if user has ERPMAX access
        validate_erpmax_access(doc)
    
    # Log successful authentication
    frappe.logger().info(f"ERPMAX: User {doc.name} authenticated successfully")


def validate_erpmax_access(user_doc):
    """Validate user access to ERPMAX features"""
    
    # Check if user has required roles
    user_roles = frappe.get_roles(user_doc.name)
    
    # ERPMAX specific role validation
    erpmax_roles = ["ERPMAX Manager", "ERPMAX User", "System Manager"]
    
    has_access = any(role in erpmax_roles for role in user_roles)
    
    if not has_access:
        frappe.logger().warning(f"User {user_doc.name} does not have ERPMAX access")
        # You can add additional logic here if needed
    
    return has_access


@frappe.whitelist()
def get_user_permissions():
    """Get enhanced user permissions for ERPMAX"""
    
    user = frappe.session.user
    roles = frappe.get_roles(user)
    
    permissions = {
        "user": user,
        "roles": roles,
        "has_erpmax_access": any(role in ["ERPMAX Manager", "ERPMAX User", "System Manager"] for role in roles),
        "is_erpmax_manager": "ERPMAX Manager" in roles,
        "timestamp": now()
    }
    
    return permissions


def on_login(login_manager):
    """Enhanced login handler for ERPMAX"""
    
    user = login_manager.user
    
    # Log login
    frappe.logger().info(f"ERPMAX: User {user} logged in successfully")
    
    # Update last login timestamp
    frappe.db.set_value("User", user, "last_login", now())
    
    # Set ERPMAX session variables
    frappe.session["erpmax_session"] = True
    frappe.session["erpmax_login_time"] = now()
    
    # Add user to ERPMAX user group if not exists
    add_to_erpmax_group(user)


def add_to_erpmax_group(user):
    """Add user to ERPMAX user group"""
    
    try:
        # Check if ERPMAX User role exists
        if not frappe.db.exists("Role", "ERPMAX User"):
            # Create ERPMAX User role
            role = frappe.get_doc({
                "doctype": "Role",
                "role_name": "ERPMAX User",
                "description": "Standard ERPMAX user access"
            })
            role.insert(ignore_permissions=True)
        
        # Add role to user if not already added
        user_roles = frappe.get_roles(user)
        if "ERPMAX User" not in user_roles:
            user_doc = frappe.get_doc("User", user)
            user_doc.append("roles", {
                "role": "ERPMAX User"
            })
            user_doc.save(ignore_permissions=True)
            
        frappe.db.commit()
        
    except Exception as e:
        frappe.logger().error(f"Error adding user to ERPMAX group: {str(e)}")


def on_logout(login_manager):
    """Enhanced logout handler for ERPMAX"""
    
    user = login_manager.user if login_manager else frappe.session.user
    
    # Log logout
    frappe.logger().info(f"ERPMAX: User {user} logged out")
    
    # Clear ERPMAX session variables
    if "erpmax_session" in frappe.session:
        del frappe.session["erpmax_session"]
    if "erpmax_login_time" in frappe.session:
        del frappe.session["erpmax_login_time"]


@frappe.whitelist()
def check_erpmax_license():
    """Check ERPMAX license status"""
    
    # For open source version, always return valid
    return {
        "valid": True,
        "type": "Community",
        "features": ["Core ERP", "Modern UI", "Basic Support"],
        "expires": None,
        "message": "ERPMAX Community Edition - Free Forever"
    }


def validate_ip_restriction(user):
    """Validate IP restrictions for enhanced security"""
    
    # Get user's IP address
    ip_address = frappe.local.request.environ.get('REMOTE_ADDR')
    
    # You can add IP restriction logic here
    # For now, just log the IP
    frappe.logger().info(f"ERPMAX: User {user} accessing from IP {ip_address}")
    
    return True


@frappe.whitelist()
def get_security_settings():
    """Get ERPMAX security settings"""
    
    return {
        "password_policy": {
            "min_length": 8,
            "require_numbers": True,
            "require_symbols": True,
            "require_uppercase": True
        },
        "session_timeout": 3600,  # 1 hour
        "max_login_attempts": 5,
        "lockout_duration": 900,  # 15 minutes
        "two_factor_auth": False  # Can be enabled later
    }
