import frappe


ALLOWED_QUERY_TYPES = {
    "sales_by_year": "ai_business_analytics.api.analytics.sales_by_year",
    "sales_by_city": "ai_business_analytics.api.analytics.sales_by_city",
    "production_status": "ai_business_analytics.api.analytics.production_status",
    "revenue_by_category": "ai_business_analytics.api.analytics.revenue_by_category",
    "paid_not_started": "ai_business_analytics.api.analytics.paid_not_started",
    "customers_recent_purchases": "ai_business_analytics.api.analytics.customers_recent_purchases",
}


DATE_FILTERED_QUERIES = {
    "sales_by_city",
    "revenue_by_category",
    "customers_recent_purchases"
}


def execute_plan(plan):
    """Execute only approved analytics functions."""

    if not isinstance(plan, dict):
        return {
            "status": "error",
            "message": "Invalid analytics plan."
        }

    query_type = plan.get("query_type")

    if query_type not in ALLOWED_QUERY_TYPES:
        return {
            "status": "unsupported",
            "message": "The requested analytics operation is not supported."
        }

    method = ALLOWED_QUERY_TYPES[query_type]

    try:
        if query_type == "customers_recent_purchases":
            days = plan.get("days", 30)

            try:
                days = int(days)
            except (TypeError, ValueError):
                days = 30

            days = max(1, min(days, 3650))

            result = frappe.call(
                method,
                days=days,
            )

        elif query_type in DATE_FILTERED_QUERIES:
            start_date = plan.get("start_date")
            end_date = plan.get("end_date")

            result = frappe.call(
                method,
                start_date=start_date,
                end_date=end_date,
            )

        else:
            result = frappe.call(method)

        return {
            "status": "success",
            "query_type": query_type,
            "data": result
        }

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "AI Business Analytics Planner Error"
        )

        return {
            "status": "error",
            "message": "Unable to execute the requested analytics query."
        }

