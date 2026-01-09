"""Shared chart styling utilities."""
from typing import Any, Dict, List, Optional


# Salesforce Lightning Design System inspired palette
COLORS = [
    "#0176d3",  # Salesforce blue
    "#06a59a",  # Teal
    "#b78def",  # Purple
    "#ff6d7e",  # Pink/Coral
    "#ffc95f",  # Yellow
    "#3dba82",  # Green
]

NEGATIVE_COLOR = "#c23934"  # Salesforce error red

FONT_FAMILY = "'Salesforce Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"

# Salesforce-style light UI
_TEXT = "#181818"
_TEXT_MUTED = "#706e6b"
_GRID = "rgba(0,0,0,0.06)"
_TICK = "rgba(0,0,0,0)"


def base_layout(
    title: str,
    *,
    height: Optional[int] = None,
    showlegend: bool = True,
) -> Dict[str, Any]:
    """Create base layout for embedding in glass cards."""
    return {
        "title": None,  # Title handled by card header in frontend
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"family": FONT_FAMILY, "size": 12, "color": _TEXT},
        "margin": {"l": 65, "r": 25, "t": 40, "b": 45, "pad": 4},
        "height": height,
        "showlegend": showlegend,
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "center",
            "x": 0.5,
            "bgcolor": "rgba(0,0,0,0)",
            "font": {"size": 11, "color": _TEXT_MUTED},
            "itemsizing": "constant",
            "tracegroupgap": 20,
        },
        "hoverlabel": {
            "bgcolor": "white",
            "bordercolor": "#c9c9c9",
            "font": {"family": FONT_FAMILY, "size": 12, "color": _TEXT},
        },
        "hovermode": "x unified",
    }


def axis_style(
    title: str,
    *,
    tickformat: Optional[str] = None,
    showgrid: bool = True,
) -> Dict[str, Any]:
    """Create consistent axis styling."""
    return {
        "title": {
            "text": title,
            "standoff": 16,
            "font": {"size": 12, "color": _TEXT_MUTED},
        },
        "showgrid": showgrid,
        "gridcolor": _GRID,
        "gridwidth": 1,
        "zeroline": False,
        "showline": False,
        "ticks": "",
        "tickcolor": _TICK,
        "tickfont": {"size": 11, "color": _TEXT_MUTED},
        "tickformat": tickformat,
        "automargin": True,
    }


def auto_currency_tickformat(values: List[float]) -> str:
    """Choose reasonable currency tickformat based on magnitude."""
    mag = max((abs(float(v)) for v in values if v is not None), default=0.0)
    if mag >= 1_000_000:
        return "$,.2s"
    if mag >= 10_000:
        return "$,.0f"
    return "$,.2f"
