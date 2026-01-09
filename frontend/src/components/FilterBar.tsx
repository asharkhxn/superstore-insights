import { useFetch } from "../hooks/useFetch";
import { FilterOptions, FilterState } from "../types/api";

interface FilterBarProps {
  filters: FilterState;
  onChange: (next: FilterState) => void;
}

type MultiKey = "regions" | "segments" | "categories";

const formatDateInput = (value?: string) => (value ? value.slice(0, 10) : "");

// Date preset options
const datePresets = [
  { label: "2014", start: "2014-01-01", end: "2014-12-31" },
  { label: "2015", start: "2015-01-01", end: "2015-12-31" },
  { label: "2016", start: "2016-01-01", end: "2016-12-31" },
  { label: "2017", start: "2017-01-01", end: "2017-12-31" },
  { label: "All Time", start: "2014-01-03", end: "2017-12-30" },
];

export default function FilterBar({ filters, onChange }: FilterBarProps) {
  const { data, loading, error } = useFetch<FilterOptions>(
    "/api/sales/filter-options"
  );

  const toggleMulti = (key: MultiKey, value: string) => {
    const current = filters[key];
    const exists = current.includes(value);
    const next = exists
      ? current.filter((v) => v !== value)
      : [...current, value];
    onChange({ ...filters, [key]: next });
  };

  const applyDatePreset = (start: string, end: string) => {
    onChange({ ...filters, start_date: start, end_date: end });
  };

  const isPresetActive = (start: string, end: string) => {
    return filters.start_date === start && filters.end_date === end;
  };

  const renderPills = (items: string[], key: MultiKey) => (
    <div className="pill-row">
      {items.map((item) => {
        const selected = filters[key].includes(item);
        return (
          <button
            type="button"
            key={item}
            className={`pill ${selected ? "pill-active" : ""}`}
            onClick={() => toggleMulti(key, item)}
            title={selected ? `Remove ${item} filter` : `Filter by ${item}`}
          >
            {item}
          </button>
        );
      })}
    </div>
  );

  return (
    <div className="filter-bar">
      {/* Top Row: Date Controls */}
      <div className="filter-row filter-row-dates">
        <div className="filter-group">
          <p className="label">Quick Select</p>
          <div className="date-presets">
            {datePresets.map((preset) => (
              <button
                key={preset.label}
                type="button"
                className={`preset-btn ${
                  isPresetActive(preset.start, preset.end) ? "preset-active" : ""
                }`}
                onClick={() => applyDatePreset(preset.start, preset.end)}
              >
                {preset.label}
              </button>
            ))}
          </div>
        </div>

        <div className="filter-divider" />

        <div className="filter-group">
          <p className="label">Custom Range</p>
          <div className="date-row">
            <input
              type="date"
              value={formatDateInput(filters.start_date)}
              min={data?.date_range.min}
              max={filters.end_date || data?.date_range.max}
              onChange={(e) =>
                onChange({ ...filters, start_date: e.target.value || undefined })
              }
              placeholder="Start date"
            />
            <span className="dash">to</span>
            <input
              type="date"
              value={formatDateInput(filters.end_date)}
              min={filters.start_date || data?.date_range.min}
              max={data?.date_range.max}
              onChange={(e) =>
                onChange({ ...filters, end_date: e.target.value || undefined })
              }
              placeholder="End date"
            />
          </div>
        </div>
      </div>

      {/* Bottom Row: Dimension Filters */}
      <div className="filter-row filter-row-dimensions">
        <div className="filter-group">
          <p className="label">Regions</p>
          {data ? (
            renderPills(data.regions, "regions")
          ) : (
            <div className="skeleton" />
          )}
        </div>

        <div className="filter-divider" />

        <div className="filter-group">
          <p className="label">Segments</p>
          {data ? (
            renderPills(data.segments, "segments")
          ) : (
            <div className="skeleton" />
          )}
        </div>

        <div className="filter-divider" />

        <div className="filter-group">
          <p className="label">Categories</p>
          {data ? (
            renderPills(data.categories, "categories")
          ) : (
            <div className="skeleton" />
          )}
        </div>
      </div>

      {loading && (
        <div className="filter-loading">
          Loading filters...
        </div>
      )}
      {error && (
        <div className="filter-error">
          {error.message}
        </div>
      )}
    </div>
  );
}
