def check_exchange_rate(
    rates,
    currency,
    upper_threshold=57.8,
    lower_threshold=55.5,
):
    if rates.get(currency, 0) > upper_threshold:
        return "above"
    if rates.get(currency, 0) < lower_threshold:
        return "below"
    return False
