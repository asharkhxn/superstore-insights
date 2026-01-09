import { useFetch, ApiError } from "../hooks/useFetch";
import { FilterState, OverviewMetrics } from "../types/api";
import MetricCard from "./MetricCard";

interface Props {
  filters: FilterState;
}

function OverviewError({
  error,
  onRetry,
}: {
  error: ApiError;
  onRetry: () => void;
}) {
  return (
    <div className="overview-error">
      <div className="error-content">
        <span className="error-icon">
          {error.type === "network"
            ? "📡"
            : error.type === "server"
            ? "🖥️"
            : "⚠️"}
        </span>
        <div className="error-details">
          <h3>
            {error.type === "network"
              ? "Connection Error"
              : error.type === "server"
              ? "Server Error"
              : "Unable to Load Metrics"}
          </h3>
          <p>{error.message}</p>
        </div>
        {error.isRetryable && (
          <button type="button" className="retry-btn" onClick={onRetry}>
            ↻ Retry
          </button>
        )}
      </div>
    </div>
  );
}

function OverviewLoading() {
  return (
    <div className="dashboard-grid">
      {[...Array(6)].map((_, i) => (
        <div key={i} className="metric-card skeleton">
          <div className="skeleton-title"></div>
          <div className="skeleton-value"></div>
        </div>
      ))}
    </div>
  );
}

export default function Overview({ filters }: Props) {
  const { data, loading, error, retry } = useFetch<OverviewMetrics>(
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
    return <OverviewLoading />;
  }

  if (error) {
    return <OverviewError error={error} onRetry={retry} />;
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
