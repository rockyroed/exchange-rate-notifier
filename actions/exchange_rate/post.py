from database.rates import post_rate


def post(rate):
    res = post_rate(rate)

    return res
