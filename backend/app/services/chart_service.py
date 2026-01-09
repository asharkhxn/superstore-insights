"""Chart service for creating Plotly visualizations."""
from typing import Any, Dict, List

from app.services.data_service import DataService
from app.services import chart_builders


class ChartService:
    """Facade service for chart generation."""

    def __init__(self, data_service: DataService) -> None:
        """Initialize with a data service."""
        self.data_service = data_service

    def create_category_chart(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a bar chart for sales by category."""
        return chart_builders.create_category_chart(data)

    def create_region_chart(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a pie chart for sales by region."""
        return chart_builders.create_region_chart(data)

    def create_trends_chart(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a line chart for sales trends."""
        return chart_builders.create_trends_chart(data)

    def create_profit_chart(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a horizontal bar chart for profit by sub-category."""
        return chart_builders.create_profit_chart(data)

    def create_segment_chart(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a bar chart for segment analysis."""
        return chart_builders.create_segment_chart(data)

    def create_choropleth_map(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a US choropleth map for sales by state."""
        return chart_builders.create_choropleth_map(data)
