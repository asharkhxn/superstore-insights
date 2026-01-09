"""Tests for the data service."""
import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.services.data_service import DataService


class TestDataServiceInit:
    """Tests for DataService initialization."""

    def test_data_service_init_no_df(self):
        """Test that DataService initializes without loading data."""
        with patch.object(DataService, '_load_data'):
            service = DataService()
            assert service._df is None

    def test_data_service_lazy_loads(self, sample_dataframe):
        """Test that DataService lazy loads data on access."""
        with patch.object(DataService, '_load_data', return_value=sample_dataframe) as mock_load:
            service = DataService()
            _ = service.df
            mock_load.assert_called_once()


class TestOverviewMetrics:
    """Tests for get_overview_metrics method."""

    def test_overview_returns_dict(self, mock_data_service):
        """Test that overview metrics returns a dictionary."""
        result = mock_data_service.get_overview_metrics()
        assert isinstance(result, dict)

    def test_overview_has_required_fields(self, mock_data_service):
        """Test that overview has all required fields."""
        result = mock_data_service.get_overview_metrics()
        required_fields = [
            'total_sales', 'total_profit', 'total_orders',
            'total_customers', 'avg_order_value', 'profit_margin'
        ]
        for field in required_fields:
            assert field in result

    def test_overview_calculates_total_sales(self, mock_data_service):
        """Test that total sales is calculated correctly."""
        result = mock_data_service.get_overview_metrics()
        # 500 + 50 + 300 + 1000 + 25 = 1875
        assert result['total_sales'] == 1875.0

    def test_overview_calculates_total_profit(self, mock_data_service):
        """Test that total profit is calculated correctly."""
        result = mock_data_service.get_overview_metrics()
        # 100 + 10 + (-20) + 200 + 5 = 295
        assert result['total_profit'] == 295.0

    def test_overview_counts_unique_orders(self, mock_data_service):
        """Test that order count is unique orders."""
        result = mock_data_service.get_overview_metrics()
        # ORD-001, ORD-002, ORD-003 = 3 unique orders
        assert result['total_orders'] == 3

    def test_overview_counts_unique_customers(self, mock_data_service):
        """Test that customer count is unique customers."""
        result = mock_data_service.get_overview_metrics()
        # CUST-001, CUST-002, CUST-003 = 3 unique customers
        assert result['total_customers'] == 3


class TestSalesByCategory:
    """Tests for get_sales_by_category method."""

    def test_category_returns_list(self, mock_data_service):
        """Test that category data returns a list."""
        result = mock_data_service.get_sales_by_category()
        assert isinstance(result, list)

    def test_category_has_required_fields(self, mock_data_service):
        """Test that each category record has required fields."""
        result = mock_data_service.get_sales_by_category()
        required_fields = ['category', 'sales', 'profit', 'quantity', 'orders']
        for record in result:
            for field in required_fields:
                assert field in record

    def test_category_groups_correctly(self, mock_data_service):
        """Test that categories are grouped correctly."""
        result = mock_data_service.get_sales_by_category()
        categories = [r['category'] for r in result]
        # Technology, Office Supplies, Furniture
        assert len(categories) == 3
        assert 'Technology' in categories
        assert 'Office Supplies' in categories
        assert 'Furniture' in categories


class TestSalesByRegion:
    """Tests for get_sales_by_region method."""

    def test_region_returns_list(self, mock_data_service):
        """Test that region data returns a list."""
        result = mock_data_service.get_sales_by_region()
        assert isinstance(result, list)

    def test_region_has_required_fields(self, mock_data_service):
        """Test that each region record has required fields."""
        result = mock_data_service.get_sales_by_region()
        required_fields = ['region', 'sales', 'profit', 'quantity', 'orders']
        for record in result:
            for field in required_fields:
                assert field in record

    def test_region_groups_correctly(self, mock_data_service):
        """Test that regions are grouped correctly."""
        result = mock_data_service.get_sales_by_region()
        regions = [r['region'] for r in result]
        # East, West, Central
        assert len(regions) == 3


class TestSalesTrends:
    """Tests for get_sales_trends method."""

    def test_trends_returns_list(self, mock_data_service):
        """Test that trends data returns a list."""
        result = mock_data_service.get_sales_trends()
        assert isinstance(result, list)

    def test_trends_has_required_fields(self, mock_data_service):
        """Test that each trend record has required fields."""
        result = mock_data_service.get_sales_trends()
        required_fields = ['month', 'sales', 'profit', 'orders']
        for record in result:
            for field in required_fields:
                assert field in record

    def test_trends_sorted_by_month(self, mock_data_service):
        """Test that trends are sorted by month."""
        result = mock_data_service.get_sales_trends()
        months = [r['month'] for r in result]
        assert months == sorted(months)


class TestProfitAnalysis:
    """Tests for get_profit_analysis method."""

    def test_profit_returns_list(self, mock_data_service):
        """Test that profit analysis returns a list."""
        result = mock_data_service.get_profit_analysis()
        assert isinstance(result, list)

    def test_profit_has_required_fields(self, mock_data_service):
        """Test that each profit record has required fields."""
        result = mock_data_service.get_profit_analysis()
        required_fields = ['category', 'sub_category', 'sales', 'profit', 'quantity', 'profit_margin']
        for record in result:
            for field in required_fields:
                assert field in record

    def test_profit_margin_calculated(self, mock_data_service):
        """Test that profit margin is calculated correctly."""
        result = mock_data_service.get_profit_analysis()
        for record in result:
            if record['sales'] > 0:
                expected_margin = round(record['profit'] / record['sales'] * 100, 2)
                assert record['profit_margin'] == expected_margin


class TestSegmentAnalysis:
    """Tests for get_segment_analysis method."""

    def test_segment_returns_list(self, mock_data_service):
        """Test that segment analysis returns a list."""
        result = mock_data_service.get_segment_analysis()
        assert isinstance(result, list)

    def test_segment_has_required_fields(self, mock_data_service):
        """Test that each segment record has required fields."""
        result = mock_data_service.get_segment_analysis()
        required_fields = ['segment', 'sales', 'profit', 'customers', 'orders']
        for record in result:
            for field in required_fields:
                assert field in record

    def test_segment_groups_correctly(self, mock_data_service):
        """Test that segments are grouped correctly."""
        result = mock_data_service.get_segment_analysis()
        segments = [r['segment'] for r in result]
        # Consumer, Corporate, Home Office
        assert len(segments) == 3
