export interface OverviewMetrics {
  total_sales: number;
  total_profit: number;
  total_orders: number;
  total_customers: number;
  avg_order_value: number;
  profit_margin: number;
}

export interface CategoryData {
  category: string;
  sales: number;
  profit: number;
  quantity: number;
  orders: number;
}

export interface RegionData {
  region: string;
  sales: number;
  profit: number;
  quantity: number;
  orders: number;
}

export interface TrendData {
  month: string;
  sales: number;
  profit: number;
  orders: number;
}

export interface ProfitData {
  category: string;
  sub_category: string;
  sales: number;
  profit: number;
  quantity: number;
  profit_margin: number;
}

export interface SegmentData {
  segment: string;
  sales: number;
  profit: number;
  customers: number;
  orders: number;
}

export interface StateData {
  state: string;
  state_code: string;
  sales: number;
  profit: number;
  orders: number;
}

export interface ChartResponse<T> {
  data: T[] | T;
  chart: PlotlyChart;
}

export interface PlotlyChart {
  data: any[];
  layout: any;
  [key: string]: any;
}

export interface FilterOptions {
  regions: string[];
  segments: string[];
  categories: string[];
  date_range: {
    min: string;
    max: string;
  };
}

export interface FilterState {
  start_date?: string;
  end_date?: string;
  regions: string[];
  segments: string[];
  categories: string[];
}
