import Plot from "react-plotly.js";
import { PlotlyChart } from "../types/api";

interface ChartProps {
  chart: PlotlyChart;
  loading?: boolean;
  refreshing?: boolean;
  error?: string | null;
}

export default function Chart({
  chart,
  loading,
  refreshing,
  error,
}: ChartProps) {
  if (loading) {
    return <div className="loading">Loading chart...</div>;
  }

  if (error) {
    return <div className="error">Error loading chart: {error}</div>;
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
