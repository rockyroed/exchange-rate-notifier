import plotly.graph_objs as go

from actions.email.send import daily
from database.rates import get_rates


def main():
    rates = get_rates()
    x = [row["created_at"] for row in rates]
    y = [row["rate"] for row in rates]

    fig = go.Figure(data=go.Scatter(x=x, y=y, mode="lines+markers"))
    fig.update_layout(
        title="Exchange Rate Over Time",
        xaxis_title="Date/Time",
        yaxis_title="Rate",
        xaxis_tickangle=-45,
        width=1400,  # Increase width for better spacing
        height=600,
    )

    daily(rates, fig)


if __name__ == "__main__":
    main()
