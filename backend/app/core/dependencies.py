"""Dependency injection for FastAPI."""
from functools import lru_cache

from app.services.data_service import DataService
from app.services.chart_service import ChartService


@lru_cache
def get_data_service() -> DataService:
    """Return a singleton DataService instance."""
    return DataService()


@lru_cache
def get_chart_service() -> ChartService:
    """Return a singleton ChartService instance."""
    return ChartService(get_data_service())
