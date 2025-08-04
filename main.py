from dotenv import load_dotenv

from actions.email_notify.notify import send_email_notification
from actions.exchange_rate.check_exchange_rate import check_exchange_rate
from actions.exchange_rate.get_exchange_rate import get_exchange_rate


def main():
    load_dotenv()
    CURRENCY = "PHP"
    THRESHOLD = 57.8

    rates = get_exchange_rate(CURRENCY)
    is_above_threshold = check_exchange_rate(
        rates,
        CURRENCY,
        THRESHOLD,
    )

    if is_above_threshold:
        print(
            f"The current exchange rate is ₱{rates[CURRENCY]}. It is above the threshold ₱{THRESHOLD}."
        )
        print("Sending notification...")
        res = send_email_notification(rates[CURRENCY])

        if res:
            print("Email notification sent successfully.")
    else:
        print(
            f"The current exchange rate is ₱{rates[CURRENCY]}. It is below the threshold ₱{THRESHOLD}."
        )
        print("No notification sent.")


if __name__ == "__main__":
    main()
