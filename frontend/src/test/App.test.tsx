import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "../App";

// Mock the fetch hook
vi.mock("../hooks/useFetch", () => ({
  useFetch: vi.fn(() => ({
    data: {
      total_sales: 1000,
      total_profit: 200,
      total_orders: 50,
      total_customers: 25,
      avg_order_value: 20,
      profit_margin: 20,
    },
    loading: false,
    error: null,
  })),
}));

describe("App", () => {
  it("renders the app header", () => {
    render(<App />);
    expect(screen.getByText(/Superstore Insights/i)).toBeInTheDocument();
  });

  it("renders all tab buttons", () => {
    render(<App />);
    expect(screen.getByText("By Category")).toBeInTheDocument();
    expect(screen.getByText("By Region")).toBeInTheDocument();
    expect(screen.getByText("Trends")).toBeInTheDocument();
    expect(screen.getByText("Profit Analysis")).toBeInTheDocument();
    expect(screen.getByText("Segments")).toBeInTheDocument();
  });

  it("has Category tab active by default", () => {
    render(<App />);
    const categoryButton = screen.getByText("By Category");
    expect(categoryButton).toHaveClass("active");
  });

  it("changes active tab on click", async () => {
    const user = userEvent.setup();
    render(<App />);

    const regionButton = screen.getByText("By Region");
    await user.click(regionButton);

    expect(regionButton).toHaveClass("active");
    expect(screen.getByText("By Category")).not.toHaveClass("active");
  });

  it("renders overview metrics", () => {
    render(<App />);
    expect(screen.getByText("Total Sales")).toBeInTheDocument();
    expect(screen.getByText("Total Profit")).toBeInTheDocument();
  });
});
