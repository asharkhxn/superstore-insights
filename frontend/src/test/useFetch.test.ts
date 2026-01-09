import { describe, it, expect, beforeEach, vi } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { useFetch } from "../hooks/useFetch";

describe("useFetch", () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it("initializes with loading state", () => {
    vi.mocked(global.fetch).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    const { result } = renderHook(() => useFetch("/api/test"));

    expect(result.current.loading).toBe(true);
    expect(result.current.data).toBe(null);
    expect(result.current.error).toBe(null);
  });

  it("fetches data successfully", async () => {
    const mockData = { test: "data" };

    vi.mocked(global.fetch).mockResolvedValue({
      ok: true,
      json: async () => mockData,
    } as Response);

    const { result } = renderHook(() => useFetch("/api/test"));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toEqual(mockData);
    expect(result.current.error).toBe(null);
  });

  it("handles fetch errors", async () => {
    vi.mocked(global.fetch).mockResolvedValue({
      ok: false,
      status: 500,
    } as Response);

    const { result } = renderHook(() => useFetch("/api/test"));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toBe(null);
    expect(result.current.error).toBeTruthy();
  });

  it("handles network errors", async () => {
    vi.mocked(global.fetch).mockRejectedValue(new Error("Network error"));

    const { result } = renderHook(() => useFetch("/api/test"));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toBe(null);
    expect(result.current.error).toBe("Network error");
  });

  it("refetches when URL changes", async () => {
    const mockData1 = { test: "data1" };
    const mockData2 = { test: "data2" };

    vi.mocked(global.fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockData1,
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockData2,
      } as Response);

    const { result, rerender } = renderHook(({ url }) => useFetch(url), {
      initialProps: { url: "/api/test1" },
    });

    await waitFor(() => {
      expect(result.current.data).toEqual(mockData1);
    });

    rerender({ url: "/api/test2" });

    await waitFor(() => {
      expect(result.current.data).toEqual(mockData2);
    });
  });
});
