from actions.email.send import send_email
from actions.exchange_rate.check import check
from actions.exchange_rate.get import get
from constants import CURRENCY, LOWER_THRESHOLD, UPPER_THRESHOLD


def main():
    rates = get(CURRENCY)
    status = check(
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
    if send_email(conversion_rate=rates[CURRENCY], status=status, threshold=threshold):
        print("Email notification sent successfully.")


if __name__ == "__main__":
    main()
