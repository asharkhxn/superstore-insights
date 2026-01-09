import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import MetricCard from "../components/MetricCard";

describe("MetricCard", () => {
  it("renders the title", () => {
    render(<MetricCard title="Test Metric" value={100} />);
    expect(screen.getByText("Test Metric")).toBeInTheDocument();
  });

  it("formats currency correctly", () => {
    render(<MetricCard title="Sales" value={1234.56} format="currency" />);
    expect(screen.getByText("$1,235")).toBeInTheDocument();
  });

  it("formats percentage correctly", () => {
    render(<MetricCard title="Margin" value={12.34} format="percent" />);
    expect(screen.getByText("12.34%")).toBeInTheDocument();
  });

  it("formats numbers correctly", () => {
    render(<MetricCard title="Orders" value={1234} format="number" />);
    expect(screen.getByText("1,234")).toBeInTheDocument();
  });

  it("defaults to number format", () => {
    render(<MetricCard title="Count" value={100} />);
    expect(screen.getByText("100")).toBeInTheDocument();
  });
});
