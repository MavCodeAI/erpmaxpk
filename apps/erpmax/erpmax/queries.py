# ERPMAX Database Queries
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import nowdate, add_days, get_datetime


def get_permission_query_conditions_for_event(user):
    """Enhanced permission query for events in ERPMAX"""
    
    if not user:
        user = frappe.session.user
    
    # ERPMAX managers can see all events
    if "ERPMAX Manager" in frappe.get_roles(user):
        return ""
    
    # Regular users can see their own events and public events
    return f"""(
        `tabEvent`.owner = '{user}' 
        OR `tabEvent`.event_type = 'Public'
        OR `tabEvent`.name in (
            SELECT parent FROM `tabEvent User` 
            WHERE `tabEvent User`.user = '{user}'
        )
    )"""


def has_permission(doc, user):
    """Enhanced permission check for ERPMAX"""
    
    if not user:
        user = frappe.session.user
    
    # System Manager and ERPMAX Manager have full access
    user_roles = frappe.get_roles(user)
    if "System Manager" in user_roles or "ERPMAX Manager" in user_roles:
        return True
    
    # Check document-specific permissions
    if doc.doctype == "Event":
        return has_event_permission(doc, user)
    
    # Default permission check
    return frappe.has_permission(doc.doctype, "read", doc, user)


def has_event_permission(doc, user):
    """Check event permission for ERPMAX"""
    
    # Owner can access
    if doc.owner == user:
        return True
    
    # Public events are accessible
    if doc.event_type == "Public":
        return True
    
    # Check if user is in event participants
    participants = frappe.get_all(
        "Event User",
        filters={"parent": doc.name, "user": user},
        fields=["user"]
    )
    
    return len(participants) > 0


@frappe.whitelist()
def get_dashboard_data(user=None):
    """Get enhanced dashboard data for ERPMAX"""
    
    if not user:
        user = frappe.session.user
    
    # Base dashboard data
    data = {
        "customers": frappe.db.count("Customer"),
        "suppliers": frappe.db.count("Supplier"),
        "items": frappe.db.count("Item"),
        "users": frappe.db.count("User", {"enabled": 1})
    }
    
    # Sales data
    data.update(get_sales_data())
    
    # Purchase data
    data.update(get_purchase_data())
    
    # Recent activities
    data["recent_activities"] = get_recent_activities(user)
    
    # User-specific data
    data["user_stats"] = get_user_stats(user)
    
    return data


def get_sales_data():
    """Get sales statistics"""
    
    today = nowdate()
    month_start = today.replace(day=1)
    
    return {
        "sales_orders_today": frappe.db.count(
            "Sales Order",
            {"transaction_date": today, "docstatus": 1}
        ),
        "sales_orders_month": frappe.db.count(
            "Sales Order",
            {"transaction_date": [">=", month_start], "docstatus": 1}
        ),
        "sales_invoices_today": frappe.db.count(
            "Sales Invoice",
            {"posting_date": today, "docstatus": 1}
        ),
        "sales_invoices_month": frappe.db.count(
            "Sales Invoice",
            {"posting_date": [">=", month_start], "docstatus": 1}
        )
    }


def get_purchase_data():
    """Get purchase statistics"""
    
    today = nowdate()
    month_start = today.replace(day=1)
    
    return {
        "purchase_orders_today": frappe.db.count(
            "Purchase Order",
            {"transaction_date": today, "docstatus": 1}
        ),
        "purchase_orders_month": frappe.db.count(
            "Purchase Order",
            {"transaction_date": [">=", month_start], "docstatus": 1}
        ),
        "purchase_invoices_today": frappe.db.count(
            "Purchase Invoice",
            {"posting_date": today, "docstatus": 1}
        ),
        "purchase_invoices_month": frappe.db.count(
            "Purchase Invoice",
            {"posting_date": [">=", month_start], "docstatus": 1}
        )
    }


