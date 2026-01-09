"""Data service facade for sales analytics."""
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.services.repository import DataRepository
from app.services.filters import apply_filters
from app.services import analytics


class DataService:
    """Facade service providing sales analytics capabilities."""

    def __init__(self, repository: Optional[DataRepository] = None) -> None:
        """Initialize with optional repository injection."""
        self._repo = repository or DataRepository()
        self._df = None

    @property
    def df(self):
        """Lazy load the dataframe."""
        if self._df is None:
            self._df = self._repo.get_dataframe()
        return self._df

    @property
    def last_refresh(self) -> Optional[datetime]:
        """Get last data refresh timestamp."""
        return self._repo.last_refresh

    def _get_filtered_df(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
    ):
        """Get filtered dataframe."""
        return apply_filters(
            self.df, start_date, end_date, regions, segments, categories
        )

    def get_overview_metrics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Get high-level sales metrics."""
        df = self._get_filtered_df(start_date, end_date, regions, segments, categories)
        return analytics.compute_overview_metrics(df)

    def get_sales_by_category(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get sales grouped by category."""
        df = self._get_filtered_df(start_date, end_date, regions, segments, categories)
        return analytics.compute_sales_by_category(df)

    def get_sales_by_region(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get sales grouped by region."""
        df = self._get_filtered_df(start_date, end_date, regions, segments, categories)
        return analytics.compute_sales_by_region(df)

    def get_sales_trends(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get monthly sales trends."""
        df = self._get_filtered_df(start_date, end_date, regions, segments, categories)
        return analytics.compute_sales_trends(df)

    def get_profit_analysis(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get profit analysis by sub-category."""
        df = self._get_filtered_df(start_date, end_date, regions, segments, categories)
        return analytics.compute_profit_analysis(df)

    def get_segment_analysis(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get sales analysis by customer segment."""
        df = self._get_filtered_df(start_date, end_date, regions, segments, categories)
        return analytics.compute_segment_analysis(df)

    def get_filter_options(self) -> Dict[str, Any]:
        """Get available filter options."""
        return analytics.compute_filter_options(self.df)
