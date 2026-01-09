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
        hovertemplate="<b>%{x}</b><br>Sales: %{y:" + y_fmt + "}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Profit",
        x=categories,
        y=profit,
        marker_color=COLORS[1],
        hovertemplate="<b>%{x}</b><br>Profit: %{y:" + y_fmt + "}<extra></extra>",
    ))
    fig.update_layout(**base_layout("Sales and Profit by Category"), barmode="group", bargap=0.22)
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
        hole=0.4,
        marker_colors=COLORS,
        sort=False,
        textposition="outside",
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Sales: %{value:" + y_fmt + "}<br>Share: %{percent}<extra></extra>",
    )])
    fig.update_layout(**base_layout("Sales Distribution by Region"))
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
        line=dict(color=COLORS[0], width=2.6),
        marker=dict(size=6, color=COLORS[0]),
        hovertemplate="<b>%{x}</b><br>Sales: %{y:" + y_fmt + "}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=months, y=profit, mode="lines+markers", name="Profit",
        line=dict(color=COLORS[1], width=2.2, dash="dot"),
        marker=dict(size=6, color=COLORS[1]),
        hovertemplate="<b>%{x}</b><br>Profit: %{y:" + y_fmt + "}<extra></extra>",
    ))
    fig.update_layout(**base_layout("Monthly Sales and Profit Trends"))
    fig.update_xaxes(**{**axis_style("Month", showgrid=False), "tickangle": 0})
    fig.update_yaxes(**axis_style("Amount", tickformat=y_fmt))
    return fig.to_plotly_json()


def create_profit_chart(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a horizontal bar chart for profit by sub-category."""
    sorted_data = sorted(data, key=lambda x: x["profit"])
    sub_categories = [d["sub_category"] for d in sorted_data]
    profit = [d["profit"] for d in sorted_data]
    colors = [COLORS[1] if p >= 0 else NEGATIVE_COLOR for p in profit]
    x_fmt = auto_currency_tickformat(profit)

    fig = go.Figure(data=[go.Bar(
        y=sub_categories, x=profit, orientation="h", marker_color=colors,
        hovertemplate="<b>%{y}</b><br>Profit: %{x:" + x_fmt + "}<extra></extra>",
    )])
    fig.update_layout(**base_layout("Profit by Sub-Category", height=520, showlegend=False))
    fig.update_xaxes(**axis_style("Profit", tickformat=x_fmt))
    fig.update_yaxes(**axis_style("Sub-Category", showgrid=False))
    return fig.to_plotly_json()


def create_segment_chart(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a bar chart for segment analysis."""
    segments = [d["segment"] for d in data]
    sales = [d["sales"] for d in data]
    customers = [d["customers"] for d in data]
    sales_fmt = auto_currency_tickformat(sales)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Sales ($)", x=segments, y=sales, marker_color=COLORS[0], yaxis="y",
        hovertemplate="<b>%{x}</b><br>Sales: %{y:" + sales_fmt + "}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        name="Customers", x=segments, y=customers, mode="lines+markers",
        marker_color=COLORS[2], line=dict(color=COLORS[2], width=2.2),
        marker=dict(size=7, color=COLORS[2]), yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Customers: %{y:,}<extra></extra>",
    ))
    fig.update_layout(**base_layout("Sales and Customers by Segment"))
    fig.update_xaxes(**axis_style("Segment", showgrid=False))
    fig.update_layout(
        yaxis=axis_style("Sales", tickformat=sales_fmt),
        yaxis2={**axis_style("Customers", tickformat=","), "side": "right", "overlaying": "y"},
    )
    return fig.to_plotly_json()
