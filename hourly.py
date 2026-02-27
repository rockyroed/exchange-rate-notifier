from actions.email.send import hourly
from actions.exchange_rate.check import check_sudden_change
from actions.exchange_rate.get import get
from constants import CURRENCY
from database.rates import get_rates


def main():
    # Get current rate (this also saves it to the database)
    current_rate = get(CURRENCY)

    # Get last 7 rates (to exclude the current one we just added)
    # The most recent rate will be the one we just added, so we exclude it
    all_recent_rates = get_rates(rows=7)

    if not all_recent_rates or len(all_recent_rates) < 3:
        message = f"The current exchange rate is ₱{current_rate}. Not enough historical data to detect sudden changes."
        print(message)
        return

    # Exclude the most recent rate (the one we just added) and use the previous 6
    # get_rates orders by created_at ASC, so the most recent is at the end
    historical_rates = all_recent_rates[:-1]  # Exclude the last (most recent) rate

    # Check for sudden change using standard deviation
    change_result = check_sudden_change(current_rate, historical_rates, std_deviation_threshold=3.0)

    if change_result is None:
        message = f"The current exchange rate is ₱{current_rate}. Not enough historical data to detect sudden changes."
        print(message)
        return

    if not change_result["is_outlier"]:
        message = (
            f"The current exchange rate is ₱{current_rate}. "
            f"No significant change detected (mean: ₱{change_result['mean']:.2f}, "
            f"deviation: {change_result['deviation']:.2f}σ)."
        )
        print(message)
        return

    # Significant change detected - send notification
    direction = change_result["direction"]
    mean = change_result["mean"]
    std_dev = change_result["std_dev"]
    deviation = change_result["deviation"]
    percentage_change = change_result["percentage_change"]

    message = (
        f"The current exchange rate is ₱{current_rate}. "
        f"Significant {direction} detected! "
        f"({abs(deviation):.2f}σ from mean of ₱{mean:.2f}, "
        f"{abs(percentage_change):.2f}% change). Sending notification..."
    )
    print(message)

    if hourly(
        conversion_rate=current_rate,
        direction=direction,
        mean=mean,
        std_dev=std_dev,
        deviation=deviation,
        percentage_change=percentage_change,
    ):
        print("Email notification sent successfully.")


if __name__ == "__main__":
    main()
