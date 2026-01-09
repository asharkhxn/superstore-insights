import { useFetch } from "../hooks/useFetch";
import { ChartResponse, FilterState, RegionData } from "../types/api";
import Chart from "./Chart";

interface Props {
  filters: FilterState;
}

export default function RegionChart({ filters }: Props) {
  const { data, loading, error, refreshing, retry } = useFetch<
    ChartResponse<RegionData>
  >("/api/sales/by-region", {
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
        <h2>Sales by Region</h2>
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
