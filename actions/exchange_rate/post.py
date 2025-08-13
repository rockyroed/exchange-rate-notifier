from database.rates import post_rate


def post(
    rates,
    currency="PHP",
):
    res = post_rate(rates[currency])

    return res
