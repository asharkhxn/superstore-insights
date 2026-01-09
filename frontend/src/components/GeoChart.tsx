import { useFetch } from "../hooks/useFetch";
import { ChartResponse, StateData, FilterState } from "../types/api";
import Chart from "./Chart";

interface Props {
  filters: FilterState;
}

export default function GeoChart({ filters }: Props) {
  const { data, loading, error, refreshing, retry } = useFetch<
    ChartResponse<StateData[]>
  >("/api/sales/geo-sales", {
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
      <div className="chart-card chart-geo">
        <h2>Geographic Sales Distribution</h2>
        <p className="chart-subtitle">
          Sales performance across US states — hover for details
        </p>
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
