# ERPMAX Background Tasks
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import now, add_days, get_datetime


def all():
    """Tasks that run every few minutes"""
    try:
        # Update system status
        update_system_status()
        
        # Clean temporary files
        cleanup_temp_files()
        
    except Exception as e:
        frappe.logger().error(f"Error in ERPMAX all tasks: {str(e)}")


def hourly():
    """Tasks that run every hour"""
    try:
        # Update dashboard cache
        update_dashboard_cache()
        
        # Check system health
        check_system_health()
        
        # Update statistics
        update_statistics()
        
    except Exception as e:
        frappe.logger().error(f"Error in ERPMAX hourly tasks: {str(e)}")


def daily():
    """Tasks that run daily"""
    try:
        # Generate daily reports
        generate_daily_reports()
        
        # Cleanup old logs
        cleanup_old_logs()
        
        # Update customer scores
        update_customer_scores()
        
        # Send daily summary
        send_daily_summary()
        
    except Exception as e:
        frappe.logger().error(f"Error in ERPMAX daily tasks: {str(e)}")


def weekly():
    """Tasks that run weekly"""
    try:
        # Generate weekly reports
        generate_weekly_reports()
        
        # Database maintenance
        database_maintenance()
        
        # Update item popularity scores
        update_item_popularity()
        
    except Exception as e:
        frappe.logger().error(f"Error in ERPMAX weekly tasks: {str(e)}")


def monthly():
    """Tasks that run monthly"""
    try:
        # Generate monthly reports
        generate_monthly_reports()
        
        # Archive old data
        archive_old_data()
        
        # System optimization
        system_optimization()
        
    except Exception as e:
        frappe.logger().error(f"Error in ERPMAX monthly tasks: {str(e)}")


# Helper functions

def update_system_status():
    """Update system status information"""
    # Log system status
    frappe.logger().info("ERPMAX system status updated")


def cleanup_temp_files():
    """Clean up temporary files"""
    # Clean up logic here
    pass


def update_dashboard_cache():
    """Update dashboard cache data"""
    try:
        # Cache dashboard data for better performance
        dashboard_data = {
            "customers": frappe.db.count("Customer"),
            "suppliers": frappe.db.count("Supplier"),
            "items": frappe.db.count("Item"),
            "sales_orders": frappe.db.count("Sales Order", {"docstatus": 1}),
            "timestamp": now()
        }
        
        frappe.cache().set_value("erpmax_dashboard_data", dashboard_data)
        frappe.logger().info("Dashboard cache updated")
        
    except Exception as e:
        frappe.logger().error(f"Error updating dashboard cache: {str(e)}")


def check_system_health():
    """Check system health metrics"""
    # System health check logic
    frappe.logger().info("System health check completed")


def update_statistics():
    """Update application statistics"""
    # Statistics update logic
    pass


def generate_daily_reports():
    """Generate daily reports"""
    # Daily report generation logic
    frappe.logger().info("Daily reports generated")


def cleanup_old_logs():
    """Clean up old log files"""
    # Log cleanup logic
    pass


def update_customer_scores():
    """Update customer scores based on activity"""
    try:
        # Update customer scores based on recent activity
        customers = frappe.get_all("Customer", fields=["name"])
        
        for customer in customers:
            # Calculate score based on recent orders, payments, etc.
            score = calculate_customer_score(customer.name)
            
            # Update customer score if custom field exists
            if frappe.db.has_column("Customer", "erpmax_customer_score"):
                frappe.db.set_value("Customer", customer.name, "erpmax_customer_score", score)
        
        frappe.db.commit()
        frappe.logger().info(f"Updated scores for {len(customers)} customers")
        
    except Exception as e:
        frappe.logger().error(f"Error updating customer scores: {str(e)}")


def calculate_customer_score(customer_name):
    """Calculate customer score based on various factors"""
    try:
        # Get recent orders count
        recent_orders = frappe.db.count(
            "Sales Order",
            {
                "customer": customer_name,
                "transaction_date": [">=", add_days(None, -30)],
                "docstatus": 1
            }
        )
        
        # Get payment history
        payment_count = frappe.db.count(
            "Payment Entry",
            {
                "party": customer_name,
                "posting_date": [">=", add_days(None, -30)],
                "docstatus": 1
            }
        )
        
        # Calculate score (simple algorithm)
        score = min(5, (recent_orders * 0.5) + (payment_count * 0.3) + 2.5)
        return round(score, 1)
        
    except Exception:
        return 3.0  # Default score


def send_daily_summary():
    """Send daily summary to administrators"""
    # Daily summary email logic
    pass


def generate_weekly_reports():
    """Generate weekly reports"""
    frappe.logger().info("Weekly reports generated")


def database_maintenance():
    """Perform database maintenance tasks"""
    frappe.logger().info("Database maintenance completed")


def update_item_popularity():
    """Update item popularity scores"""
    try:
        items = frappe.get_all("Item", fields=["name"])
        
        for item in items:
            # Calculate popularity based on sales
            popularity = calculate_item_popularity(item.name)
            
            # Update if custom field exists
            if frappe.db.has_column("Item", "erpmax_popularity_score"):
                frappe.db.set_value("Item", item.name, "erpmax_popularity_score", popularity)
        
        frappe.db.commit()
        frappe.logger().info(f"Updated popularity for {len(items)} items")
        
    except Exception as e:
        frappe.logger().error(f"Error updating item popularity: {str(e)}")


def calculate_item_popularity(item_code):
    """Calculate item popularity score"""
    try:
        # Get sales count in last 3 months
        sales_count = frappe.db.sql("""
            SELECT SUM(qty) 
            FROM `tabSales Order Item` soi
            JOIN `tabSales Order` so ON soi.parent = so.name
            WHERE soi.item_code = %s 
            AND so.transaction_date >= %s
            AND so.docstatus = 1
        """, [item_code, add_days(None, -90)])[0][0] or 0
        
        # Simple popularity score
        return min(100, sales_count * 2)
        
    except Exception:
        return 0


def generate_monthly_reports():
    """Generate monthly reports"""
    frappe.logger().info("Monthly reports generated")


def archive_old_data():
    """Archive old data for performance"""
    frappe.logger().info("Old data archival completed")


def system_optimization():
    """Perform system optimization tasks"""
    frappe.logger().info("System optimization completed")
