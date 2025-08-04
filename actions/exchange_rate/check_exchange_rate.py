def check_exchange_rate(rates, currency, threshold=57.8):
    if rates.get(currency, 0) > threshold:
        return True
    return False