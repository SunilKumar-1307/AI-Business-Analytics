import json
import re

from openai import OpenAI


# ============================================================
# ALLOWED ANALYTICS OPERATIONS
# ============================================================

ALLOWED_QUERY_TYPES = {
    "sales_by_year",
    "sales_by_city",
    "production_status",
    "revenue_by_category",
    "paid_not_started",
    "customers_recent_purchases",
}


# ============================================================
# OLLAMA CLIENT
# ============================================================

def get_client():
    return OpenAI(
        base_url="http://host.docker.internal:11434/v1",
        api_key="ollama",
    )


# ============================================================
# YEAR EXTRACTION
# ============================================================

def extract_year(question):
    match = re.search(r"\b(20\d{2})\b", question)

    if match:
        year = int(match.group(1))

        if 2021 <= year <= 2026:
            return year

    return None


def make_date_range(year):
    if not year:
        return None, None

    return (
        f"{year}-01-01",
        f"{year}-12-31",
    )


# ============================================================
# RELATIVE DATE EXTRACTION
# ============================================================

def extract_days(question):
    text = question.lower()

    # Example:
    # last 30 days
    # past 30 days
    match = re.search(
        r"(?:last|past|previous)\s+(\d+)\s+days?",
        text,
    )

    if match:
        return int(match.group(1))

    # Example:
    # last 3 months
    # previous 3 months
    match = re.search(
        r"(?:last|past|previous)\s+(\d+)\s+months?",
        text,
    )

    if match:
        return int(match.group(1)) * 30

    # One month
    if any(
        phrase in text
        for phrase in [
            "last month",
            "last one month",
            "past month",
            "previous month",
            "previous one month",
        ]
    ):
        return 30

    # One week
    if any(
        phrase in text
        for phrase in [
            "last week",
            "past week",
            "previous week",
        ]
    ):
        return 7

    return None


# ============================================================
# FAST CLASSIFIER
# ============================================================

def fast_classify(question):
    """
    Handles obvious questions quickly.

    Complex or unusual wording is passed to Ollama.
    """

    text = question.lower().strip()

    compact = re.sub(
        r"[^a-z0-9]+",
        " ",
        text,
    )

    year = extract_year(text)

    start_date, end_date = make_date_range(year)

    # --------------------------------------------------------
    # RECENT CUSTOMER PURCHASES
    # --------------------------------------------------------

    customer_words = [
        "customer",
        "customers",
        "buyer",
        "buyers",
    ]

    purchase_words = [
        "purchase",
        "purchases",
        "purchased",
        "bought",
        "order",
        "orders",
        "ordered",
    ]

    recent_words = [
        "last month",
        "last one month",
        "past month",
        "previous month",
        "last week",
        "past week",
        "last 30 days",
        "past 30 days",
        "recent purchase",
        "recent purchases",
        "recently purchased",
    ]

    has_customer = any(
        word in compact
        for word in customer_words
    )

    has_purchase = any(
        word in compact
        for word in purchase_words
    )

    has_recent = any(
        phrase in text
        for phrase in recent_words
    )

    if has_customer and has_purchase and has_recent:

        days = extract_days(text)

        if days is None:
            days = 30

        days = max(1, min(days, 3650))

        return {
            "query_type": "customers_recent_purchases",
            "start_date": None,
            "end_date": None,
            "days": days,
        }

    # --------------------------------------------------------
    # SALES BY CITY
    # --------------------------------------------------------

    if (
        ("sales" in compact or "revenue" in compact)
        and "city" in compact
    ):
        return {
            "query_type": "sales_by_city",
            "start_date": start_date,
            "end_date": end_date,
            "days": None,
        }

    # --------------------------------------------------------
    # REVENUE BY CATEGORY
    # --------------------------------------------------------

    if (
        ("revenue" in compact or "sales" in compact)
        and (
            "category" in compact
            or "categories" in compact
            or "product category" in compact
            or "product categories" in compact
        )
    ):
        return {
            "query_type": "revenue_by_category",
            "start_date": start_date,
            "end_date": end_date,
            "days": None,
        }

    # --------------------------------------------------------
    # SALES BY YEAR
    # --------------------------------------------------------

    if (
        "sales" in compact
        and (
            "year" in compact
            or "yearly" in compact
            or "annual" in compact
        )
    ):
        return {
            "query_type": "sales_by_year",
            "start_date": None,
            "end_date": None,
            "days": None,
        }

    # --------------------------------------------------------
    # PRODUCTION STATUS
    # --------------------------------------------------------

    if (
        "production" in compact
        and (
            "status" in compact
            or "pipeline" in compact
            or "workload" in compact
        )
    ):
        return {
            "query_type": "production_status",
            "start_date": None,
            "end_date": None,
            "days": None,
        }

    # --------------------------------------------------------
    # PAID BUT PRODUCTION NOT STARTED
    # --------------------------------------------------------

    if (
        ("paid" in compact or "payment" in compact)
        and "production" in compact
        and (
            "not started" in compact
            or "not begun" in compact
            or "waiting" in compact
        )
    ):
        return {
            "query_type": "paid_not_started",
            "start_date": None,
            "end_date": None,
            "days": None,
        }

    # Anything else goes to the LLM.

    return None


# ============================================================
# LLM CLASSIFIER
# ============================================================

