import { useEffect } from "react";
import { useFetch } from "../hooks/useFetch";
import { FilterOptions, FilterState } from "../types/api";

interface FilterBarProps {
  filters: FilterState;
  onChange: (next: FilterState) => void;
}

type MultiKey = "regions" | "segments" | "categories";

const formatDateInput = (value?: string) => (value ? value.slice(0, 10) : "");

export default function FilterBar({ filters, onChange }: FilterBarProps) {
  const { data, loading, error } = useFetch<FilterOptions>(
    "/api/sales/filter-options"
  );

  // Initialize defaults once options load
  useEffect(() => {
    if (data && (!filters.start_date || !filters.end_date)) {
      onChange({
        ...filters,
        start_date: data.date_range.min,
        end_date: data.date_range.max,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data]);

  const toggleMulti = (key: MultiKey, value: string) => {
    const current = filters[key];
    const exists = current.includes(value);
    const next = exists
      ? current.filter((v) => v !== value)
      : [...current, value];
    onChange({ ...filters, [key]: next });
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
          >
            {item}
          </button>
        );
      })}
    </div>
  );

  return (
    <div className="filter-bar">
      <div className="filter-header">
        {loading && <span className="badge">Loading…</span>}
        {error && (
          <span className="badge" style={{ background: "#ef4444" }}>
            {error}
          </span>
        )}
      </div>

      <div className="filter-group">
        <p className="label">Date Range</p>
        <div className="date-row">
          <input
            type="date"
            value={formatDateInput(filters.start_date)}
            min={data?.date_range.min}
            max={filters.end_date || data?.date_range.max}
            onChange={(e) =>
              onChange({ ...filters, start_date: e.target.value || undefined })
            }
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
          />
        </div>
      </div>

      <div className="filter-group">
        <p className="label">Regions</p>
        {data ? (
          renderPills(data.regions, "regions")
        ) : (
          <div className="skeleton" />
        )}
      </div>

      <div className="filter-group">
        <p className="label">Segments</p>
        {data ? (
          renderPills(data.segments, "segments")
        ) : (
          <div className="skeleton" />
        )}
      </div>

      <div className="filter-group">
        <p className="label">Categories</p>
        {data ? (
          renderPills(data.categories, "categories")
        ) : (
          <div className="skeleton" />
        )}
      </div>
    </div>
  );
}
