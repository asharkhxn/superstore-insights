"""Sales API routes."""
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.dependencies import get_chart_service, get_data_service
from app.services.chart_service import ChartService
from app.services.data_service import DataService
from app.services.repository import DataLoadError, DataValidationError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sales", tags=["sales"])


def handle_service_error(e: Exception, operation: str) -> HTTPException:
    """Convert service exceptions to appropriate HTTP errors."""
    logger.error(f"Error in {operation}: {e}", exc_info=True)
    
    if isinstance(e, DataLoadError):
        return HTTPException(
            status_code=503,
            detail={
                "error": "Data Source Unavailable",
                "message": str(e),
                "code": "DATA_LOAD_ERROR"
            }
        )
    elif isinstance(e, DataValidationError):
        return HTTPException(
            status_code=500,
            detail={
                "error": "Data Validation Failed",
                "message": str(e),
                "code": "DATA_VALIDATION_ERROR"
            }
        )
    elif isinstance(e, ValueError):
        return HTTPException(
            status_code=400,
            detail={
                "error": "Invalid Request",
                "message": str(e),
                "code": "INVALID_REQUEST"
            }
        )
    else:
        return HTTPException(
            status_code=500,
            detail={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred. Please try again later.",
                "code": "INTERNAL_ERROR"
            }
        )


@router.get("/filter-options")
async def get_filter_options(
    data_service: DataService = Depends(get_data_service),
) -> dict:
    """Get available filter options."""
    try:
        return data_service.get_filter_options()
    except Exception as e:
        raise handle_service_error(e, "get_filter_options")


@router.get("/overview")
async def get_sales_overview(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories"),
    data_service: DataService = Depends(get_data_service),
) -> dict:
    """Get overall sales metrics with optional filters."""
    try:
        return data_service.get_overview_metrics(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories,
        )
    except Exception as e:
        raise handle_service_error(e, "get_sales_overview")


@router.get("/by-category")
async def get_sales_by_category(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories"),
    data_service: DataService = Depends(get_data_service),
    chart_service: ChartService = Depends(get_chart_service),
) -> dict:
    """Get sales data grouped by category with optional filters."""
    try:
        data = data_service.get_sales_by_category(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories,
        )
        chart = chart_service.create_category_chart(data)
        return {"data": data, "chart": chart}
    except Exception as e:
        raise handle_service_error(e, "get_sales_by_category")


@router.get("/by-region")
async def get_sales_by_region(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories"),
    data_service: DataService = Depends(get_data_service),
    chart_service: ChartService = Depends(get_chart_service),
) -> dict:
    """Get sales data grouped by region with optional filters."""
    try:
        data = data_service.get_sales_by_region(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories,
        )
        chart = chart_service.create_region_chart(data)
        return {"data": data, "chart": chart}
    except Exception as e:
        raise handle_service_error(e, "get_sales_by_region")


@router.get("/trends")
async def get_sales_trends(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories"),
    data_service: DataService = Depends(get_data_service),
    chart_service: ChartService = Depends(get_chart_service),
) -> dict:
    """Get sales trends over time with optional filters."""
    try:
        data = data_service.get_sales_trends(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories,
        )
        chart = chart_service.create_trends_chart(data)
        return {"data": data, "chart": chart}
    except Exception as e:
        raise handle_service_error(e, "get_sales_trends")


@router.get("/profit-analysis")
async def get_profit_analysis(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories"),
    data_service: DataService = Depends(get_data_service),
    chart_service: ChartService = Depends(get_chart_service),
) -> dict:
    """Get profit analysis by category and sub-category with optional filters."""
    try:
        data = data_service.get_profit_analysis(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories,
        )
        chart = chart_service.create_profit_chart(data)
        return {"data": data, "chart": chart}
    except Exception as e:
        raise handle_service_error(e, "get_profit_analysis")


@router.get("/segment-analysis")
async def get_segment_analysis(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories"),
    data_service: DataService = Depends(get_data_service),
    chart_service: ChartService = Depends(get_chart_service),
) -> dict:
    """Get sales analysis by customer segment with optional filters."""
    try:
        data = data_service.get_segment_analysis(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories,
        )
        chart = chart_service.create_segment_chart(data)
        return {"data": data, "chart": chart}
    except Exception as e:
        raise handle_service_error(e, "get_segment_analysis")


@router.get("/geo-sales")
async def get_geo_sales(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories"),
    data_service: DataService = Depends(get_data_service),
    chart_service: ChartService = Depends(get_chart_service),
) -> dict:
    """Get geographic sales distribution by US state."""
    try:
        data = data_service.get_state_sales(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories,
        )
        chart = chart_service.create_choropleth_map(data)
        return {"data": data, "chart": chart}
    except Exception as e:
        raise handle_service_error(e, "get_geo_sales")
