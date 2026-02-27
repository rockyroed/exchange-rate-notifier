import statistics


def check_sudden_change(current_rate, historical_rates, std_deviation_threshold=3.0):
    """
    Check if the current rate is a significant outlier compared to historical rates.

    Args:
        current_rate: The current exchange rate (float)
        historical_rates: List of historical rate dictionaries with 'rate' key
        std_deviation_threshold: Number of standard deviations to consider an outlier (default: 3.0)

    Returns:
        dict with 'is_outlier' (bool), 'direction' ('spike' or 'drop'), 'mean' (float),
        'std_dev' (float), 'deviation' (float), 'percentage_change' (float)
        or None if not enough historical data
    """
    if not historical_rates or len(historical_rates) < 2:
        return None

    # Extract rates as floats
    rates = [float(rate_dict["rate"]) for rate_dict in historical_rates]

    # Calculate mean and standard deviation
    mean = statistics.mean(rates)
    std_dev = statistics.stdev(rates) if len(rates) > 1 else 0

    # If standard deviation is 0 (all rates are the same), we can't detect outliers
    if std_dev == 0:
        return None

    # Calculate how many standard deviations the current rate is from the mean
    deviation = (current_rate - mean) / std_dev

    # Check if it's an outlier (beyond threshold in either direction)
    is_outlier = abs(deviation) >= std_deviation_threshold

    if not is_outlier:
        return {
            "is_outlier": False,
            "mean": mean,
            "std_dev": std_dev,
            "deviation": deviation,
            "percentage_change": ((current_rate - mean) / mean) * 100,
        }

    # Determine direction
    direction = "spike" if deviation > 0 else "drop"

    # Calculate percentage change from mean
    percentage_change = ((current_rate - mean) / mean) * 100

    return {
        "is_outlier": True,
        "direction": direction,
        "mean": mean,
        "std_dev": std_dev,
        "deviation": deviation,
        "percentage_change": percentage_change,
    }


def check(
    rate,
    upper_threshold=57.8,
    lower_threshold=55.5,
):
    if rate > upper_threshold:
        return "above"
    if rate < lower_threshold:
        return "below"
    return False
