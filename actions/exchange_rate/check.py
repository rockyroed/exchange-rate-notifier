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
