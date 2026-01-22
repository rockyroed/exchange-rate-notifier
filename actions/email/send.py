import os
import tempfile

import yagmail


def hourly(conversion_rate, direction, mean, std_dev, deviation, percentage_change):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    if not SENDER_EMAIL:
        raise ValueError("Sender email is not set in the environment variables.")

    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    if not SENDER_PASSWORD:
        raise ValueError("Email password is not set in the environment variables.")

    RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS").split(",")
    if not RECIPIENT_EMAILS:
        raise ValueError("Recipient emails are not set in the environment variables.")

    subject = f"Exchange Rate Alert: Significant {direction.capitalize()} Detected"

    direction_emoji = "📈" if direction == "spike" else "📉"
    change_sign = "+" if percentage_change > 0 else ""

    body = (
        f"{direction_emoji} <b>Significant {direction.capitalize()} Detected!</b><br><br>"
        f"Current Rate: <b>₱{conversion_rate:.2f}</b><br>"
        f"Recent Average (6 hours): ₱{mean:.2f}<br>"
        f"Standard Deviation: ₱{std_dev:.2f}<br><br>"
        f"Deviation: <b>{abs(deviation):.2f}σ</b> from mean<br>"
        f"Percentage Change: <b>{change_sign}{percentage_change:.2f}%</b> from recent average"
    )

    yag = yagmail.SMTP(
        user=SENDER_EMAIL,
        password=SENDER_PASSWORD,
    )
    yag.send(
        to=RECIPIENT_EMAILS,
        subject=subject,
        contents=body,
    )

    return True


def daily(rates, fig):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    if not SENDER_EMAIL:
        raise ValueError("Sender email is not set in the environment variables.")

    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    if not SENDER_PASSWORD:
        raise ValueError("Email password is not set in the environment variables.")

    RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS").split(",")
    if not RECIPIENT_EMAILS:
        raise ValueError("Recipient emails are not set in the environment variables.")

    # Calculate average rate
    if not rates:
        avg_rate = 0
    else:
        avg_rate = sum([row["rate"] for row in rates]) / len(rates)

    subject = "Daily Exchange Rate Report"

    # Save the figure to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        fig.write_image(tmpfile.name)
        image_path = tmpfile.name

    import yagmail

    body = [
        f"<p>Here is the daily exchange rate graph."
        f"<br>Latest rate: ₱{rates[-1]['rate']:.2f}"
        f"<br>Average rate: ₱{avg_rate:.2f}</p>",
        yagmail.inline(image_path),
    ]

    yag = yagmail.SMTP(
        user=SENDER_EMAIL,
        password=SENDER_PASSWORD,
    )
    yag.send(
        to=RECIPIENT_EMAILS,
        subject=subject,
        contents=body,
    )

    # Optionally, remove the temp file after sending (not strictly necessary)
    try:
        os.remove(image_path)
    except Exception:
        pass

    return True


if __name__ == "__main__":
    # Example usage
    conversion_rate = "50.00"  # This would be dynamically fetched in a real scenario
    res = hourly(conversion_rate)

    if res:
        print("Email notification sent successfully.")