def llm_classify(question):

    client = get_client()

    system_prompt = """
You are the natural-language business analytics planner
for a Frappe business analytics application.

Your job is to understand the user's business question
and map it to ONE of the supported analytics operations.

You MUST NOT generate SQL.

You MUST NOT invent a new query type.

You MUST return ONLY valid JSON.

SUPPORTED OPERATIONS
====================

1. sales_by_year

Use this when the user wants sales/revenue
broken down by year.

Examples:

"What were the sales for each year?"

"Show me our annual sales."

"How did sales change from year to year?"

"I want yearly sales performance."

"Give me the sales history across the available years."

"Looking across the available years, how did our
overall sales change from one year to another?"

Return:

{
    "query_type": "sales_by_year",
    "start_date": null,
    "end_date": null,
    "days": null
}


2. sales_by_city

Use this when the user wants sales/revenue
broken down by city.

Examples:

"Show sales by city for 2025."

"Which cities generated sales in 2025?"

"Where did our sales come from geographically?"

"Show me the revenue for each location."

"Can you tell me which cities contributed to our
sales during 2025?"

"If I wanted to know where our sales came from
geographically in 2025, what would the numbers
look like for each city?"

If a year is specified:

2025 -> start_date = "2025-01-01"
2025 -> end_date = "2025-12-31"

Return:

{
    "query_type": "sales_by_city",
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "days": null
}


3. revenue_by_category

Use this when the user wants revenue/sales
broken down by product category.

Examples:

"Show revenue by product category for 2025."

"What are the sales for each product category?"

"Show category-wise revenue."

"How much revenue did each type of product generate?"

"I want to understand the composition of our 2025
income according to the different kinds of products
we sell."

"Show the revenue contribution of every product
category for 2025."

If a year is specified, convert it into start_date
and end_date.

Return:

{
    "query_type": "revenue_by_category",
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "days": null
}


4. production_status

Use this when the user wants to understand
the production/manufacturing status.

Examples:

"Show me production status."

"How many orders are finished?"

"How many are still in progress?"

"How many have not started?"

"Give me a breakdown of production."

"Can you summarize our production workload
by its current status?"

"Give me a breakdown of the current manufacturing
pipeline."

Return:

{
    "query_type": "production_status",
    "start_date": null,
    "end_date": null,
    "days": null
}


5. paid_not_started

Use this when payment is completed/paid
but production has not started.

Examples:

"Which customers have paid but production
has not started?"

"Show paid orders where production has
not started."

"Give me customers whose payment is paid
but production is not started."

"Which customers have completed a financial
transaction with us while their manufacturing
request remains untouched?"

"For orders where the customer has already paid,
which ones are still waiting for production to begin?"

Return:

{
    "query_type": "paid_not_started",
    "start_date": null,
    "end_date": null,
    "days": null
}


6. customers_recent_purchases

Use this when the user wants customer details
for customers who purchased recently.

Examples:

"Which customers purchased last month?"

"Give me customer details who purchased
in the last 30 days."

"Who bought something recently?"

"Which customers made purchases in the
last 3 months?"

"Give me the people who placed orders recently."

"Show customers who recently did business with us."

"I want the customers who purchased during
the previous month."

"Give me a customer-level view of buyers who
placed an order within the past 90 days."

For relative periods:

last month = 30 days

last one month = 30 days

last week = 7 days

last 7 days = 7 days

last 30 days = 30 days

last 3 months = 90 days

last 6 months = 180 days

If the user gives a number of months,
multiply it by 30.

Return:

{
    "query_type": "customers_recent_purchases",
    "start_date": null,
    "end_date": null,
    "days": 90
}


IMPORTANT RULES
===============

- Never generate SQL.
- Never return SQL.
- Never invent database fields.
- Never invent tables.
- Never invent query types.
- Only use the six supported query types.
- If the question cannot be answered by one of
  the six operations, return "unsupported".
- If a year is explicitly given, use that year.
- Do not confuse a city with a product category.
- Do not confuse production status with payment status.
- Do not confuse paid orders with delivered orders.

For unsupported questions return:

{
    "query_type": "unsupported",
    "start_date": null,
    "end_date": null,
    "days": null
}
"""

    response = client.chat.completions.create(
        model="qwen2.5:1.5b",
        temperature=0,
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    plan = json.loads(
        response.choices[0].message.content
    )

    query_type = plan.get("query_type")

    if query_type not in ALLOWED_QUERY_TYPES:
        return {
            "query_type": "unsupported",
            "start_date": None,
            "end_date": None,
            "days": None,
        }

    days = plan.get("days")

    if query_type == "customers_recent_purchases":

        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 30

        days = max(1, min(days, 3650))

    else:
        days = None

    return {
        "query_type": query_type,
        "start_date": plan.get("start_date"),
        "end_date": plan.get("end_date"),
        "days": days,
    }


# ============================================================
# MAIN PLANNER
# ============================================================

def create_plan(question):

    if not question or not question.strip():

        return {
            "query_type": "unsupported",
            "start_date": None,
            "end_date": None,
            "days": None,
        }

    question = question.strip()

    # Try fast classification first.
    fast_plan = fast_classify(question)

    if fast_plan:
        return fast_plan

    # Complex/unusual wording goes to Ollama.
    return llm_classify(question)