def get_recent_activities(user, limit=10):
    """Get recent activities for user"""
    
    activities = []
    
    # Get recent documents created by user
    recent_docs = frappe.db.sql("""
        SELECT 
            creation,
            modified,
            owner,
            modified_by,
            doctype,
            name
        FROM (
            SELECT creation, modified, owner, modified_by, 'Sales Order' as doctype, name
            FROM `tabSales Order` 
            WHERE owner = %(user)s OR modified_by = %(user)s
            
            UNION ALL
            
            SELECT creation, modified, owner, modified_by, 'Customer' as doctype, name
            FROM `tabCustomer`
            WHERE owner = %(user)s OR modified_by = %(user)s
            
            UNION ALL
            
            SELECT creation, modified, owner, modified_by, 'Item' as doctype, name
            FROM `tabItem`
            WHERE owner = %(user)s OR modified_by = %(user)s
        ) as combined
        ORDER BY modified DESC
        LIMIT %(limit)s
    """, {"user": user, "limit": limit}, as_dict=True)
    
    for doc in recent_docs:
        activities.append({
            "type": "document",
            "doctype": doc.doctype,
            "name": doc.name,
            "action": "created" if doc.owner == user else "modified",
            "timestamp": doc.modified,
            "user": doc.modified_by
        })
    
    return activities


def get_user_stats(user):
    """Get user-specific statistics"""
    
    return {
        "documents_created_today": frappe.db.sql("""
            SELECT COUNT(*) FROM (
                SELECT name FROM `tabSales Order` WHERE owner = %(user)s AND DATE(creation) = %(today)s
                UNION ALL
                SELECT name FROM `tabCustomer` WHERE owner = %(user)s AND DATE(creation) = %(today)s
                UNION ALL
                SELECT name FROM `tabItem` WHERE owner = %(user)s AND DATE(creation) = %(today)s
                UNION ALL
                SELECT name FROM `tabSupplier` WHERE owner = %(user)s AND DATE(creation) = %(today)s
            ) as combined
        """, {"user": user, "today": nowdate()})[0][0] or 0,
        
        "login_count_month": frappe.db.count(
            "Activity Log",
            {
                "user": user,
                "status": "Success",
                "operation": "Login",
                "creation": [">=", nowdate().replace(day=1)]
            }
        ),
        
        "last_login": frappe.db.get_value("User", user, "last_login")
    }


@frappe.whitelist()
def get_quick_stats():
    """Get quick statistics for ERPMAX dashboard"""
    
    return {
        "total_revenue_month": get_monthly_revenue(),
        "total_orders_month": get_monthly_orders(),
        "top_customers": get_top_customers(),
        "top_items": get_top_items(),
        "pending_quotations": get_pending_quotations(),
        "overdue_invoices": get_overdue_invoices()
    }


def get_monthly_revenue():
    """Get current month revenue"""
    
    month_start = nowdate().replace(day=1)
    
    revenue = frappe.db.sql("""
        SELECT COALESCE(SUM(grand_total), 0) as revenue
        FROM `tabSales Invoice`
        WHERE docstatus = 1 
        AND posting_date >= %s
    """, [month_start])[0][0] or 0
    
    return float(revenue)


def get_monthly_orders():
    """Get current month orders count"""
    
    month_start = nowdate().replace(day=1)
    
    return frappe.db.count(
        "Sales Order",
        {"transaction_date": [">=", month_start], "docstatus": 1}
    )


def get_top_customers(limit=5):
    """Get top customers by revenue"""
    
    customers = frappe.db.sql("""
        SELECT 
            customer,
            customer_name,
            SUM(grand_total) as total_revenue,
            COUNT(*) as total_orders
        FROM `tabSales Invoice`
        WHERE docstatus = 1
        AND posting_date >= %s
        GROUP BY customer
        ORDER BY total_revenue DESC
        LIMIT %s
    """, [add_days(nowdate(), -90), limit], as_dict=True)
    
    return customers


def get_top_items(limit=5):
    """Get top selling items"""
    
    items = frappe.db.sql("""
        SELECT 
            sii.item_code,
            sii.item_name,
            SUM(sii.qty) as total_qty,
            SUM(sii.amount) as total_amount
        FROM `tabSales Invoice Item` sii
        JOIN `tabSales Invoice` si ON sii.parent = si.name
        WHERE si.docstatus = 1
        AND si.posting_date >= %s
        GROUP BY sii.item_code
        ORDER BY total_amount DESC
        LIMIT %s
    """, [add_days(nowdate(), -30), limit], as_dict=True)
    
    return items


def get_pending_quotations():
    """Get pending quotations count"""
    
    return frappe.db.count(
        "Quotation",
        {"status": "Open", "docstatus": 1}
    )


def get_overdue_invoices():
    """Get overdue invoices count"""
    
    return frappe.db.count(
        "Sales Invoice",
        {
            "due_date": ["<", nowdate()],
            "outstanding_amount": [">=", 0.01],
            "docstatus": 1
        }
    )
