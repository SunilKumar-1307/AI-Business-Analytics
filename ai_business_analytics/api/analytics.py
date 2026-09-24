import time

import frappe


# ----------------------------------------------------------------------
# Sales by Year
# ----------------------------------------------------------------------

@frappe.whitelist()
def sales_by_year():
    """Return total sales grouped by year."""

    return frappe.db.sql(
        """
        SELECT
            YEAR(order_date) AS year,
            ROUND(SUM(total_amount), 2) AS total_sales
        FROM `tabBA Order`
        GROUP BY YEAR(order_date)
        ORDER BY YEAR(order_date)
        """,
        as_dict=True,
    )


# ----------------------------------------------------------------------
# Sales by City
# ----------------------------------------------------------------------

@frappe.whitelist()
def sales_by_city(start_date=None, end_date=None):
    """Return total sales grouped by city."""

    if not start_date:
        start_date = "2025-01-01"

    if not end_date:
        end_date = "2025-12-31"

    return frappe.db.sql(
        """
        SELECT
            city,
            ROUND(SUM(total_amount), 2) AS total_sales
        FROM `tabBA Order`
        WHERE order_date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY city
        ORDER BY total_sales DESC
        """,
        {
            "start_date": start_date,
            "end_date": end_date,
        },
        as_dict=True,
    )


# ----------------------------------------------------------------------
# Production Status
# ----------------------------------------------------------------------

@frappe.whitelist()
def production_status():
    """Return order counts grouped by production status."""

    return frappe.db.sql(
        """
        SELECT
            production_status,
            COUNT(*) AS order_count
        FROM `tabBA Production`
        GROUP BY production_status
        ORDER BY order_count DESC
        """,
        as_dict=True,
    )


# ----------------------------------------------------------------------
# Revenue by Product Category
# ----------------------------------------------------------------------

@frappe.whitelist()
def revenue_by_category(start_date=None, end_date=None):
    """Return revenue grouped by product category."""

    if not start_date:
        start_date = "2025-01-01"

    if not end_date:
        end_date = "2025-12-31"

    return frappe.db.sql(
        """
        SELECT
            p.category,
            ROUND(SUM(oi.amount), 2) AS total_revenue
        FROM `tabBA Order Item` oi
        INNER JOIN `tabBA Product` p
            ON p.name = oi.product
        INNER JOIN `tabBA Order` o
            ON o.name = oi.order
        WHERE o.order_date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY p.category
        ORDER BY total_revenue DESC
        """,
        {
            "start_date": start_date,
            "end_date": end_date,
        },
        as_dict=True,
    )


# ----------------------------------------------------------------------
# Paid Orders + Production Not Started
# ----------------------------------------------------------------------

@frappe.whitelist()
def paid_not_started():
    """Return customers whose orders are paid but production has not started."""

    return frappe.db.sql(
        """
        SELECT DISTINCT
            c.customer_name,
            c.email,
            c.city
        FROM `tabBA Customer` c
        INNER JOIN `tabBA Order` o
            ON o.customer = c.name
        INNER JOIN `tabBA Payment` p
            ON p.order = o.name
        INNER JOIN `tabBA Production` pr
            ON pr.order = o.name
        WHERE p.payment_status = 'Paid'
          AND pr.production_status = 'Not Started'
        ORDER BY c.customer_name
        """,
        as_dict=True,
    )


# ----------------------------------------------------------------------
# Customers with Recent Purchases
# ----------------------------------------------------------------------

@frappe.whitelist()
def customers_recent_purchases(days=30):
    """
    Return customers who purchased recently.

    The time period is calculated relative to the latest order date
    available in the synthetic dataset rather than the actual current date.
    This keeps the query useful when the dataset's dates are historical.
    """

    try:
        days = int(days)
    except (TypeError, ValueError):
        days = 30

    days = max(1, min(days, 3650))

    return frappe.db.sql(
        """
        SELECT
            customer_name,
            email,
            city,
            order_date AS latest_order_date,
            total_amount AS latest_order_amount
        FROM (
            SELECT
                c.customer_name,
                c.email,
                c.city,
                o.order_date,
                o.total_amount,
                ROW_NUMBER() OVER (
                    PARTITION BY o.customer
                    ORDER BY o.order_date DESC, o.name DESC
                ) AS row_num
            FROM `tabBA Customer` c
            INNER JOIN `tabBA Order` o
                ON o.customer = c.name
            WHERE o.order_date >= DATE_SUB(
                (
                    SELECT MAX(order_date)
                    FROM `tabBA Order`
                ),
                INTERVAL %(days)s DAY
            )
        ) recent
        WHERE row_num = 1
        ORDER BY latest_order_date DESC
        """,
        {
            "days": days,
        },
        as_dict=True,
    )


# ----------------------------------------------------------------------
# AI / Natural Language Question
# ----------------------------------------------------------------------

@frappe.whitelist()
def ask_question(question):
    """Use the local LLM to classify and execute a business question."""

    if not question or not question.strip():
        return {
            "status": "error",
            "message": "Please enter a business question.",
        }

    start_time = time.perf_counter()

    try:
        from ai_business_analytics.ai.llm import create_plan
        from ai_business_analytics.ai.planner import execute_plan

        plan = create_plan(question.strip())

        result = execute_plan(plan)

        elapsed_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        result["response_time_ms"] = elapsed_ms
        result["question"] = question.strip()

        return result

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "AI Business Analytics Ask Question Error",
        )

        elapsed_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        return {
            "status": "error",
            "message": (
                "Unable to process the question. "
                "Please try a supported business analytics question."
            ),
            "response_time_ms": elapsed_ms,
        }
