from actions.email.send import daily
from database.rates import get_previous_average, get_rates
from utils.graph import create_graph


def main():
    rates = get_rates(daily=True)
    if not rates:
        print("No rates found.")
        return
    x = [row["created_at"] for row in rates]
    y = [row["rate"] for row in rates]

    fig = create_graph(x, y)

    previous_average = get_previous_average()

    daily(rates, fig, previous_average)


if __name__ == "__main__":
    main()
