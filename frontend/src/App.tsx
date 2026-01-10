import { useState } from "react";
import Overview from "./components/Overview";
import CategoryChart from "./components/CategoryChart";
import RegionChart from "./components/RegionChart";
import TrendsChart from "./components/TrendsChart";
import ProfitChart from "./components/ProfitChart";
import SegmentChart from "./components/SegmentChart";
import GeoChart from "./components/GeoChart";
import FilterBar from "./components/FilterBar";
import { FilterState } from "./types/api";

function formatDateRange(filters: FilterState): string {
  const { start_date, end_date } = filters;

  if (start_date && end_date) {
    const start = new Date(start_date);
    const end = new Date(end_date);
    const opts: Intl.DateTimeFormatOptions = {
      month: "short",
      year: "numeric",
    };
    return `${start.toLocaleDateString(
      "en-US",
      opts
    )} – ${end.toLocaleDateString("en-US", opts)}`;
  }
  if (start_date) {
    const start = new Date(start_date);
    return `From ${start.toLocaleDateString("en-US", {
      month: "short",
      year: "numeric",
    })}`;
  }
  if (end_date) {
    const end = new Date(end_date);
    return `Until ${end.toLocaleDateString("en-US", {
      month: "short",
      year: "numeric",
    })}`;
  }
  return "Jan 2014 – Dec 2017";
}

function getActiveFiltersSummary(filters: FilterState): string[] {
  const summary: string[] = [];
  if (filters.regions.length > 0) {
    summary.push(
      filters.regions.length === 1
        ? filters.regions[0]
        : `${filters.regions.length} Regions`
    );
  }
  if (filters.segments.length > 0) {
    summary.push(
      filters.segments.length === 1
        ? filters.segments[0]
        : `${filters.segments.length} Segments`
    );
  }
  if (filters.categories.length > 0) {
    summary.push(
      filters.categories.length === 1
        ? filters.categories[0]
        : `${filters.categories.length} Categories`
    );
  }
  return summary;
}

function hasActiveFilters(filters: FilterState): boolean {
  return !!(
    filters.start_date ||
    filters.end_date ||
    filters.regions.length > 0 ||
    filters.segments.length > 0 ||
    filters.categories.length > 0
  );
}

const defaultFilters: FilterState = {
  start_date: undefined,
  end_date: undefined,
  regions: [],
  segments: [],
  categories: [],
};

function App() {
  const [filters, setFilters] = useState<FilterState>(defaultFilters);
  const [showFilters, setShowFilters] = useState(true);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const [visible, setVisible] = useState({
    category: true,
    region: true,
    trends: true,
    profit: true,
    segment: true,
    geo: true,
  });

  const filterSummary = getActiveFiltersSummary(filters);
  const filtersActive = hasActiveFilters(filters);

  const clearAllFilters = () => {
    setFilters(defaultFilters);
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <div className="logo">
            <svg
              viewBox="0 0 32 32"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <rect width="32" height="32" rx="8" fill="url(#logo-gradient)" />
              <path
                d="M8 16L12 12L16 16L20 12L24 16"
                stroke="white"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M8 20L12 16L16 20L20 16L24 20"
                stroke="white"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                opacity="0.6"
              />
              <defs>
                <linearGradient
                  id="logo-gradient"
                  x1="0"
                  y1="0"
                  x2="32"
                  y2="32"
                  gradientUnits="userSpaceOnUse"
                >
                  <stop stopColor="#0176d3" />
                  <stop offset="1" stopColor="#032d60" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1>Superstore Insights</h1>
          <span className="badge">Live</span>
        </div>
        <div className="header-right">
          <button
            type="button"
            className="filter-toggle"
            onClick={() => setShowFilters(!showFilters)}
          >
            {showFilters ? "Hide Filters" : "Show Filters"}
          </button>
        </div>
      </header>

      {/* Filters (collapsible) */}
      {showFilters && (
        <section className="filters-section">
          <FilterBar filters={filters} onChange={setFilters} />
        </section>
      )}

      {/* Data Context Bar - Shows what data user is viewing (only when filters active) */}
      {filtersActive && (
        <div className="data-context-bar">
          <div className="context-left">
            <span className="context-label">Filtered View:</span>
            <span className="context-period">{formatDateRange(filters)}</span>
            {filterSummary.length > 0 && (
              <>
                <span className="context-separator">•</span>
                <span className="context-filters">
                  {filterSummary.join(", ")}
                </span>
              </>
            )}
          </div>
          <button
            type="button"
            className="clear-filters-btn"
            onClick={clearAllFilters}
          >
            ✕ Clear All Filters
          </button>
        </div>
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
              <button
                type="button"
                className={`chip ${visible.geo ? "chip-on" : ""}`}
                onClick={() => setVisible((v) => ({ ...v, geo: !v.geo }))}
              >
                Map
              </button>
            </>
          )}
        </div>
      </section>

      {/* Show message if no dates selected */}
      {!filters.start_date || !filters.end_date ? (
        <section className="no-data-message">
          <div className="no-data-icon">📊</div>
          <h2>Select a Date Range to View Data</h2>
          <p>
            Choose a time period using the Quick Select buttons or Custom Date
            Range above to see your analytics.
          </p>
          <div className="no-data-hint">
            <span>💡</span>
            <span>Tip: Click "2017" or "All Time" to quickly load data</span>
          </div>
        </section>
      ) : (
        <>
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
                {visible.geo && (
                  <div className="chart-wrapper wide">
                    <GeoChart filters={filters} />
                  </div>
                )}
              </>
            )}
          </section>
        </>
      )}
    </div>
  );
}

export default App;
