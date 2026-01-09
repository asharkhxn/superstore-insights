"""Data repository for loading Superstore data."""
import logging
from datetime import datetime, timezone
from io import BytesIO
from typing import Optional

import pandas as pd
import pyarrow as pa
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class DataLoadError(Exception):
    """Raised when data cannot be loaded from source."""
    pass


class DataValidationError(Exception):
    """Raised when data fails validation."""
    pass


class DataRepository:
    """Load and cache the Superstore dataset."""

    REQUIRED_COLUMNS = (
        "Order Date", "Ship Date", "Sales", "Profit", "Quantity",
        "Discount", "Order ID", "Customer ID", "Customer Name",
        "Segment", "Region", "Category", "Sub-Category", "Product Name",
    )

    def __init__(self) -> None:
        """Initialize the repository."""
        self._settings = get_settings()
        self._df: Optional[pd.DataFrame] = None
        self._last_refresh: Optional[datetime] = None
        self._session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    @property
    def last_refresh(self) -> Optional[datetime]:
        """Get last refresh timestamp."""
        return self._last_refresh

    def get_dataframe(self, *, force_refresh: bool = False) -> pd.DataFrame:
        """Return the dataframe, loading if necessary."""
        if force_refresh or self._df is None:
            self._df = self._load()
            self._last_refresh = datetime.now(timezone.utc)
        return self._df

    def _load(self) -> pd.DataFrame:
        """Load data from the Arrow file."""
        url = self._settings.data_source_url
        logger.info(f"Loading data from {url}")
        
        try:
            response = self._session.get(
                url,
                timeout=self._settings.request_timeout_seconds,
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise DataLoadError(
                "Unable to connect to data source. Please check your internet connection."
            ) from e
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout: {e}")
            raise DataLoadError(
                "Data source request timed out. Please try again later."
            ) from e
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise DataLoadError(
                f"Data source returned an error (HTTP {response.status_code}). Please try again later."
            ) from e
        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            raise DataLoadError(f"Failed to load data: {e}") from e

        try:
            df = self._read_arrow(BytesIO(response.content))
        except Exception as e:
            logger.error(f"Failed to parse Arrow data: {e}")
            raise DataLoadError(
                "Failed to parse data file. The data source may be corrupted."
            ) from e

        try:
            self._validate_schema(df)
        except ValueError as e:
            logger.error(f"Schema validation failed: {e}")
            raise DataValidationError(str(e)) from e

        self._coerce_types(df)
        self._clean_data(df)
        
        logger.info(f"Successfully loaded {len(df)} records")
        return df

    def _read_arrow(self, payload: BytesIO) -> pd.DataFrame:
        """Read Arrow file with fallback to IPC stream."""
        try:
            payload.seek(0)
            return pd.read_feather(payload)
        except Exception:
            payload.seek(0)
            reader = pa.ipc.open_stream(payload)
            return reader.read_all().to_pandas()

    def _validate_schema(self, df: pd.DataFrame) -> None:
        """Validate required columns exist."""
        missing = [c for c in self.REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    def _coerce_types(self, df: pd.DataFrame) -> None:
        """Convert columns to proper types."""
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
        for col in ["Sales", "Profit", "Quantity", "Discount"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    def _clean_data(self, df: pd.DataFrame) -> None:
        """Clean and validate data values."""
        # Fill NaN values with defaults
        df["Sales"] = df["Sales"].fillna(0)
        df["Profit"] = df["Profit"].fillna(0)
        df["Quantity"] = df["Quantity"].fillna(0)
        df["Discount"] = df["Discount"].fillna(0)
        
        # Remove rows with invalid dates
        initial_count = len(df)
        df.dropna(subset=["Order Date"], inplace=True)
        if len(df) < initial_count:
            logger.warning(f"Dropped {initial_count - len(df)} rows with invalid dates")
