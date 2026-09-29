import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", GMAIL_ADDRESS)


def send_order_confirmation_email(order) -> None:
    """
    Sends a plain-text order confirmation email.
    Fails silently (just prints a warning) rather than raising — a broken
    email should never stop an order from being saved.
    """
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("Email not sent: GMAIL_ADDRESS/GMAIL_APP_PASSWORD not set in .env")
        return

    lines = [f"{item['name']} x{item['quantity']} — ${item['price'] * item['quantity']:.2f}"
             for item in order.items]
    items_text = "\n".join(lines)

    payment_label = "Cash on Delivery" if order.payment_method == "cod" else "Card"

    body = f"""Hi {order.customer_name},

Thank you for your order from Aurelis. Here's your confirmation:

Order #{order.id}

{items_text}

Total: ${order.total:.2f}
Payment method: {payment_label}
Shipping to: {order.shipping_address}, {order.city}

We'll be in touch as soon as your order ships.

Warmly,
Aurelis
"""

    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = order.customer_email
    msg["Subject"] = f"Your Aurelis order #{order.id} is confirmed"
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, order.customer_email, msg.as_string())
        print(f"Order confirmation email sent to {order.customer_email}")
    except Exception as e:
        print(f"Failed to send order confirmation email: {e}")

def send_stock_alert_email(email: str, product) -> None:
    """
    Notifies one customer that a product they asked about is back in stock.
    Fails silently — a broken email should never break the restock flow.
    """
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("Email not sent: GMAIL_ADDRESS/GMAIL_APP_PASSWORD not set in .env")
        return

    body = f"""Hi,

Good news — "{product.name}" is back in stock at Aurelis.

${product.price:.2f} · {product.metal_type or ""}

It won't stay in stock for long, so shop now if you'd still like it.

Warmly,
Aurelis
"""

    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = email
    msg["Subject"] = f'"{product.name}" is back in stock'
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, email, msg.as_string())
        print(f"Stock alert email sent to {email}")
    except Exception as e:
        print(f"Failed to send stock alert email: {e}")

def send_admin_out_of_stock_email(product) -> None:
    """
    Notifies the store admin that a product just sold out.
    Fails silently — a broken email should never break the checkout flow.
    """
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD or not ADMIN_EMAIL:
        print("Admin alert not sent: email credentials not fully set in .env")
        return

    body = f"""Heads up — "{product.name}" just sold out.

Product ID: {product.id}
Category: {product.category}

Restock it from the admin dashboard, or run:
python restock.py {product.id} <quantity>

This will also notify anyone who signed up for a "back in stock" alert.
"""

    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = f'"{product.name}" is now out of stock'
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, ADMIN_EMAIL, msg.as_string())
        print(f"Admin out-of-stock alert sent for '{product.name}'")
    except Exception as e:
        print(f"Failed to send admin out-of-stock alert: {e}")