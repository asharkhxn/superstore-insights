import { useFetch } from "../hooks/useFetch";
import { ChartResponse, FilterState, ProfitData } from "../types/api";
import Chart from "./Chart";

interface Props {
  filters: FilterState;
}

export default function ProfitChart({ filters }: Props) {
  const { data, loading, error, refreshing, retry } = useFetch<
    ChartResponse<ProfitData>
  >("/api/sales/profit-analysis", {
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
        <h2>Profit Analysis</h2>
        <Chart
          chart={data?.chart || { data: [], layout: {} }}
          loading={loading}
          refreshing={refreshing}
          error={error}
          onRetry={retry}
        />
      </div>
    </div>
  );
}
