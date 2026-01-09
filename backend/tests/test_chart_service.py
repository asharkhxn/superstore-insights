"""Tests for the chart service."""
import pytest

from app.services.chart_service import ChartService
from app.services.chart_styles import COLORS


class TestChartServiceInit:
    """Tests for ChartService initialization."""

    def test_chart_service_init(self, mock_data_service):
        """Test that ChartService initializes correctly."""
        chart_service = ChartService(mock_data_service)
        assert chart_service.data_service == mock_data_service

    def test_chart_colors_exist(self):
        """Test that chart color palette exists."""
        assert len(COLORS) > 0


class TestCategoryChart:
    """Tests for create_category_chart method."""

    def test_category_chart_returns_dict(self, mock_data_service):
        """Test that category chart returns a dictionary."""
        chart_service = ChartService(mock_data_service)
        data = mock_data_service.get_sales_by_category()
        result = chart_service.create_category_chart(data)
        assert isinstance(result, dict)

    def test_category_chart_has_data(self, mock_data_service):
        """Test that category chart has data property."""
        chart_service = ChartService(mock_data_service)
        data = mock_data_service.get_sales_by_category()
        result = chart_service.create_category_chart(data)
        assert 'data' in result

    def test_category_chart_has_layout(self, mock_data_service):
        """Test that category chart has layout property."""
        chart_service = ChartService(mock_data_service)
        data = mock_data_service.get_sales_by_category()
        result = chart_service.create_category_chart(data)
        assert 'layout' in result


class TestRegionChart:
    """Tests for create_region_chart method."""

    def test_region_chart_returns_dict(self, mock_data_service):
        """Test that region chart returns a dictionary."""
        chart_service = ChartService(mock_data_service)
        data = mock_data_service.get_sales_by_region()
        result = chart_service.create_region_chart(data)
        assert isinstance(result, dict)

    def test_region_chart_has_data(self, mock_data_service):
        """Test that region chart has data property."""
        chart_service = ChartService(mock_data_service)
        data = mock_data_service.get_sales_by_region()
        result = chart_service.create_region_chart(data)
        assert 'data' in result


class TestTrendsChart:
    """Tests for create_trends_chart method."""

    def test_trends_chart_returns_dict(self, mock_data_service):
        """Test that trends chart returns a dictionary."""
        chart_service = ChartService(mock_data_service)
        data = mock_data_service.get_sales_trends()
        result = chart_service.create_trends_chart(data)
        assert isinstance(result, dict)

    def test_trends_chart_has_data(self, mock_data_service):
        """Test that trends chart has data property."""
        chart_service = ChartService(mock_data_service)
        data = mock_data_service.get_sales_trends()
        result = chart_service.create_trends_chart(data)
        assert 'data' in result


class TestProfitChart:
    """Tests for create_profit_chart method."""

    def test_profit_chart_returns_dict(self, mock_data_service):
        """Test that profit chart returns a dictionary."""
        chart_service = ChartService(mock_data_service)
        data = mock_data_service.get_profit_analysis()
        result = chart_service.create_profit_chart(data)
        assert isinstance(result, dict)

    def test_profit_chart_has_data(self, mock_data_service):
        """Test that profit chart has data property."""
        chart_service = ChartService(mock_data_service)
        data = mock_data_service.get_profit_analysis()
        result = chart_service.create_profit_chart(data)
        assert 'data' in result


class TestSegmentChart:
    """Tests for create_segment_chart method."""

    def test_segment_chart_returns_dict(self, mock_data_service):
        """Test that segment chart returns a dictionary."""
        chart_service = ChartService(mock_data_service)
        data = mock_data_service.get_segment_analysis()
        result = chart_service.create_segment_chart(data)
        assert isinstance(result, dict)

    def test_segment_chart_has_data(self, mock_data_service):
        """Test that segment chart has data property."""
        chart_service = ChartService(mock_data_service)
        data = mock_data_service.get_segment_analysis()
        result = chart_service.create_segment_chart(data)
        assert 'data' in result
