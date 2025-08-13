from actions.email_notify.notify import send_email_notification
from actions.exchange_rate.check_exchange_rate import check_exchange_rate
from actions.exchange_rate.get_exchange_rate import get_exchange_rate
from constants import CURRENCY, LOWER_THRESHOLD, UPPER_THRESHOLD


def main():
    rates = get_exchange_rate(CURRENCY)
    status = check_exchange_rate(
        rates,
        currency=CURRENCY,
        upper_threshold=UPPER_THRESHOLD,
        lower_threshold=LOWER_THRESHOLD,
    )

    message = f"The current exchange rate is ₱{rates[CURRENCY]}."

    if not status:
        message += f" It is within the thresholds ₱{LOWER_THRESHOLD} and ₱{UPPER_THRESHOLD}."
        " No notification will be sent."
        print(message)
        return

    if status == "above":
        message += f" It is above the threshold (₱{UPPER_THRESHOLD}). Sending notification..."
        threshold = UPPER_THRESHOLD
    elif status == "below":
        message += f" It is below the threshold (₱{LOWER_THRESHOLD}). Sending notification..."
        threshold = LOWER_THRESHOLD

    print(message)
    if send_email_notification(conversion_rate=rates[CURRENCY], status=status, threshold=threshold):
        print("Email notification sent successfully.")


if __name__ == "__main__":
    main()
