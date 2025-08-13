import os

import yagmail


def send_email(conversion_rate, status, threshold):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    if not SENDER_EMAIL:
        raise ValueError("Sender email is not set in the environment variables.")

    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    if not SENDER_PASSWORD:
        raise ValueError("Email password is not set in the environment variables.")

    RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS").split(",")
    if not RECIPIENT_EMAILS:
        raise ValueError("Recipient emails are not set in the environment variables.")

    subject = f"Exchange Rate Notification: {conversion_rate}"
    body = f"The current exchange rate is ₱{conversion_rate}. It is {status} the threshold (₱{threshold})."

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


if __name__ == "__main__":
    # Example usage
    conversion_rate = "50.00"  # This would be dynamically fetched in a real scenario
    res = send_email(conversion_rate)

    if res:
        print("Email notification sent successfully.")
