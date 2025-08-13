import os

import requests

from actions.exchange_rate.post import post


def get(
    currency="PHP",
):
    APP_ID = os.getenv("OPEN_EXCHANGE_RATES_APP_ID")
    APP_BACKUP_ID = os.getenv("OPEN_EXCHANGE_RATES_APP_BACKUP_ID")

    response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id={APP_ID}&symbols={currency}")
    if response.status_code == 200:
        data = response.json()
        rates = data.get("rates", {})

        if not rates:
            raise Exception("No rates found in the response.")

        rate = round(rates.get(currency), 2)

        # Post rate to database
        post(rate)

        return rate
    elif APP_BACKUP_ID:
        response = requests.get(
            f"https://openexchangerates.org/api/latest.json?app_id={APP_BACKUP_ID}&symbols={currency}"
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("rates", {})

    raise Exception(f"Failed to fetch exchange rates: {response.status_code}")
