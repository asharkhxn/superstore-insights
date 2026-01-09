"""Tests for the sales API routes."""
import pytest
from unittest.mock import patch, MagicMock

from app.services.data_service import DataService


class TestSalesOverviewEndpoint:
    """Tests for the /api/sales/overview endpoint."""

    def test_overview_returns_200(self, client, mock_data_service):
        """Test that overview endpoint returns 200."""
        with patch('app.routes.sales.data_service', mock_data_service):
            response = client.get("/api/sales/overview")
            assert response.status_code == 200

    def test_overview_returns_metrics(self, client, mock_data_service):
        """Test that overview returns metrics data."""
        with patch('app.routes.sales.data_service', mock_data_service):
            response = client.get("/api/sales/overview")
            data = response.json()
            assert 'total_sales' in data
            assert 'total_profit' in data


class TestSalesByCategoryEndpoint:
    """Tests for the /api/sales/by-category endpoint."""

    def test_category_returns_200(self, client, mock_data_service):
        """Test that category endpoint returns 200."""
        with patch('app.routes.sales.data_service', mock_data_service):
            with patch('app.routes.sales.chart_service') as mock_chart:
                mock_chart.create_category_chart.return_value = {'data': [], 'layout': {}}
                response = client.get("/api/sales/by-category")
                assert response.status_code == 200

    def test_category_returns_data_and_chart(self, client, mock_data_service):
        """Test that category returns both data and chart."""
        with patch('app.routes.sales.data_service', mock_data_service):
            with patch('app.routes.sales.chart_service') as mock_chart:
                mock_chart.create_category_chart.return_value = {'data': [], 'layout': {}}
                response = client.get("/api/sales/by-category")
                data = response.json()
                assert 'data' in data
                assert 'chart' in data


class TestSalesByRegionEndpoint:
    """Tests for the /api/sales/by-region endpoint."""

    def test_region_returns_200(self, client, mock_data_service):
        """Test that region endpoint returns 200."""
        with patch('app.routes.sales.data_service', mock_data_service):
            with patch('app.routes.sales.chart_service') as mock_chart:
                mock_chart.create_region_chart.return_value = {'data': [], 'layout': {}}
                response = client.get("/api/sales/by-region")
                assert response.status_code == 200


class TestSalesTrendsEndpoint:
    """Tests for the /api/sales/trends endpoint."""

    def test_trends_returns_200(self, client, mock_data_service):
        """Test that trends endpoint returns 200."""
        with patch('app.routes.sales.data_service', mock_data_service):
            with patch('app.routes.sales.chart_service') as mock_chart:
                mock_chart.create_trends_chart.return_value = {'data': [], 'layout': {}}
                response = client.get("/api/sales/trends")
                assert response.status_code == 200


class TestProfitAnalysisEndpoint:
    """Tests for the /api/sales/profit-analysis endpoint."""

    def test_profit_returns_200(self, client, mock_data_service):
        """Test that profit analysis endpoint returns 200."""
        with patch('app.routes.sales.data_service', mock_data_service):
            with patch('app.routes.sales.chart_service') as mock_chart:
                mock_chart.create_profit_chart.return_value = {'data': [], 'layout': {}}
                response = client.get("/api/sales/profit-analysis")
                assert response.status_code == 200


class TestSegmentAnalysisEndpoint:
    """Tests for the /api/sales/segment-analysis endpoint."""

    def test_segment_returns_200(self, client, mock_data_service):
        """Test that segment analysis endpoint returns 200."""
        with patch('app.routes.sales.data_service', mock_data_service):
            with patch('app.routes.sales.chart_service') as mock_chart:
                mock_chart.create_segment_chart.return_value = {'data': [], 'layout': {}}
                response = client.get("/api/sales/segment-analysis")
                assert response.status_code == 200
