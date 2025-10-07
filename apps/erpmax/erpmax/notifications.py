# ERPMAX Notification Configuration
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _


def get_notification_config():
    """Enhanced notification configuration for ERPMAX"""
    
    return {
        "for_doctype": {
            "Customer": {
                "status": "Active",
                "conditions": [
                    {
                        "condition": "doc.erpmax_customer_score < 3",
                        "message": _("Customer has low rating"),
                        "alert_type": "warning"
                    }
                ]
            },
            "Sales Order": {
                "status": "To Deliver",
                "conditions": [
                    {
                        "condition": "doc.delivery_status == 'Overdue'",
                        "message": _("Sales Order delivery is overdue"),
                        "alert_type": "danger"
                    }
                ]
            },
            "Purchase Order": {
                "status": "To Receive",
                "conditions": [
                    {
                        "condition": "doc.status == 'Overdue'",
                        "message": _("Purchase Order is overdue"),
                        "alert_type": "warning"
                    }
                ]
            },
            "Sales Invoice": {
                "status": "Overdue",
                "conditions": [
                    {
                        "condition": "doc.outstanding_amount > 0",
                        "message": _("Payment overdue"),
                        "alert_type": "danger"
                    }
                ]
            },
            "Item": {
                "status": "Active",
                "conditions": [
                    {
                        "condition": "doc.erpmax_popularity_score < 10",
                        "message": _("Item has low popularity"),
                        "alert_type": "info"
                    }
                ]
            }
        },
        "for_module": {
            "Stock": {
                "label": _("Stock Alerts"),
                "conditions": [
                    {
                        "condition": "stock_level < reorder_level",
                        "message": _("Items below reorder level"),
                        "alert_type": "warning"
                    }
                ]
            },
            "Accounts": {
                "label": _("Accounting Alerts"),
                "conditions": [
                    {
                        "condition": "overdue_invoices > 0",
                        "message": _("Overdue invoices pending"),
                        "alert_type": "danger"
                    }
                ]
            },
            "Selling": {
                "label": _("Sales Alerts"),
                "conditions": [
                    {
                        "condition": "pending_quotations > 5",
                        "message": _("Multiple quotations pending"),
                        "alert_type": "info"
                    }
                ]
            }
        },
        "targets": {
            "Customer": {
                "color": "#1976D2",
                "conditions": [
                    "frappe.defaults.get_user_default('Company') == doc.company"
                ]
            },
            "Sales Order": {
                "color": "#4CAF50",
                "conditions": [
                    "doc.grand_total > 1000"
                ]
            },
            "Sales Invoice": {
                "color": "#FF9800",
                "conditions": [
                    "doc.outstanding_amount > 0"
                ]
            }
        },
        "open_count_doctype": {
            "Customer": {
                "doctype": "Customer",
                "filters": {"disabled": 0}
            },
            "Supplier": {
                "doctype": "Supplier", 
                "filters": {"disabled": 0}
            },
            "Item": {
                "doctype": "Item",
                "filters": {"disabled": 0}
            },
            "Sales Order": {
                "doctype": "Sales Order",
                "filters": {"status": ["in", ["Draft", "To Deliver"]]}
            },
            "Purchase Order": {
                "doctype": "Purchase Order",
                "filters": {"status": ["in", ["Draft", "To Receive"]]}
            },
            "Quotation": {
                "doctype": "Quotation",
                "filters": {"status": "Open"}
            }
        }
    }


@frappe.whitelist()
def get_notifications_for_user(user=None):
    """Get notifications for specific user"""
    
    if not user:
        user = frappe.session.user
    
    notifications = []
    
    # Get overdue invoices
    overdue_invoices = get_overdue_invoices_for_user(user)
    if overdue_invoices:
        notifications.append({
            "type": "danger",
            "title": _("Overdue Invoices"),
            "message": _(f"{overdue_invoices} invoices are overdue"),
            "doctype": "Sales Invoice",
            "count": overdue_invoices
        })
    
    # Get low stock items
    low_stock_items = get_low_stock_items()
    if low_stock_items:
        notifications.append({
            "type": "warning",
            "title": _("Low Stock Alert"),
            "message": _(f"{low_stock_items} items are below reorder level"),
            "doctype": "Item",
            "count": low_stock_items
        })
    
    # Get pending quotations
    pending_quotations = get_pending_quotations_count()
    if pending_quotations > 5:
        notifications.append({
            "type": "info",
            "title": _("Pending Quotations"),
            "message": _(f"{pending_quotations} quotations are pending response"),
            "doctype": "Quotation",
            "count": pending_quotations
        })
    
    # Get user-specific notifications
    user_notifications = get_user_specific_notifications(user)
    notifications.extend(user_notifications)
    
    return notifications


