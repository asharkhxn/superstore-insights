import { useState } from "react";
import Overview from "./components/Overview";
import CategoryChart from "./components/CategoryChart";
import RegionChart from "./components/RegionChart";
import TrendsChart from "./components/TrendsChart";
import ProfitChart from "./components/ProfitChart";
import SegmentChart from "./components/SegmentChart";
import FilterBar from "./components/FilterBar";
import { FilterState } from "./types/api";

function App() {
  const [filters, setFilters] = useState<FilterState>({
    start_date: undefined,
    end_date: undefined,
    regions: [],
    segments: [],
    categories: [],
  });
  const [showFilters, setShowFilters] = useState(true);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const [visible, setVisible] = useState({
    category: true,
    region: true,
    trends: true,
    profit: true,
    segment: true,
  });

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <h1>Superstore Insights</h1>
          <span className="badge">Live</span>
        </div>
        <button
          type="button"
          className="filter-toggle"
          onClick={() => setShowFilters(!showFilters)}
        >
          {showFilters ? "Hide Filters" : "Filters"}
        </button>
      </header>

      {/* Filters (collapsible) */}
      {showFilters && (
        <section className="filters-section">
          <FilterBar filters={filters} onChange={setFilters} />
        </section>
      )}

      {/* Chart toggles */}
      <section className="chart-toolbar">
        <div className="chart-toolbar-left">
          <span className="toolbar-label">Charts</span>
          <button
            type="button"
            className={`segmented ${showAdvanced ? "" : "segmented-active"}`}
            onClick={() => setShowAdvanced(false)}
          >
            Core
          </button>
          <button
            type="button"
            className={`segmented ${showAdvanced ? "segmented-active" : ""}`}
            onClick={() => setShowAdvanced(true)}
          >
            Advanced
          </button>
        </div>

        <div className="chart-toolbar-right">
          {!showAdvanced ? (
            <>
              <button
                type="button"
                className={`chip ${visible.category ? "chip-on" : ""}`}
                onClick={() =>
                  setVisible((v) => ({ ...v, category: !v.category }))
                }
              >
                Category
              </button>
              <button
                type="button"
                className={`chip ${visible.region ? "chip-on" : ""}`}
                onClick={() => setVisible((v) => ({ ...v, region: !v.region }))}
              >
                Region
              </button>
              <button
                type="button"
                className={`chip ${visible.trends ? "chip-on" : ""}`}
                onClick={() => setVisible((v) => ({ ...v, trends: !v.trends }))}
              >
                Trends
              </button>
            </>
          ) : (
            <>
              <button
                type="button"
                className={`chip ${visible.profit ? "chip-on" : ""}`}
                onClick={() => setVisible((v) => ({ ...v, profit: !v.profit }))}
              >
                Profit
              </button>
              <button
                type="button"
                className={`chip ${visible.segment ? "chip-on" : ""}`}
                onClick={() =>
                  setVisible((v) => ({ ...v, segment: !v.segment }))
                }
              >
                Segment
              </button>
            </>
          )}
        </div>
      </section>

      {/* KPI Cards */}
      <section className="kpi-section">
        <Overview filters={filters} />
      </section>

      {/* Charts */}
      <section className="charts-section">
        {!showAdvanced ? (
          <>
            {visible.category && (
              <div className="chart-wrapper">
                <CategoryChart filters={filters} />
              </div>
            )}
            {visible.region && (
              <div className="chart-wrapper">
                <RegionChart filters={filters} />
              </div>
            )}
            {visible.trends && (
              <div className="chart-wrapper wide">
                <TrendsChart filters={filters} />
              </div>
            )}
          </>
        ) : (
          <>
            {visible.profit && (
              <div className="chart-wrapper">
                <ProfitChart filters={filters} />
              </div>
            )}
            {visible.segment && (
              <div className="chart-wrapper">
                <SegmentChart filters={filters} />
              </div>
            )}
          </>
        )}
      </section>
    </div>
  );
}

export default App;
