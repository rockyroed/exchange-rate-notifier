import requests
import os

def get_exchange_rate(currency="PHP"):
    APP_ID = os.getenv('OPEN_EXCHANGE_RATES_APP_ID')
    APP_BACKUP_ID = os.getenv('OPEN_EXCHANGE_RATES_APP_BACKUP_ID')

    response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id={APP_ID}&symbols={currency}")
    if response.status_code == 200:
        data = response.json()
        return data.get("rates", {})
    elif APP_BACKUP_ID:
        response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id={APP_BACKUP_ID}&symbols={currency}")
        if response.status_code == 200:
            data = response.json()
            return data.get("rates", {})
    
    raise Exception(f"Failed to fetch exchange rates: {response.status_code}")