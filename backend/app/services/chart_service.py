"""Chart service for creating Plotly visualizations."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

import plotly.graph_objects as go

from app.services.data_service import DataService


class ChartService:
    """Service for creating Plotly chart configurations."""

    # Muted, “financial dashboard”-style palette (no default Plotly colors)
    COLORS = [
        "#4F8AF0",  # blue
        "#34D399",  # green
        "#F59E0B",  # amber
        "#A78BFA",  # violet
        "#F97316",  # orange
        "#22C55E",  # emerald
    ]

    NEGATIVE = "#F87171"  # soft red

    FONT_FAMILY = "Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial"

    # Light UI defaults (transparent backgrounds so charts inherit card surface)
    _TEXT = "rgba(15,23,42,0.92)"  # slate-900
    _TEXT_MUTED = "rgba(51,65,85,0.82)"  # slate-700
    _GRID = "rgba(15,23,42,0.10)"
    _TICK = "rgba(15,23,42,0.22)"

    def _base_layout(
        self,
        title: str,
        *,
        height: Optional[int] = None,
        showlegend: bool = True,
    ) -> Dict[str, Any]:
        """Base layout tuned for embedding inside glass cards (transparent background)."""

        return {
            "title": {"text": title, "x": 0.02, "xanchor": "left"},
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"family": self.FONT_FAMILY, "size": 12, "color": self._TEXT},
            "margin": {"l": 56, "r": 24, "t": 54, "b": 52},
            "height": height,
            "showlegend": showlegend,
            "legend": {
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.02,
                "xanchor": "left",
                "x": 0.0,
                "bgcolor": "rgba(0,0,0,0)",
                "font": {"size": 11, "color": self._TEXT_MUTED},
            },
            "hoverlabel": {
                "bgcolor": "rgba(255,255,255,0.98)",
                "bordercolor": "rgba(15,23,42,0.12)",
                "font": {"family": self.FONT_FAMILY, "size": 12, "color": self._TEXT},
            },
        }

    def _axis(self, title: str, *, tickformat: Optional[str] = None, showgrid: bool = True) -> Dict[str, Any]:
        return {
            "title": {"text": title, "standoff": 12},
            "showgrid": showgrid,
            "gridcolor": self._GRID,
            "zeroline": False,
            "showline": False,
            "ticks": "outside",
            "tickcolor": self._TICK,
            "tickfont": {"color": self._TEXT_MUTED},
            "tickformat": tickformat,
        }

    def _auto_currency_tickformat(self, values: List[float]) -> str:
        """Choose a reasonable currency tickformat based on magnitude."""
        mag = 0.0
        for v in values:
            if v is None:
                continue
            mag = max(mag, abs(float(v)))
        if mag >= 1_000_000:
            return "$,.2s"  # $1.2M
        if mag >= 10_000:
            return "$,.0f"
        return "$,.2f"

    def __init__(self, data_service: DataService):
        """Initialize chart service with data service."""
        self.data_service = data_service

    def _to_plotly_json(self, fig: go.Figure) -> Dict[str, Any]:
        """Convert Plotly figure to JSON-serializable dict."""
        return fig.to_plotly_json()

    def create_category_chart(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a bar chart for sales by category."""
        categories = [d['category'] for d in data]
        sales = [d['sales'] for d in data]
        profit = [d['profit'] for d in data]

        y_fmt = self._auto_currency_tickformat([*sales, *profit])

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Sales',
            x=categories,
            y=sales,
            marker_color=self.COLORS[0],
            hovertemplate="<b>%{x}</b><br>Sales: %{y:" + y_fmt + "}<extra></extra>",
        ))
        fig.add_trace(go.Bar(
            name='Profit',
            x=categories,
            y=profit,
            marker_color=self.COLORS[1],
            hovertemplate="<b>%{x}</b><br>Profit: %{y:" + y_fmt + "}<extra></extra>",
        ))

        fig.update_layout(
            **self._base_layout("Sales and Profit by Category"),
            barmode="group",
            bargap=0.22,
        )
        fig.update_xaxes(**self._axis("Category", showgrid=False))
        fig.update_yaxes(**self._axis("Amount", tickformat=y_fmt))

        return self._to_plotly_json(fig)

    def create_region_chart(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a pie chart for sales by region."""
        regions = [d['region'] for d in data]
        sales = [d['sales'] for d in data]

        y_fmt = self._auto_currency_tickformat(sales)

        fig = go.Figure(data=[go.Pie(
            labels=regions,
            values=sales,
            hole=0.4,
            marker_colors=self.COLORS,
            sort=False,
            textposition="outside",
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Sales: %{value:" + y_fmt + "}<br>Share: %{percent}<extra></extra>",
        )])

        fig.update_layout(**self._base_layout("Sales Distribution by Region"))

        return self._to_plotly_json(fig)

    def create_trends_chart(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a line chart for sales trends."""
        months = [d['month'] for d in data]
        sales = [d['sales'] for d in data]
        profit = [d['profit'] for d in data]

        y_fmt = self._auto_currency_tickformat([*sales, *profit])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=sales,
            mode='lines+markers',
            name='Sales',
            line=dict(color=self.COLORS[0], width=2.6),
            marker=dict(size=6, color=self.COLORS[0]),
            hovertemplate="<b>%{x}</b><br>Sales: %{y:" + y_fmt + "}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=months,
            y=profit,
            mode='lines+markers',
            name='Profit',
            line=dict(color=self.COLORS[1], width=2.2, dash="dot"),
            marker=dict(size=6, color=self.COLORS[1]),
            hovertemplate="<b>%{x}</b><br>Profit: %{y:" + y_fmt + "}<extra></extra>",
        ))

        fig.update_layout(**self._base_layout("Monthly Sales and Profit Trends"))
        fig.update_xaxes(**{**self._axis("Month", showgrid=False), "tickangle": 0})
        fig.update_yaxes(**self._axis("Amount", tickformat=y_fmt))

        return self._to_plotly_json(fig)

    def create_profit_chart(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a horizontal bar chart for profit by sub-category."""
        # Sort by profit
        sorted_data = sorted(data, key=lambda x: x['profit'])
        
        sub_categories = [d['sub_category'] for d in sorted_data]
        profit = [d['profit'] for d in sorted_data]
        colors = [self.COLORS[1] if p >= 0 else self.NEGATIVE for p in profit]

        x_fmt = self._auto_currency_tickformat(profit)

        fig = go.Figure(data=[go.Bar(
            y=sub_categories,
            x=profit,
            orientation='h',
            marker_color=colors,
            hovertemplate="<b>%{y}</b><br>Profit: %{x:" + x_fmt + "}<extra></extra>",
        )])

        fig.update_layout(**self._base_layout("Profit by Sub-Category", height=520, showlegend=False))
        fig.update_xaxes(**self._axis("Profit", tickformat=x_fmt))
        fig.update_yaxes(**self._axis("Sub-Category", showgrid=False))

        return self._to_plotly_json(fig)

    def create_segment_chart(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a bar chart for segment analysis."""
        segments = [d['segment'] for d in data]
        sales = [d['sales'] for d in data]
        customers = [d['customers'] for d in data]

        sales_fmt = self._auto_currency_tickformat(sales)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Sales ($)',
            x=segments,
            y=sales,
            marker_color=self.COLORS[0],
            yaxis='y',
            hovertemplate="<b>%{x}</b><br>Sales: %{y:" + sales_fmt + "}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            name='Customers',
            x=segments,
            y=customers,
            mode='lines+markers',
            marker_color=self.COLORS[2],
            line=dict(color=self.COLORS[2], width=2.2),
            marker=dict(size=7, color=self.COLORS[2]),
            yaxis='y2',
            hovertemplate="<b>%{x}</b><br>Customers: %{y:,}<extra></extra>",
        ))

        fig.update_layout(**self._base_layout("Sales and Customers by Segment"))
        fig.update_xaxes(**self._axis("Segment", showgrid=False))
        fig.update_layout(
            yaxis=self._axis("Sales", tickformat=sales_fmt),
            yaxis2={
                **self._axis("Customers", tickformat=","),
                "side": "right",
                "overlaying": "y",
            },
        )

        return self._to_plotly_json(fig)
