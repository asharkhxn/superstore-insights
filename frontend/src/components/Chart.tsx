import Plot from "react-plotly.js";
import { PlotlyChart } from "../types/api";
import { ApiError } from "../hooks/useFetch";

interface ChartProps {
  chart: PlotlyChart;
  loading?: boolean;
  refreshing?: boolean;
  error?: ApiError | null;
  onRetry?: () => void;
}

export default function Chart({
  chart,
  loading,
  refreshing,
  error,
  onRetry,
}: ChartProps) {
  if (loading) {
    return (
      <div className="chart-loading">
        <div className="loading-spinner"></div>
        <p>Loading chart...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="chart-error">
        <div className="error-icon">
          {error.type === "network"
            ? "📡"
            : error.type === "server"
            ? "🖥️"
            : "⚠️"}
        </div>
        <h3>
          {error.type === "network"
            ? "Connection Error"
            : error.type === "server"
            ? "Server Error"
            : "Unable to Load Chart"}
        </h3>
        <p className="error-message">{error.message}</p>
        {error.isRetryable && onRetry && (
          <button type="button" className="retry-btn" onClick={onRetry}>
            ↻ Try Again
          </button>
        )}
        {error.code && (
          <span className="error-code">Error Code: {error.code}</span>
        )}
      </div>
    );
  }

  if (!chart || !chart.data) {
    return null;
  }

  return (
    <div className="chart-container">
      {refreshing && <div className="soft-refresh">Updating…</div>}
      <Plot
        data={chart.data}
        layout={{
          ...chart.layout,
          autosize: true,
          responsive: true,
          dragmode: false,
        }}
        useResizeHandler={true}
        style={{ width: "100%", height: "100%", minHeight: 320 }}
        config={{
          displayModeBar: true,
          displaylogo: false,
          responsive: true,
          scrollZoom: false,
          doubleClick: false,
          modeBarButtonsToRemove: [
            "select2d",
            "lasso2d",
            "pan2d",
            "zoom2d",
            "zoomIn2d",
            "zoomOut2d",
            "autoScale2d",
            "resetScale2d",
            "toggleSpikelines",
          ],
        }}
      />
    </div>
  );
}
