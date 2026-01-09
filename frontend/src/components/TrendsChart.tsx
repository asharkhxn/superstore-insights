import { useFetch } from "../hooks/useFetch";
import { ChartResponse, FilterState, TrendData } from "../types/api";
import Chart from "./Chart";

interface Props {
  filters: FilterState;
}

export default function TrendsChart({ filters }: Props) {
  const { data, loading, error, refreshing } = useFetch<
    ChartResponse<TrendData>
  >("/api/sales/trends", {
    params: {
      start_date: filters.start_date,
      end_date: filters.end_date,
      regions: filters.regions,
      segments: filters.segments,
      categories: filters.categories,
    },
  });

  return (
    <div className="chart-section">
      <div className="chart-card">
        <h2>Sales Trends</h2>
        <Chart
          chart={data?.chart || { data: [], layout: {} }}
          loading={loading}
          refreshing={refreshing}
          error={error}
        />
      </div>
    </div>
  );
}
