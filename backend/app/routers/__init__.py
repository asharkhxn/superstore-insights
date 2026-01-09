"""API routers package."""
from app.routers.health import router as health_router
from app.routers.sales import router as sales_router

__all__ = ["health_router", "sales_router"]
