"""Data repository for loading Superstore data."""
from datetime import datetime, timezone
from io import BytesIO
from typing import Optional

import pandas as pd
import pyarrow as pa
import requests

from app.core.config import get_settings


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
        try:
            response = requests.get(
                self._settings.data_source_url,
                timeout=self._settings.request_timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to load data: {e}") from e

        df = self._read_arrow(BytesIO(response.content))
        self._validate_schema(df)
        self._coerce_types(df)
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
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["Ship Date"] = pd.to_datetime(df["Ship Date"])
        for col in ["Sales", "Profit", "Quantity", "Discount"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
