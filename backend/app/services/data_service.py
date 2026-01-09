"""Data service for loading and processing Superstore data."""
import pandas as pd
import pyarrow as pa
import requests
from io import BytesIO
from typing import Dict, List, Any, Optional
from functools import lru_cache
from datetime import datetime


class DataService:
    """Service for loading and analyzing Superstore sales data."""

    ARROW_URL = "https://raw.githubusercontent.com/texodus/superstore-arrow/master/superstore.arrow"
    
    # Required schema for validation
    REQUIRED_COLUMNS = [
        'Order Date', 'Ship Date', 'Sales', 'Profit', 'Quantity', 
        'Discount', 'Order ID', 'Customer ID', 'Customer Name',
        'Segment', 'Region', 'Category', 'Sub-Category', 'Product Name'
    ]

    def __init__(self):
        """Initialize the data service."""
        self._df = None
        self._last_refresh = None

    @property
    def df(self) -> pd.DataFrame:
        """Lazy load the dataframe."""
        if self._df is None:
            self._df = self._load_data()
            self._last_refresh = datetime.now()
        return self._df
    
    @property
    def last_refresh(self) -> Optional[datetime]:
        """Get last refresh timestamp."""
        return self._last_refresh

    def _load_data(self) -> pd.DataFrame:
        """Load data from the Arrow file with validation."""
        try:
            response = requests.get(self.ARROW_URL, timeout=30)
            response.raise_for_status()
            
            # Try reading as Feather format (Arrow IPC file format)
            try:
                df = pd.read_feather(BytesIO(response.content))
            except Exception:
                # Fallback to IPC stream reader
                reader = pa.ipc.open_stream(BytesIO(response.content))
                table = reader.read_all()
                df = table.to_pandas()
            
            # Validate schema
            missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Convert date columns
            df['Order Date'] = pd.to_datetime(df['Order Date'])
            df['Ship Date'] = pd.to_datetime(df['Ship Date'])
            
            # Ensure numeric types
            for col in ['Sales', 'Profit', 'Quantity', 'Discount']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
        except Exception as e:
            raise RuntimeError(f"Failed to load data: {str(e)}")
    
    def _apply_filters(
        self, 
        df: pd.DataFrame,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Apply global filters to dataframe."""
        filtered = df.copy()
        
        # Date range filter
        if start_date:
            filtered = filtered[filtered['Order Date'] >= pd.to_datetime(start_date)]
        if end_date:
            filtered = filtered[filtered['Order Date'] <= pd.to_datetime(end_date)]
        
        # Region filter
        if regions and len(regions) > 0:
            filtered = filtered[filtered['Region'].isin(regions)]
        
        # Segment filter
        if segments and len(segments) > 0:
            filtered = filtered[filtered['Segment'].isin(segments)]
        
        # Category filter
        if categories and len(categories) > 0:
            filtered = filtered[filtered['Category'].isin(categories)]
        
        return filtered

    def get_overview_metrics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get high-level sales metrics with optional filters."""
        df = self._apply_filters(
            self.df, start_date, end_date, regions, segments, categories
        )
        
        total_sales = float(df['Sales'].sum())
        total_profit = float(df['Profit'].sum())
        unique_orders = df['Order ID'].nunique()
        
        return {
            "total_sales": round(total_sales, 2),
            "total_profit": round(total_profit, 2),
            "total_orders": int(unique_orders),
            "total_customers": int(df['Customer ID'].nunique()),
            "avg_order_value": round(total_sales / unique_orders, 2) if unique_orders > 0 else 0.0,
            "profit_margin": round(total_profit / total_sales * 100, 2) if total_sales > 0 else 0.0,
        }

    def get_sales_by_category(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get sales grouped by category with optional filters."""
        df = self._apply_filters(
            self.df, start_date, end_date, regions, segments, categories
        )
        grouped = df.groupby('Category').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum',
            'Order ID': 'nunique'
        }).reset_index()
        grouped.columns = ['category', 'sales', 'profit', 'quantity', 'orders']
        grouped = grouped.round({'sales': 2, 'profit': 2})
        return grouped.to_dict('records')

    def get_sales_by_region(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get sales grouped by region with optional filters."""
        df = self._apply_filters(
            self.df, start_date, end_date, regions, segments, categories
        )
        grouped = df.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum',
            'Order ID': 'nunique'
        }).reset_index()
        grouped.columns = ['region', 'sales', 'profit', 'quantity', 'orders']
        grouped = grouped.round({'sales': 2, 'profit': 2})
        return grouped.to_dict('records')

    def get_sales_trends(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get monthly sales trends with optional filters."""
        df = self._apply_filters(
            self.df, start_date, end_date, regions, segments, categories
        )
        df = df.copy()
        df['Month'] = df['Order Date'].dt.to_period('M')
        grouped = df.groupby('Month').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique'
        }).reset_index()
        grouped['Month'] = grouped['Month'].astype(str)
        grouped.columns = ['month', 'sales', 'profit', 'orders']
        grouped = grouped.round({'sales': 2, 'profit': 2})
        return grouped.to_dict('records')

    def get_profit_analysis(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get profit analysis by sub-category with optional filters."""
        df = self._apply_filters(
            self.df, start_date, end_date, regions, segments, categories
        )
        
        # Check if required columns exist
        required_cols = ['Category', 'Sub-Category', 'Sales', 'Profit', 'Quantity']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        grouped = df.groupby(['Category', 'Sub-Category']).agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        
        # Calculate profit margin, handling division by zero
        profit_margin = []
        for _, row in grouped.iterrows():
            if row['Sales'] != 0:
                margin = round((row['Profit'] / row['Sales'] * 100), 2)
            else:
                margin = 0.0
            profit_margin.append(margin)
        
        # Create result dictionary
        result = {
            'category': grouped['Category'].astype(str).tolist(),
            'sub_category': grouped['Sub-Category'].astype(str).tolist(),
            'sales': grouped['Sales'].round(2).tolist(),
            'profit': grouped['Profit'].round(2).tolist(),
            'quantity': grouped['Quantity'].astype(int).tolist(),
            'profit_margin': profit_margin
        }
        
        # Convert to list of dicts
        records = []
        for i in range(len(result['category'])):
            records.append({
                'category': result['category'][i],
                'sub_category': result['sub_category'][i],
                'sales': result['sales'][i],
                'profit': result['profit'][i],
                'quantity': result['quantity'][i],
                'profit_margin': result['profit_margin'][i]
            })
        
        return records

    def get_segment_analysis(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        regions: Optional[List[str]] = None,
        segments: Optional[List[str]] = None,
        categories: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get sales analysis by customer segment with optional filters."""
        df = self._apply_filters(
            self.df, start_date, end_date, regions, segments, categories
        )
        grouped = df.groupby('Segment').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Customer ID': 'nunique',
            'Order ID': 'nunique'
        }).reset_index()
        grouped.columns = ['segment', 'sales', 'profit', 'customers', 'orders']
        grouped = grouped.round({'sales': 2, 'profit': 2})
        return grouped.to_dict('records')
    
    def get_filter_options(self) -> Dict[str, Any]:
        """Get available filter options from the dataset."""
        df = self.df
        
        # Get unique values for each filter
        regions = sorted(df['Region'].unique().tolist())
        segments = sorted(df['Segment'].unique().tolist())
        categories = sorted(df['Category'].unique().tolist())
        
        # Get date range
        min_date = df['Order Date'].min().strftime('%Y-%m-%d')
        max_date = df['Order Date'].max().strftime('%Y-%m-%d')
        
        return {
            "regions": regions,
            "segments": segments,
            "categories": categories,
            "date_range": {
                "min": min_date,
                "max": max_date
            }
        }