def get_overdue_invoices_for_user(user):
    """Get overdue invoices count for user"""
    
    user_roles = frappe.get_roles(user)
    
    # If user is sales manager, show all overdue invoices
    if "Sales Manager" in user_roles or "Accounts Manager" in user_roles:
        return frappe.db.count(
            "Sales Invoice",
            {
                "due_date": ["<", frappe.utils.nowdate()],
                "outstanding_amount": [">=", 0.01],
                "docstatus": 1
            }
        )
    
    # Otherwise show only user's invoices
    return frappe.db.count(
        "Sales Invoice",
        {
            "owner": user,
            "due_date": ["<", frappe.utils.nowdate()],
            "outstanding_amount": [">=", 0.01],
            "docstatus": 1
        }
    )


def get_low_stock_items():
    """Get count of items with low stock"""
    
    return frappe.db.sql("""
        SELECT COUNT(*) FROM `tabBin` b
        JOIN `tabItem` i ON b.item_code = i.item_code
        WHERE b.actual_qty <= COALESCE(b.reorder_level, 0)
        AND i.disabled = 0
        AND i.is_stock_item = 1
    """)[0][0] or 0


def get_pending_quotations_count():
    """Get pending quotations count"""
    
    return frappe.db.count(
        "Quotation",
        {
            "status": "Open",
            "docstatus": 1,
            "valid_till": [">=", frappe.utils.nowdate()]
        }
    )


def get_user_specific_notifications(user):
    """Get user-specific notifications"""
    
    notifications = []
    
    # Check for documents assigned to user
    assigned_docs = frappe.db.sql("""
        SELECT 
            reference_doctype,
            COUNT(*) as count
        FROM `tabToDo`
        WHERE owner = %(user)s
        AND status = 'Open'
        GROUP BY reference_doctype
    """, {"user": user}, as_dict=True)
    
    for doc in assigned_docs:
        if doc.count > 0:
            notifications.append({
                "type": "info",
                "title": _(f"Assigned {doc.reference_doctype}"),
                "message": _(f"{doc.count} {doc.reference_doctype} assigned to you"),
                "doctype": doc.reference_doctype,
                "count": doc.count
            })
    
    # Check for documents created by user needing attention
    draft_docs = frappe.db.sql("""
        SELECT 
            'Sales Order' as doctype,
            COUNT(*) as count
        FROM `tabSales Order`
        WHERE owner = %(user)s
        AND docstatus = 0
        
        UNION ALL
        
        SELECT 
            'Purchase Order' as doctype,
            COUNT(*) as count
        FROM `tabPurchase Order`
        WHERE owner = %(user)s
        AND docstatus = 0
        
        UNION ALL
        
        SELECT 
            'Quotation' as doctype,
            COUNT(*) as count
        FROM `tabQuotation`
        WHERE owner = %(user)s
        AND docstatus = 0
    """, {"user": user}, as_dict=True)
    
    for doc in draft_docs:
        if doc.count > 0:
            notifications.append({
                "type": "warning",
                "title": _(f"Draft {doc.doctype}"),
                "message": _(f"{doc.count} draft {doc.doctype} need submission"),
                "doctype": doc.doctype,
                "count": doc.count
            })
    
    return notifications


@frappe.whitelist()
def mark_notification_as_read(notification_id):
    """Mark notification as read"""
    
    # Implementation for marking notifications as read
    # This would typically update a user preference or log table
    
    frappe.logger().info(f"Notification {notification_id} marked as read by {frappe.session.user}")
    
    return {"status": "success"}


@frappe.whitelist()
def get_notification_settings(user=None):
    """Get notification settings for user"""
    
    if not user:
        user = frappe.session.user
    
    # Default notification settings
    settings = {
        "email_notifications": True,
        "push_notifications": True,
        "desktop_notifications": True,
        "notification_frequency": "immediate",  # immediate, hourly, daily
        "categories": {
            "sales": True,
            "purchase": True,
            "stock": True,
            "accounts": True,
            "system": False
        }
    }
    
    # Get user-specific settings from User Preference or similar
    user_settings = frappe.db.get_value(
        "User", 
        user, 
        ["email_notifications", "notification_settings"],
        as_dict=True
    )
    
    if user_settings:
        settings.update(user_settings)
    
    return settings
