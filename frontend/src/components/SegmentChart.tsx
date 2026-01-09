import { useFetch } from "../hooks/useFetch";
import { ChartResponse, FilterState, SegmentData } from "../types/api";
import Chart from "./Chart";

interface Props {
  filters: FilterState;
}

export default function SegmentChart({ filters }: Props) {
  const { data, loading, error, refreshing, retry } = useFetch<
    ChartResponse<SegmentData>
  >("/api/sales/segment-analysis", {
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
        <h2>Customer Segment Analysis</h2>
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
