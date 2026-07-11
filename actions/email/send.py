import base64
import os
from datetime import date, timedelta
from string import Template

import yagmail

DAILY_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "daily_template.html")
HOURLY_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "hourly_template.html")


def hourly(conversion_rate, direction, mean, std_dev, deviation, percentage_change):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    if not SENDER_EMAIL:
        raise ValueError("Sender email is not set in the environment variables.")

    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    if not SENDER_PASSWORD:
        raise ValueError("Email password is not set in the environment variables.")

    RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS")
    if not RECIPIENT_EMAILS:
        raise ValueError("Recipient emails are not set in the environment variables.")

    RECIPIENT_EMAILS_ARRAY = RECIPIENT_EMAILS.split(",")

    subject = f"Exchange Rate Alert: Significant {direction.capitalize()} Detected"

    direction_emoji = "📈" if direction == "spike" else "📉"
    change_sign = "+" if percentage_change > 0 else ""

    with open(HOURLY_TEMPLATE_PATH, encoding="utf-8") as f:
        template = Template(f.read())

    body = template.substitute(
        direction_emoji=direction_emoji,
        direction=direction.capitalize(),
        current_rate=f"₱{conversion_rate:.2f}",
        recent_average=f"₱{mean:.2f}",
        percentage_change=f"{change_sign}{percentage_change:.2f}%",
    ).replace("\n", " ")

    yag = yagmail.SMTP(
        user=SENDER_EMAIL,
        password=SENDER_PASSWORD,
    )
    yag.send(
        to=RECIPIENT_EMAILS_ARRAY,
        subject=subject,
        contents=body,
    )

    return True


def daily(rates, fig, previous_average=None):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    if not SENDER_EMAIL:
        raise ValueError("Sender email is not set in the environment variables.")

    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    if not SENDER_PASSWORD:
        raise ValueError("Email password is not set in the environment variables.")

    RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS")
    if not RECIPIENT_EMAILS:
        raise ValueError("Recipient emails are not set in the environment variables.")

    RECIPIENT_EMAILS_ARRAY = RECIPIENT_EMAILS.split(",")

    # Calculate average rate
    if not rates:
        avg_rate = 0
    else:
        avg_rate = sum([row["rate"] for row in rates]) / len(rates)

    latest_rate = rates[-1]["rate"] if rates else 0

    today = date.today()
    subject = "Daily Exchange Rate Report for " + today.strftime("%B %d, %Y")

    # Date range: the day before through the current date
    yesterday = today - timedelta(days=1)
    if today.month == yesterday.month:
        date_range = f"{today.strftime('%B')} {yesterday.day}-{today.day}, {today.year}"
    else:
        date_range = f"{yesterday.strftime('%B %d')} - {today.strftime('%B %d, %Y')}"

    # Embed the graph directly in the HTML as a base64 data URI
    img_bytes = fig.to_image(format="png")
    img_b64 = base64.b64encode(img_bytes).decode("ascii")
    graph_img = (
        f'<img src="data:image/png;base64,{img_b64}" alt="Exchange rate graph" align="center" '
        f'style="max-width:100%;height:auto;display:block;margin-left:auto;margin-right:auto;border-radius:8px;" />'
    )

    with open(DAILY_TEMPLATE_PATH, encoding="utf-8") as f:
        template = Template(f.read())

    body = template.substitute(
        date_range=date_range,
        average_rate=f"₱{avg_rate:.2f}",
        latest_rate=f"₱{latest_rate:.2f}",
        previous_average=f"₱{previous_average:.2f}",
        graph_img=graph_img,
    ).replace("\n", " ")

    yag = yagmail.SMTP(
        user=SENDER_EMAIL,
        password=SENDER_PASSWORD,
    )
    yag.send(
        to=RECIPIENT_EMAILS_ARRAY,
        subject=subject,
        contents=body,
    )

    return True


if __name__ == "__main__":
    # Example usage
    conversion_rate = 50.00  # This would be dynamically fetched in a real scenario
    res = hourly(conversion_rate, "spike", 49.50, 0.25, 2.0, 1.0)

    if res:
        print("Email notification sent successfully.")
