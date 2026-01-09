"""Chart builder functions for Plotly visualizations."""
from typing import Any, Dict, List

import plotly.graph_objects as go

from app.services.chart_styles import (
    COLORS,
    NEGATIVE_COLOR,
    auto_currency_tickformat,
    axis_style,
    base_layout,
)


def create_category_chart(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a bar chart for sales by category."""
    categories = [d["category"] for d in data]
    sales = [d["sales"] for d in data]
    profit = [d["profit"] for d in data]
    y_fmt = auto_currency_tickformat([*sales, *profit])

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Sales",
        x=categories,
        y=sales,
        marker_color=COLORS[0],
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Sales: %{y:" + y_fmt + "}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Profit",
        x=categories,
        y=profit,
        marker_color=COLORS[1],
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Profit: %{y:" + y_fmt + "}<extra></extra>",
    ))
    layout = base_layout("Sales and Profit by Category")
    layout["barmode"] = "group"
    layout["bargap"] = 0.35
    layout["bargroupgap"] = 0.15
    fig.update_layout(**layout)
    fig.update_xaxes(**axis_style("Category", showgrid=False))
    fig.update_yaxes(**axis_style("Amount", tickformat=y_fmt))
    return fig.to_plotly_json()


def create_region_chart(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a pie chart for sales by region."""
    regions = [d["region"] for d in data]
    sales = [d["sales"] for d in data]
    y_fmt = auto_currency_tickformat(sales)

    fig = go.Figure(data=[go.Pie(
        labels=regions,
        values=sales,
        hole=0.5,
        marker_colors=COLORS,
        marker_line_width=2,
        marker_line_color="white",
        sort=False,
        textposition="outside",
        textinfo="label+percent",
        textfont=dict(size=11),
        insidetextorientation="horizontal",
        pull=[0.01] * len(regions),
        hovertemplate="<b>%{label}</b><br>Sales: %{value:" + y_fmt + "}<br>Share: %{percent}<extra></extra>",
    )])
    layout = base_layout("", showlegend=False)
    layout["margin"] = {"l": 20, "r": 20, "t": 20, "b": 20}
    fig.update_layout(**layout)
    return fig.to_plotly_json()


def create_trends_chart(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a line chart for sales trends."""
    months = [d["month"] for d in data]
    sales = [d["sales"] for d in data]
    profit = [d["profit"] for d in data]
    y_fmt = auto_currency_tickformat([*sales, *profit])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, y=sales, mode="lines+markers", name="Sales",
        line=dict(color=COLORS[0], width=2.5, shape="spline"),
        marker=dict(size=7, color=COLORS[0], line=dict(width=2, color="white")),
        hovertemplate="Sales: %{y:" + y_fmt + "}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=months, y=profit, mode="lines+markers", name="Profit",
        line=dict(color=COLORS[1], width=2.5, dash="dot", shape="spline"),
        marker=dict(size=7, color=COLORS[1], line=dict(width=2, color="white")),
        hovertemplate="Profit: %{y:" + y_fmt + "}<extra></extra>",
    ))
    fig.update_layout(**base_layout("Monthly Sales and Profit Trends"))
    fig.update_xaxes(**{**axis_style("", showgrid=False), "tickangle": -45})
    fig.update_yaxes(**axis_style("", tickformat=y_fmt))
    return fig.to_plotly_json()


def create_profit_chart(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a horizontal bar chart for profit by sub-category."""
    sorted_data = sorted(data, key=lambda x: x["profit"])
    sub_categories = [d["sub_category"] for d in sorted_data]
    profit = [d["profit"] for d in sorted_data]
    colors = [COLORS[1] if p >= 0 else NEGATIVE_COLOR for p in profit]
    x_fmt = auto_currency_tickformat(profit)

    fig = go.Figure(data=[go.Bar(
        y=sub_categories, x=profit, orientation="h",
        marker_color=colors,
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Profit: %{x:" + x_fmt + "}<extra></extra>",
    )])
    layout = base_layout("", height=520, showlegend=False)
    layout["bargap"] = 0.3
    layout["margin"] = {"l": 110, "r": 25, "t": 20, "b": 45}
    fig.update_layout(**layout)
    fig.update_xaxes(**axis_style("Profit", tickformat=x_fmt))
    fig.update_yaxes(**axis_style("", showgrid=False))
    return fig.to_plotly_json()


def create_segment_chart(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a bar chart for segment analysis."""
    segments = [d["segment"] for d in data]
    sales = [d["sales"] for d in data]
    customers = [d["customers"] for d in data]
    sales_fmt = auto_currency_tickformat(sales)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Sales ($)", x=segments, y=sales,
        marker_color=COLORS[0],
        marker_line_width=0,
        yaxis="y",
        hovertemplate="<b>%{x}</b><br>Sales: %{y:" + sales_fmt + "}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        name="Customers", x=segments, y=customers, mode="lines+markers",
        line=dict(color=COLORS[2], width=3),
        marker=dict(size=10, color=COLORS[2], line=dict(width=2, color="white")),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Customers: %{y:,}<extra></extra>",
    ))
    layout = base_layout("Sales and Customers by Segment")
    layout["bargap"] = 0.5
    fig.update_layout(**layout)
    fig.update_xaxes(**axis_style("", showgrid=False))
    fig.update_layout(
        yaxis=axis_style("Sales", tickformat=sales_fmt),
        yaxis2={**axis_style("Customers", tickformat=","), "side": "right", "overlaying": "y"},
    )
    return fig.to_plotly_json()


def create_choropleth_map(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a US choropleth map for sales by state."""
    states = [d["state_code"] for d in data]
    state_names = [d["state"] for d in data]
    sales = [d["sales"] for d in data]
    profit = [d["profit"] for d in data]
    orders = [d["orders"] for d in data]
    
    fig = go.Figure(data=go.Choropleth(
        locations=states,
        z=sales,
        locationmode="USA-states",
        colorscale=[
            [0, "#e8f5e9"],
            [0.2, "#a5d6a7"],
            [0.4, "#66bb6a"],
            [0.6, "#43a047"],
            [0.8, "#2e7d32"],
            [1, "#1b5e20"]
        ],
        colorbar=dict(
            title=dict(text="Sales ($)", font=dict(size=12)),
            tickformat="$,.0f",
            len=0.6,
            thickness=15,
            x=1.0,
        ),
        marker_line_color="white",
        marker_line_width=1.5,
        customdata=list(zip(state_names, profit, orders)),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Sales: $%{z:,.0f}<br>"
            "Profit: $%{customdata[1]:,.0f}<br>"
            "Orders: %{customdata[2]:,}<extra></extra>"
        ),
    ))
    
    fig.update_layout(
        geo=dict(
            scope="usa",
            bgcolor="rgba(248,250,252,0.95)",
            lakecolor="rgba(200,230,255,0.5)",
            landcolor="rgba(243,244,246,1)",
            showlakes=True,
            showland=True,
            subunitcolor="white",
            subunitwidth=1,
            projection=dict(type="albers usa"),
            fitbounds="locations",
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="white",
        font=dict(family="Inter, system-ui, sans-serif", size=11, color="#181818"),
        autosize=True,
    )
    
    return fig.to_plotly_json()
