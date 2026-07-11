import plotly.graph_objs as go

FONT_FAMILY = "Ubuntu, Helvetica, Arial, sans-serif"
INK = "#000000"
MUTED = "#606060"
GRID = "#f0f0f0"
SURFACE = "#f9f9f9"


def create_graph(x, y):
    fig = go.Figure(
        data=go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            line=dict(color=INK, width=2),
            marker=dict(color=INK, size=6),
            hovertemplate="%{x}<br>₱%{y:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(
            text="Exchange Rate Over Time",
            font=dict(family=FONT_FAMILY, size=20, color=INK),
            x=0.5,
            xanchor="center",
        ),
        font=dict(family=FONT_FAMILY, color=MUTED, size=13),
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        xaxis=dict(
            title=dict(text="Date/Time", font=dict(color=MUTED)),
            tickangle=-45,
            showgrid=False,
            linecolor=GRID,
            tickfont=dict(color=MUTED),
        ),
        yaxis=dict(
            title=dict(text="Rate", font=dict(color=MUTED)),
            showgrid=True,
            gridcolor=GRID,
            zeroline=False,
            linecolor=GRID,
            tickfont=dict(color=MUTED),
        ),
        margin=dict(l=60, r=30, t=60, b=80),
        width=700,
        height=350,
    )

    return fig
