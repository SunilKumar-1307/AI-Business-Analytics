import frappe
import random
from datetime import date, timedelta

START_DATE = date(2021, 4, 1)
END_DATE = date(2026, 3, 31)

NUM_CUSTOMERS = 10_000
NUM_PRODUCTS = 1_000
NUM_ORDERS = 100_000

random.seed(42)

CITIES = [
    ("Chennai", "Tamil Nadu"),
    ("Bengaluru", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Delhi", "Delhi"),
    ("Kolkata", "West Bengal"),
    ("Ahmedabad", "Gujarat"),
    ("Coimbatore", "Tamil Nadu"),
    ("Madurai", "Tamil Nadu"),
]

CUSTOMER_TYPES = ["Individual", "Company"]

PRODUCT_CATEGORIES = [
    "Electronics",
    "Machinery",
    "Automotive",
    "Industrial",
    "Electrical",
    "Hardware",
    "Office Equipment",
    "Consumer Goods",
]

ORDER_STATUSES = [
    "Pending",
    "Confirmed",
    "Cancelled",
    "Completed",
]

PAYMENT_STATUSES = [
    "Paid",
    "Pending",
    "Failed",
]

PRODUCTION_STATUSES = [
    "Not Started",
    "In Progress",
    "Finished",
]

DELIVERY_STATUSES = [
    "Not Delivered",
    "In Transit",
    "Delivered",
]


def random_date(start_date, end_date):
    days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days))


def random_amount(minimum, maximum):
    return round(random.uniform(minimum, maximum), 2)


def insert_data(doctype, fields, rows):
    if rows:
        frappe.db.bulk_insert(
            doctype,
            fields,
            rows,
            ignore_duplicates=True,
            chunk_size=1000,
        )


def create_customers():
    print(f"Creating {NUM_CUSTOMERS:,} customers...")

    fields = [
        "name",
        "customer_name",
        "email",
        "city",
        "state",
        "country",
        "customer_type",
    ]

    rows = []

    for i in range(1, NUM_CUSTOMERS + 1):
        city, state = random.choice(CITIES)

        rows.append((
            f"CUST-{i:06d}",
            f"Customer {i:06d}",
            f"customer{i:06d}@example.com",
            city,
            state,
            "India",
            random.choice(CUSTOMER_TYPES),
        ))

    insert_data("BA Customer", fields, rows)
    frappe.db.commit()

    print("Customers created.")


def create_products():
    print(f"Creating {NUM_PRODUCTS:,} products...")

    fields = [
        "name",
        "product_name",
        "category",
        "unit_price",
        "cost_price",
    ]

    rows = []

    for i in range(1, NUM_PRODUCTS + 1):
        cost = random_amount(100, 50_000)
        selling_price = round(cost * random.uniform(1.10, 1.50), 2)

        rows.append((
            f"PROD-{i:05d}",
            f"Product {i:05d}",
            random.choice(PRODUCT_CATEGORIES),
            selling_price,
            cost,
        ))

    insert_data("BA Product", fields, rows)
    frappe.db.commit()

    print("Products created.")


def create_orders():
    print(f"Creating {NUM_ORDERS:,} orders...")

    order_fields = [
        "name",
        "customer",
        "order_date",
        "city",
        "total_amount",
        "order_status",
    ]

    item_fields = [
        "name",
        "order",
        "product",
        "quantity",
        "rate",
        "amount",
    ]

    payment_fields = [
        "name",
        "order",
        "payment_date",
        "amount",
        "payment_status",
    ]

    production_fields = [
        "name",
        "order",
        "production_date",
        "production_status",
    ]

    delivery_fields = [
        "name",
        "order",
        "delivery_date",
        "delivery_status",
    ]

    orders = []
    order_items = []
    payments = []
    productions = []
    deliveries = []

    for i in range(1, NUM_ORDERS + 1):

        order_name = f"ORD-{i:07d}"
        customer_id = random.randint(1, NUM_CUSTOMERS)
        city, state = random.choice(CITIES)
        order_date = random_date(START_DATE, END_DATE)
        order_status = random.choice(ORDER_STATUSES)

        total_amount = 0

        number_of_items = random.randint(1, 5)

        selected_products = random.sample(
            range(1, NUM_PRODUCTS + 1),
            number_of_items,
        )

        for product_number in selected_products:

            quantity = random.randint(1, 10)
            rate = random_amount(500, 50_000)
            amount = round(quantity * rate, 2)

            total_amount += amount

            order_items.append((
                f"ORDITEM-{i:07d}-{product_number:05d}",
                order_name,
                f"PROD-{product_number:05d}",
                quantity,
                rate,
                amount,
            ))

        total_amount = round(total_amount, 2)

        orders.append((
            order_name,
            f"CUST-{customer_id:06d}",
            order_date,
            city,
            total_amount,
            order_status,
        ))

        payment_status = random.choices(
            PAYMENT_STATUSES,
            weights=[70, 20, 10],
            k=1,
        )[0]

        payments.append((
            f"PAY-{i:07d}",
            order_name,
            order_date,
            total_amount,
            payment_status,
        ))

        production_status = random.choices(
            PRODUCTION_STATUSES,
            weights=[15, 25, 60],
            k=1,
        )[0]

        productions.append((
            f"PRODUCTION-{i:07d}",
            order_name,
            order_date,
            production_status,
        ))

        delivery_status = random.choices(
            DELIVERY_STATUSES,
            weights=[20, 20, 60],
            k=1,
        )[0]

        deliveries.append((
            f"DEL-{i:07d}",
            order_name,
            order_date,
            delivery_status,
        ))

        if i % 5_000 == 0 or i == NUM_ORDERS:

            insert_data("BA Order", order_fields, orders)
            insert_data("BA Order Item", item_fields, order_items)
            insert_data("BA Payment", payment_fields, payments)
            insert_data("BA Production", production_fields, productions)
            insert_data("BA Delivery", delivery_fields, deliveries)

            frappe.db.commit()

            orders.clear()
            order_items.clear()
            payments.clear()
            productions.clear()
            deliveries.clear()

            print(f"Inserted {i:,} orders...")


def main():
    print("=" * 60)
    print("AI BUSINESS ANALYTICS - SYNTHETIC DATA GENERATOR")
    print("=" * 60)

    print(f"Date range : {START_DATE} -> {END_DATE}")
    print(f"Customers  : {NUM_CUSTOMERS:,}")
    print(f"Products   : {NUM_PRODUCTS:,}")
    print(f"Orders     : {NUM_ORDERS:,}")

    create_customers()
    create_products()
    create_orders()

    print("=" * 60)
    print("DATA GENERATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
