import { useFetch } from "../hooks/useFetch";
import { FilterState, OverviewMetrics } from "../types/api";
import MetricCard from "./MetricCard";

interface Props {
  filters: FilterState;
}

export default function Overview({ filters }: Props) {
  const { data, loading, error } = useFetch<OverviewMetrics>(
    "/api/sales/overview",
    {
      params: {
        start_date: filters.start_date,
        end_date: filters.end_date,
        regions: filters.regions,
        segments: filters.segments,
        categories: filters.categories,
      },
    }
  );

  if (loading) {
    return <div className="loading">Loading overview metrics...</div>;
  }

  if (error) {
    return <div className="error">Error loading overview: {error}</div>;
  }

  if (!data) {
    return null;
  }

  return (
    <div className="dashboard-grid">
      <MetricCard
        title="Total Sales"
        value={data.total_sales}
        format="currency"
      />
      <MetricCard
        title="Total Profit"
        value={data.total_profit}
        format="currency"
      />
      <MetricCard title="Total Orders" value={data.total_orders} />
      <MetricCard title="Total Customers" value={data.total_customers} />
      <MetricCard
        title="Avg Order Value"
        value={data.avg_order_value}
        format="currency"
      />
      <MetricCard
        title="Profit Margin"
        value={data.profit_margin}
        format="percent"
      />
    </div>
  );
}
