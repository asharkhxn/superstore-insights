"""Sales API routes."""
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query

from app.services.data_service import DataService
from app.services.chart_service import ChartService

router = APIRouter()
data_service = DataService()
chart_service = ChartService(data_service)


@router.get("/filter-options")
async def get_filter_options():
    """Get available filter options."""
    try:
        return data_service.get_filter_options()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/overview")
async def get_sales_overview(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories")
):
    """Get overall sales metrics with optional filters."""
    try:
        return data_service.get_overview_metrics(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-category")
async def get_sales_by_category(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories")
):
    """Get sales data grouped by category with optional filters."""
    try:
        data = data_service.get_sales_by_category(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories
        )
        chart = chart_service.create_category_chart(data)
        return {"data": data, "chart": chart}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-region")
async def get_sales_by_region(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories")
):
    """Get sales data grouped by region with optional filters."""
    try:
        data = data_service.get_sales_by_region(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories
        )
        chart = chart_service.create_region_chart(data)
        return {"data": data, "chart": chart}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends")
async def get_sales_trends(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories")
):
    """Get sales trends over time with optional filters."""
    try:
        data = data_service.get_sales_trends(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories
        )
        chart = chart_service.create_trends_chart(data)
        return {"data": data, "chart": chart}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profit-analysis")
async def get_profit_analysis(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories")
):
    """Get profit analysis by category and sub-category with optional filters."""
    try:
        data = data_service.get_profit_analysis(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories
        )
        chart = chart_service.create_profit_chart(data)
        return {"data": data, "chart": chart}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/segment-analysis")
async def get_segment_analysis(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    regions: Optional[List[str]] = Query(None, description="Filter by regions"),
    segments: Optional[List[str]] = Query(None, description="Filter by segments"),
    categories: Optional[List[str]] = Query(None, description="Filter by categories")
):
    """Get sales analysis by customer segment with optional filters."""
    try:
        data = data_service.get_segment_analysis(
            start_date=start_date,
            end_date=end_date,
            regions=regions,
            segments=segments,
            categories=categories
        )
        chart = chart_service.create_segment_chart(data)
        return {"data": data, "chart": chart}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

