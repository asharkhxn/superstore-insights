"""Shared pytest fixtures."""
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from app.services.data_service import DataService
from app.services.repository import DataRepository


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        "Row ID": [1, 2, 3, 4, 5],
        "Order ID": ["ORD-001", "ORD-001", "ORD-002", "ORD-003", "ORD-003"],
        "Order Date": [
            datetime(2023, 1, 15),
            datetime(2023, 1, 15),
            datetime(2023, 2, 20),
            datetime(2023, 3, 10),
            datetime(2023, 3, 10),
        ],
        "Ship Date": [
            datetime(2023, 1, 20),
            datetime(2023, 1, 20),
            datetime(2023, 2, 25),
            datetime(2023, 3, 15),
            datetime(2023, 3, 15),
        ],
        "Ship Mode": ["Standard", "Standard", "Express", "Standard", "Standard"],
        "Customer ID": ["CUST-001", "CUST-001", "CUST-002", "CUST-003", "CUST-003"],
        "Customer Name": ["John Doe", "John Doe", "Jane Smith", "Bob Wilson", "Bob Wilson"],
        "Segment": ["Consumer", "Consumer", "Corporate", "Home Office", "Home Office"],
        "Country": ["USA", "USA", "USA", "USA", "USA"],
        "City": ["New York", "New York", "Los Angeles", "Chicago", "Chicago"],
        "State": ["New York", "New York", "California", "Illinois", "Illinois"],
        "Postal Code": [10001, 10001, 90001, 60601, 60601],
        "Region": ["East", "East", "West", "Central", "Central"],
        "Product ID": ["PROD-001", "PROD-002", "PROD-003", "PROD-004", "PROD-005"],
        "Category": ["Technology", "Office Supplies", "Furniture", "Technology", "Office Supplies"],
        "Sub-Category": ["Phones", "Paper", "Chairs", "Computers", "Binders"],
        "Product Name": ["iPhone", "A4 Paper", "Office Chair", "Laptop", "Ring Binder"],
        "Sales": [500.0, 50.0, 300.0, 1000.0, 25.0],
        "Quantity": [1, 5, 1, 1, 10],
        "Discount": [0.0, 0.1, 0.2, 0.0, 0.15],
        "Profit": [100.0, 10.0, -20.0, 200.0, 5.0],
    })


@pytest.fixture
def mock_repository(sample_dataframe):
    """Create a mocked DataRepository with sample data."""
    mock_repo = MagicMock(spec=DataRepository)
    mock_repo.get_dataframe.return_value = sample_dataframe
    mock_repo.last_refresh = datetime.now()
    return mock_repo


@pytest.fixture
def mock_data_service(sample_dataframe, mock_repository):
    """Create a DataService with mocked repository."""
    service = DataService(repository=mock_repository)
    service._df = sample_dataframe
    return service
