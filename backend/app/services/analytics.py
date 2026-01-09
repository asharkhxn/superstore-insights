"""Analytics functions for computing sales metrics."""
from typing import Any, Dict, List

import pandas as pd


def compute_overview_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute high-level sales metrics from dataframe.
    
    Args:
        df: Filtered sales dataframe
        
    Returns:
        Dictionary with overview metrics
    """
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    unique_orders = df["Order ID"].nunique()
    
    return {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "total_orders": int(unique_orders),
        "total_customers": int(df["Customer ID"].nunique()),
        "avg_order_value": round(total_sales / unique_orders, 2) if unique_orders > 0 else 0.0,
        "profit_margin": round(total_profit / total_sales * 100, 2) if total_sales > 0 else 0.0,
    }


def compute_sales_by_category(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Compute sales grouped by category.
    
    Args:
        df: Filtered sales dataframe
        
    Returns:
        List of category sales records
    """
    grouped = df.groupby("Category").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Order ID": "nunique",
    }).reset_index()
    grouped.columns = ["category", "sales", "profit", "quantity", "orders"]
    grouped = grouped.round({"sales": 2, "profit": 2})
    return grouped.to_dict("records")


def compute_sales_by_region(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Compute sales grouped by region.
    
    Args:
        df: Filtered sales dataframe
        
    Returns:
        List of region sales records
    """
    grouped = df.groupby("Region").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Order ID": "nunique",
    }).reset_index()
    grouped.columns = ["region", "sales", "profit", "quantity", "orders"]
    grouped = grouped.round({"sales": 2, "profit": 2})
    return grouped.to_dict("records")


def compute_sales_trends(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Compute monthly sales trends.
    
    Args:
        df: Filtered sales dataframe
        
    Returns:
        List of monthly trend records
    """
    df_copy = df.copy()
    df_copy["Month"] = df_copy["Order Date"].dt.to_period("M")
    grouped = df_copy.groupby("Month").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique",
    }).reset_index()
    grouped["Month"] = grouped["Month"].astype(str)
    grouped.columns = ["month", "sales", "profit", "orders"]
    grouped = grouped.round({"sales": 2, "profit": 2})
    return grouped.to_dict("records")


def compute_profit_analysis(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Compute profit analysis by sub-category.
    
    Args:
        df: Filtered sales dataframe
        
    Returns:
        List of profit analysis records
    """
    grouped = df.groupby(["Category", "Sub-Category"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
    }).reset_index()
    
    records = []
    for _, row in grouped.iterrows():
        sales = row["Sales"]
        profit = row["Profit"]
        margin = round((profit / sales * 100), 2) if sales != 0 else 0.0
        
        records.append({
            "category": str(row["Category"]),
            "sub_category": str(row["Sub-Category"]),
            "sales": round(sales, 2),
            "profit": round(profit, 2),
            "quantity": int(row["Quantity"]),
            "profit_margin": margin,
        })
    
    return records


def compute_segment_analysis(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Compute sales analysis by customer segment.
    
    Args:
        df: Filtered sales dataframe
        
    Returns:
        List of segment analysis records
    """
    grouped = df.groupby("Segment").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Customer ID": "nunique",
        "Order ID": "nunique",
    }).reset_index()
    grouped.columns = ["segment", "sales", "profit", "customers", "orders"]
    grouped = grouped.round({"sales": 2, "profit": 2})
    return grouped.to_dict("records")


def compute_filter_options(df: pd.DataFrame) -> Dict[str, Any]:
    """Get available filter options from the dataset.
    
    Args:
        df: Full sales dataframe
        
    Returns:
        Dictionary with filter options
    """
    return {
        "regions": sorted(df["Region"].unique().tolist()),
        "segments": sorted(df["Segment"].unique().tolist()),
        "categories": sorted(df["Category"].unique().tolist()),
        "date_range": {
            "min": df["Order Date"].min().strftime("%Y-%m-%d"),
            "max": df["Order Date"].max().strftime("%Y-%m-%d"),
        },
    }


def compute_state_sales(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Compute sales aggregated by state for choropleth map.
    
    Args:
        df: Filtered sales dataframe
        
    Returns:
        List of state sales records with state codes
    """
    # State name to abbreviation mapping
    state_abbrev = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
        "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
        "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
        "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
        "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
        "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
        "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
        "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
        "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
        "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
    }
    
    grouped = df.groupby("State", observed=True).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique",
    }).reset_index()
    
    records = []
    for _, row in grouped.iterrows():
        state_name = str(row["State"])
        state_code = state_abbrev.get(state_name, "")
        if state_code:
            records.append({
                "state": state_name,
                "state_code": state_code,
                "sales": round(float(row["Sales"]), 2),
                "profit": round(float(row["Profit"]), 2),
                "orders": int(row["Order ID"]),
            })
    
    return records
