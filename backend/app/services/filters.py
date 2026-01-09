"""DataFrame filtering utilities."""
from typing import List, Optional

import pandas as pd


def apply_filters(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    regions: Optional[List[str]] = None,
    segments: Optional[List[str]] = None,
    categories: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Apply global filters to dataframe.
    
    Args:
        df: Source dataframe
        start_date: Filter orders on or after this date (YYYY-MM-DD)
        end_date: Filter orders on or before this date (YYYY-MM-DD)
        regions: List of regions to include
        segments: List of segments to include
        categories: List of categories to include
        
    Returns:
        Filtered copy of the dataframe
    """
    filtered = df.copy()
    
    if start_date:
        filtered = filtered[filtered["Order Date"] >= pd.to_datetime(start_date)]
    if end_date:
        filtered = filtered[filtered["Order Date"] <= pd.to_datetime(end_date)]
    if regions:
        filtered = filtered[filtered["Region"].isin(regions)]
    if segments:
        filtered = filtered[filtered["Segment"].isin(segments)]
    if categories:
        filtered = filtered[filtered["Category"].isin(categories)]
    
    return filtered
