"""Pydantic models for API responses."""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str


class OverviewMetrics(BaseModel):
    """Overview metrics response."""
    total_sales: float
    total_profit: float
    total_orders: int
    total_customers: int
    avg_order_value: float
    profit_margin: float


class CategoryData(BaseModel):
    """Category sales data."""
    category: str
    sales: float
    profit: float
    quantity: int
    orders: int


class RegionData(BaseModel):
    """Region sales data."""
    region: str
    sales: float
    profit: float
    quantity: int
    orders: int


class TrendData(BaseModel):
    """Monthly trend data."""
    month: str
    sales: float
    profit: float
    orders: int


class ProfitData(BaseModel):
    """Profit analysis data."""
    category: str
    sub_category: str
    sales: float
    profit: float
    quantity: int
    profit_margin: float


class SegmentData(BaseModel):
    """Segment analysis data."""
    segment: str
    sales: float
    profit: float
    customers: int
    orders: int


class ChartResponse(BaseModel):
    """Response with data and chart configuration."""
    data: List[Dict[str, Any]]
    chart: Dict[str, Any]
