"""Shared chart styling utilities."""
from typing import Any, Dict, List, Optional


# Muted, financial dashboard-style palette
COLORS = [
    "#4F8AF0",  # blue
    "#34D399",  # green
    "#F59E0B",  # amber
    "#A78BFA",  # violet
    "#F97316",  # orange
    "#22C55E",  # emerald
]

NEGATIVE_COLOR = "#F87171"  # soft red

FONT_FAMILY = "Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial"

# Light UI defaults (transparent backgrounds)
_TEXT = "rgba(15,23,42,0.92)"
_TEXT_MUTED = "rgba(51,65,85,0.82)"
_GRID = "rgba(15,23,42,0.10)"
_TICK = "rgba(15,23,42,0.22)"


def base_layout(
    title: str,
    *,
    height: Optional[int] = None,
    showlegend: bool = True,
) -> Dict[str, Any]:
    """Create base layout for embedding in glass cards."""
    return {
        "title": {"text": title, "x": 0.02, "xanchor": "left"},
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"family": FONT_FAMILY, "size": 12, "color": _TEXT},
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
            "font": {"size": 11, "color": _TEXT_MUTED},
        },
        "hoverlabel": {
            "bgcolor": "rgba(255,255,255,0.98)",
            "bordercolor": "rgba(15,23,42,0.12)",
            "font": {"family": FONT_FAMILY, "size": 12, "color": _TEXT},
        },
    }


def axis_style(
    title: str,
    *,
    tickformat: Optional[str] = None,
    showgrid: bool = True,
) -> Dict[str, Any]:
    """Create consistent axis styling."""
    return {
        "title": {"text": title, "standoff": 12},
        "showgrid": showgrid,
        "gridcolor": _GRID,
        "zeroline": False,
        "showline": False,
        "ticks": "outside",
        "tickcolor": _TICK,
        "tickfont": {"color": _TEXT_MUTED},
        "tickformat": tickformat,
    }


def auto_currency_tickformat(values: List[float]) -> str:
    """Choose reasonable currency tickformat based on magnitude."""
    mag = max((abs(float(v)) for v in values if v is not None), default=0.0)
    if mag >= 1_000_000:
        return "$,.2s"
    if mag >= 10_000:
        return "$,.0f"
    return "$,.2f"
